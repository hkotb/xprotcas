from Bio.PDB import is_aa
from Bio.PDB.PDBIO import PDBIO
from Bio.PDB.PDBIO import Select
from Bio.PDB.PDBParser import PDBParser

import io

# Fixing potential issues in the PDB files (It was important when we were using DSSP-based accessibility). Currently, its main use is in selecting residues within the same domain in the predicted alphafold structures.
class SingleChainSelect(Select):
	"""
	Custom Bio.PDB.PDBIO.Select class to select a single chain (or domain).
		:param Select: parent Bio.PDB.PDBIO.Select
	"""
	def __init__(self, globular, domain):
		"""
		Creates a new SingleChainSelect class instance
			:param self:
			:param globular: a character string representing a PDB chain.
			:param domain: a collection of residues representing a seperate domain.
		"""
		self.globular = globular
		self.domain = domain

	def accept_model(self, model):
		"""
		Accepts only the first model of a PDB
			:param self:
			:param model:
		"""
		return 1 if model.id == 0 else 0

	def flag_residue_for_deletion(self, residue):
		for atom in residue.child_list:
			if atom.is_disordered():
				atom = atom.disordered_get()
				atom.altloc = "@"

	def accept_chain(self, chain):
		"""
		Accepts one chain, and flag disordered residues for deletion (to solve issues in 1AW8, 2HAL, 4AON, 4Z0Y, 6RXH)
			:param self:
			:param chain:
		"""
		if chain.id != self.globular:
			return 0
		
		disordered_dict = {}
		for res in chain.get_residues():
			if res.is_disordered():
				resseq = str(res.get_id()[1])
				icode = str(res.get_id()[2].strip())
				key = resseq+icode
				if key in disordered_dict:
					if disordered_dict[key].get_resname() != res.get_resname():
						if not is_aa(disordered_dict[key].get_resname(), standard=True) and is_aa(res.get_resname(), standard=True):
							self.flag_residue_for_deletion(disordered_dict[key])
						else:
							self.flag_residue_for_deletion(res)
				else:
					disordered_dict[key] = res
		
		return 1

	def accept_residue(self, residue):
		"""
		Accepts all residues with backbone atoms, but flag the disordered atoms which should be kept (to solve dropping atoms ex: 1F7A, 3FMA)
			:param self:
			:param residue:
		"""
		# REMOVE WATERS
		if residue.get_full_id()[3][0] == 'W':
			return 0
			
		# skip residues lacking a backbone atom
		all_atoms = [atom.get_name().strip() for atom in residue.get_atoms()]
		if residue.get_parent().id == self.globular and ("C" not in all_atoms or "CA" not in all_atoms or "N" not in all_atoms):
			return 0
			
		# flag the disordered atoms which should be kept
		for atom in residue.child_list:
			if atom.is_disordered():
				atom = atom.disordered_get()
				if atom.altloc != "@":
					atom.altloc = " "
		
		# skip residues not in the specified domain.
		if self.domain:
			if residue.get_id()[1] in self.domain:
				return 1
			else:
				return 0
		return 1

	def accept_atom(self, atom):
		"""
		Reject disordered atoms which are not flagged
			:param self:
			:param atom:
		"""
		# REMOVE HYDROGENS
		if atom.element.strip() == 'H':
			return 0
			
		if atom.is_disordered() and not atom.altloc.isspace():
			return 0
			
		return 1

def read_clean_pdb(pdb_file, globular, domain):
	
	parser = PDBParser()
		
	structure = parser.get_structure('structure', pdb_file)
	pdbio = PDBIO()
	pdbio.set_structure(structure)
	outputStream = io.StringIO()
	pdbio.save(outputStream, SingleChainSelect(globular, domain))
	outputStream.seek(0)
	
	return parser.get_structure('structure', outputStream)[0]

