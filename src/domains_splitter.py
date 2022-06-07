import networkx as nx
import numpy as np
import json

from Bio.PDB import PDBParser

#Graph-based community clustering approach to extract protein domains
#from https://pythonawesome.com/graph-based-community-clustering-approach-to-extract-protein-domains/
#https://github.com/tristanic/pae_to_domains
class AlphafoldDomainsSplitter():

	def get_pLDDT(self, pdb_path):

		parser = PDBParser()
		pLDDT = {}
		pLDDT_list = []
		structure = parser.get_structure('structure', pdb_path)
		for atom in structure.get_atoms():
			pLDDT[atom.parent.get_id()[1]] = atom.bfactor

		for i in range(len(pLDDT)):
			pLDDT_list.append(pLDDT[i+1])

		return pLDDT_list
		
	def parse_pae_file(self, pae_json_file):
		
		with open(pae_json_file, 'rt') as f:
			data = json.load(f)[0]
		
		r1, d = data['residue1'],data['distance']

		size = max(r1)

		matrix = np.empty((size,size))

		matrix.ravel()[:] = d

		return matrix

	def domains_from_pae_matrix_networkx(self, pae_json_file, pdb_path, pae_power=1, pae_cutoff=5, graph_resolution=1):
		
		pae_matrix = self.parse_pae_file(pae_json_file)
		pLDDT = self.get_pLDDT(pdb_path)
		
		weights = 1/pae_matrix**pae_power

		g = nx.Graph()
		edges = np.argwhere(pae_matrix < pae_cutoff)
		sel_weights = weights[edges.T[0], edges.T[1]]
		wedges = []
		for (i,j),w in zip(edges,sel_weights):
			if pLDDT[i] >= 70 and pLDDT[j] >= 70:
				wedges.append((i+1,j+1,w))
				
		g.add_weighted_edges_from(wedges)

		clusters = nx.algorithms.community.greedy_modularity_communities(g, weight='weight', resolution=graph_resolution)
		clusters_list = []
		for c in clusters:
			if len(c) >= 30:
				clusters_list.append(list(c))
		return clusters_list
