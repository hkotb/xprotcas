import os, sys, datetime, time, requests
import argparse
from Bio.PDB import PDBParser, Selection
from Bio.PDB.Polypeptide import three_to_one

from pdb_parser import read_clean_pdb
from accessibility_scorer import AccessibilityScorer
from centrality_scorer import CentralityScorer
from domains_splitter import AlphafoldDomainsSplitter

import logging

try:
	from pymol import cmd
	is_pymol_installed = True
except:
	is_pymol_installed = False

import numpy as np
import json
import math

from pathlib import Path


class PipelineStarter:

	def get_parsed_args(self):
		parser = argparse.ArgumentParser(description='Run functional regions detector.')
		parser.add_argument('--output', type=str, default='../output', help='Path to an output directory where the pipeline results will be saved.')
		parser.add_argument('--input', type=str, default='../input', help='Path to the directory where the input files should be saved.')
		parser.add_argument('--uniprot', type=str, default=None, help='UniProt accession, --uniprot or --pdb should be passed, not both of them.')
		parser.add_argument('--pdb', type=str, default=None, help='PDB id, --uniprot or --pdb should be passed, not both of them.')
		parser.add_argument('--create_pymol_session', type=str, default='true', choices=['true', 'false'], help='PyMol session will be created if this option is true and PyMol is installed. (default: true)')
		parser.add_argument('--pdb_file', type=str, default=None, help='The file name of the resolved or predicted structure (in PDB format) (should be saved in the input directory). If it is passed, the pipeline will use it and not download a pdb file based on uniprot/pdb options.')
		parser.add_argument('--conservations_file', type=str, default=None, help='The name of conservation scores file (should be saved in the input directory). If it is passed, the pipeline will use it and not call SLiM RESTful APIs to get the conservation scores based on uniprot/pdb options.')
		parser.add_argument('--split_into_domains', type=str, default='true', choices=['true', 'false'], help='If true, the pipeline will split AlphaFold predicted structure into domains. (default: true)')
		parser.add_argument('--predicted_aligned_error_file', type=str, default=None, help='The name of AlphaFold predicted aligned error file (should be saved in the input directory). If it is passed, the pipeline will use it instead of trying to download it from AlphaFold database. It is used in splitting AlphaFold predicted structure into domains.')
		parser.add_argument('--orthdb_taxon_id', type=str, default='metazoa', choices=['metazoa', 'qfo'], help='The search database to find orthologous sequences to the query structure. It is used by SLiM tools to generate conservations. (default: metazoa)')
		parser.add_argument('--number_of_iterations', type=int, default=20, help='Maximum number of iterations the pipeline will perform (per each chain/domain). (default: 20)')
		parser.add_argument('--log', type=str, default='info', choices=['debug', 'info', 'warning', 'error', 'critical'], help='Specify the logging level. (default: info)')
		parser.add_argument('--slim_server', type=str, default='http://slim.icr.ac.uk/restapi/rest/get/', help='SLiM tools server url.')
		args = parser.parse_args()
		
		if args.uniprot and args.pdb:
			parser.error("--uniprot and --pdb can't be used together.")
		if not args.uniprot and not args.pdb and (not args.pdb_file or not args.conservations_file):
			parser.error("at least --pdb_file and --conservations_file are required, if no --uniprot and --pdb are passed.")
			
		args.create_pymol_session = True if args.create_pymol_session == 'true' else False
		args.split_into_domains = True if args.split_into_domains == 'true' else False
		numeric_level = getattr(logging, args.log.upper())
		FORMAT = '%(levelname)s: %(message)s'
		logging.basicConfig(level=numeric_level, format=FORMAT)
		return args
	
	def check_file_existence(self, file_path):
		if not os.path.exists(file_path):
			logging.error("Can not find the specified file path %s Make sure:\n- The name of the file is correct.\n- The file is in the input directory.\n- If you are using docker, you have copied the input directory on your local machine to the docker container by `docker cp ./input my_pocket_container:/home/submitter/`\n- If you are running on your local machine, you have passed the input file to the pipeline using --input argument.", file_path)
			sys.exit(1)
	
	def download_file(self, id, output_path, file_type):
		logging.info("downloading %s, %s", id, file_type)
		start = time.time()
		
		try:
			if file_type == 'pdb_structure':
				url = "http://files.rcsb.org/download/" + id + ".pdb"
				out_path = os.path.join(output_path, id + ".pdb")
			elif file_type == 'alphafold_structure':
				url = "https://alphafold.ebi.ac.uk/files/AF-" + id + "-F1-model_v2.pdb"
				out_path = os.path.join(output_path, "AF-" + id + "-F1-model_v2.pdb")
			elif file_type == 'alphafold_error':
				url = "https://alphafold.ebi.ac.uk/files/AF-" + id + "-F1-predicted_aligned_error_v2.json"
				out_path = os.path.join(output_path, "AF-" + id + "-F1-predicted_aligned_error_v2.json")
			
			resp = requests.get(url)
			status = resp.status_code
			
			if status == 200:
				content = resp.text
				open(out_path,"w").write(content)
			else:
				raise Exception()
		except:
			logging.error('Failed to download, URL %s, try to download it manually and pass it using the options --pdb_file or --predicted_aligned_error_file.', url)
			sys.exit(1)
		
		end = time.time()
		logging.info('Finished downloading in %f seconds', end - start)
		return out_path

	def waiter(self, status):
		if status not in ['Finished','Error','Success']:
			return True
		else:
			time.sleep(1)
			return False

	def get_conservations(self, id, orthdb_taxon_id, output_path, slim_server, file_type):
		logging.info("downloading conservations for %s %s", file_type, id)
		start = time.time()
		
		try:
			if file_type == 'pdb':
				url = slim_server + "evolution?task=get_conservation_scores_by_pdb&orthdb_taxon_id=%s&conservation_score_type=WCS&pdb_id=%s" % (orthdb_taxon_id, id)
			elif file_type == 'uniprot':
				url = slim_server + "evolution?task=get_conservation_score&orthdb_taxon_id=%s&conservation_score_type=WCS&accession=%s" % (orthdb_taxon_id, id)
			
			out_path = os.path.join(output_path, id + ".conservations.json")
			is_running = True
			while is_running:
				resp = requests.get(url)
				content = resp.json()
				is_running = self.waiter(content['status'])

			if content['status'] == 'Success':
				with open(out_path, 'w') as fl:
					json.dump(content, fl)
			else:
				raise Exception()
		except:
			logging.error('Failed to download conservations, URL %s, try to download it manually and pass it using the option --conservations_file.', url)
			sys.exit(1)
		
		end = time.time()
		logging.info('Finished downloading in %f seconds', end - start)
		return out_path
	
	def confirm_same_sequence_is_used(self, uniprot, orthdb_taxon_id, pdb_file, slim_server):
		logging.info("checking sequence used in calculating conservations matches the pdb file")
		start = time.time()
		
		parser = PDBParser()
		structure = parser.get_structure('structure', pdb_file)
		residues = Selection.unfold_entities(structure, 'R')
		
		try:
			url = slim_server + "evolution?task=get_alignment_query_sequence_gopher&orthdb_taxon_id=%s&accession=%s" % (orthdb_taxon_id, uniprot)
			is_running = True
			while is_running:
				resp = requests.get(url)
				content = resp.json()
				is_running = self.waiter(content['status'])

			if content['status'] == 'Success' and len(content['data']['sequence']) == len(residues):
				for residue_indx, residue in enumerate(residues):
					resname = residue.get_resname()
					pdb_residue = three_to_one(resname)
					if pdb_residue != content['data']['sequence'][residue_indx]:
						raise Exception()
			else:
				raise Exception()
		except:
			logging.error('The sequence used in calculating conservations and the pdb file sequence don\'t match!')
			sys.exit(1)
		
		end = time.time()
		logging.info('Finished checking in %f seconds', end - start)
	
	def split_domains(self, predicted_aligned_error_file, pdb_file):
		logging.info("Splitting structure into domains...")
		start = time.time()
		alphafoldDomainsSplitterObj = AlphafoldDomainsSplitter()
		domains = alphafoldDomainsSplitterObj.domains_from_pae_matrix_networkx(predicted_aligned_error_file, pdb_file)
		end = time.time()
		logging.info('Finished splitting in %f seconds', end - start)
		return domains
		
	def get_accessibility(self, pdb_file, domains=[None]):
		logging.info("Calculating accessibility...")
		start = time.time()
		
		parser = PDBParser()
		structure = parser.get_structure('structure', pdb_file)
		model = structure[0]
		pdb_chains = [c.id for c in Selection.unfold_entities(model, "C")]
		
		self.data = {}
		
		for pdb_chain in pdb_chains:
			self.data[pdb_chain] = {}
			for domain_indx, domain in enumerate(domains):
				model = read_clean_pdb(pdb_file, pdb_chain, domain)
				
				atm_keys = []
				coords = []

				for r in model.get_residues():
					res_id = r.get_full_id()[3]
					res_key = str(res_id[1])+res_id[2].strip()
					
					for atom in r.get_atoms():
						if atom.get_name().strip() != "H":
							atm_keys.append(res_key+'_'+r.get_resname().strip()+'_'+atom.get_name().strip())
							coords.append(atom.get_coord())
				
				AccessibilityScorerObj = AccessibilityScorer(np.array(coords), np.array(atm_keys))
				accessible_residues, direct_neighbors = AccessibilityScorerObj.get_accessible_residues_and_their_neighbors()
				
				chain_details = {
					'accessible_residues': accessible_residues,
					'direct_neighbors': direct_neighbors
				}
				
				self.data[pdb_chain][str(domain_indx+1)] = chain_details
		
		end = time.time()
		logging.info('Finished calculating accessibility in %f seconds', end - start)
		return self.data
	
	def merge_conservations(self, conservations_file, accessibility_data):
		with open(conservations_file, 'r') as fl:
			conservations = json.load(fl)['data']
		
		merged_data = {}
		
		for pdb_chain in accessibility_data:
			merged_data[pdb_chain] = {}
			for domain in accessibility_data[pdb_chain]:
				merged_data[pdb_chain][domain] = {'residues':{}}
				for residue in accessibility_data[pdb_chain][domain]['accessible_residues']:
					if residue not in merged_data[pdb_chain][domain]['residues']:
						merged_data[pdb_chain][domain]['residues'][residue] = {}
					merged_data[pdb_chain][domain]['residues'][residue]['accessibility'] = accessibility_data[pdb_chain][domain]['accessible_residues'][residue]['any_atm_score']
				
				for residue in accessibility_data[pdb_chain][domain]['direct_neighbors']:
					if residue not in merged_data[pdb_chain][domain]['residues']:
						merged_data[pdb_chain][domain]['residues'][residue] = {}
					merged_data[pdb_chain][domain]['residues'][residue]['direct_neighbors'] = accessibility_data[pdb_chain][domain]['direct_neighbors'][residue]
					
				if pdb_chain in conservations:
					chain_cons = conservations[pdb_chain]
				else:
					chain_cons = conservations
				for residue in merged_data[pdb_chain][domain]['residues']:
					if residue in chain_cons:
						merged_data[pdb_chain][domain]['residues'][residue]['conservation'] = chain_cons[residue]
		
		return merged_data
	
	def run_centrality_iterations(self, merged_data, number_of_iterations):
		logging.info("Calculating centrality scores and patches through iterations...")
		start = time.time()
		centralityScorerObj = CentralityScorer()
		centralityScorerObj.eigenvector_centrality(merged_data, number_of_iterations, logging)
		end = time.time()
		logging.info('Finished calculating scores and patches in %f seconds', end - start)
		
	def create_pymol_session(self, merged_data, pdb_file, output_path):
		logging.info("Creating PyMol session...")
		start = time.time()
		cmd.reinitialize()
		pdb_file_no_ext = Path(pdb_file).stem
		for i, prop in enumerate(["conservation"]+["score_"+str(patch_indx) for patch_indx in range(1, 21)]):
			cmd.load(pdb_file)
			cmd.hide('everything')
			cmd.show("surface")
			file_chains = cmd.get_chains()
			for pdb_chain in file_chains:
				chain_selector = "/"+pdb_file_no_ext+"//"+pdb_chain+"/"
				for domain in merged_data[pdb_chain]:
					minimum = math.inf
					to_default = []
					for residue in merged_data[pdb_chain][domain]['residues']:
						if prop in merged_data[pdb_chain][domain]['residues'][residue]:
							cmd.set_atom_property(prop, merged_data[pdb_chain][domain]['residues'][residue][prop], chain_selector+residue, proptype=3)
							if merged_data[pdb_chain][domain]['residues'][residue][prop] < minimum:
								minimum = merged_data[pdb_chain][domain]['residues'][residue][prop]
						else:
							to_default.append(residue)
					for residue in to_default:
						cmd.set_atom_property(prop, minimum, chain_selector+residue, proptype=3)

					domain_selector = pdb_chain+str(domain)+'.'+prop
					cmd.extract(domain_selector, " ".join([chain_selector+residue for residue in merged_data[pdb_chain][domain]['residues']]))
					cmd.spectrum("properties['"+prop+"']", "white_blue_red", domain_selector)
					
					if i != 0:
						cmd.disable(domain_selector)
				
				if i == 0:
					cmd.color("white", chain_selector)
					cmd.extract(pdb_chain+'.excluded', chain_selector)
			cmd.delete(pdb_file_no_ext)
				
		cmd.zoom()
		cmd.bg_color('white')
		cmd.save(os.path.join(output_path, pdb_file_no_ext+'.pse'))
		end = time.time()
		logging.info('Finished creating PyMol session in %f seconds', end - start)
		
	def main(self):
		args = self.get_parsed_args()
		
		output_path = os.path.join(args.output, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
		os.makedirs(output_path)
		logging.info("The results will be saved in: %s \nIf you are using docker, copy the results to your local machine by `docker cp my_pocket_container:/home/submitter/output ./`", output_path)
		
		if args.pdb_file:
			pdb_file = os.path.join(args.input, args.pdb_file)
			self.check_file_existence(pdb_file)
			logging.info("The pipeline will use the pdb file you passed.")
		else:
			if args.pdb:
				pdb_file = self.download_file(args.pdb, output_path, 'pdb_structure')
			else:
				pdb_file = self.download_file(args.uniprot, output_path, 'alphafold_structure')
		
		if args.conservations_file:
			conservations_file = os.path.join(args.input, args.conservations_file)
			self.check_file_existence(conservations_file)
			logging.info("The pipeline will use the conservations file you passed.")
		else:
			if args.pdb:
				conservations_file = self.get_conservations(args.pdb, args.orthdb_taxon_id, output_path, args.slim_server, 'pdb')
			else:
				conservations_file = self.get_conservations(args.uniprot, args.orthdb_taxon_id, output_path, args.slim_server, 'uniprot')
				self.confirm_same_sequence_is_used(args.uniprot, args.orthdb_taxon_id, pdb_file, args.slim_server)
		
		domains = [None]
		predicted_aligned_error_file = None
		if args.split_into_domains:
			if args.predicted_aligned_error_file:
				predicted_aligned_error_file = os.path.join(args.input, args.predicted_aligned_error_file)
				self.check_file_existence(predicted_aligned_error_file)
				logging.info("The pipeline will use the predicted aligned error file you passed.")
			elif args.uniprot:
				predicted_aligned_error_file = self.download_file(args.uniprot, output_path, 'alphafold_error')
			
			if predicted_aligned_error_file:
				domains = self.split_domains(predicted_aligned_error_file, pdb_file)
		
		accessibility_data = self.get_accessibility(pdb_file, domains)
		merged_data = self.merge_conservations(conservations_file, accessibility_data)
		
		self.run_centrality_iterations(merged_data, args.number_of_iterations)
		
		with open(os.path.join(output_path, 'merged_data.json'), 'w') as fl:
			json.dump(merged_data, fl)
		
		if args.create_pymol_session:
			if is_pymol_installed:
				self.create_pymol_session(merged_data, pdb_file, output_path)
			else:
				logging.warning('Pymol is not installed, no pymol session will be created!')

if __name__ == "__main__":
	pipelineStarterObj = PipelineStarter()
	pipelineStarterObj.main()
    
    

