from scipy.spatial.distance import euclidean
from scipy.spatial import Delaunay

import numpy as np

#Calculating accessibility and neighbourhood of residues based on the idea presented in:
#Detection of Functionally Important Regions in “Hypothetical Proteins” of Known Structure

rad_siz = {'ALAN':1.65, 'ALACA':1.87, 'ALAC':1.76, 'ALAO':1.40, 'ALACB':1.87, 'ARGN':1.65, 'ARGCA':1.87, 'ARGC':1.76, 'ARGO':1.40, 'ARGCB':1.87, 'ARGCG':1.87, 'ARGCD':1.87, 'ARGNE':1.65, 'ARGCZ':1.76, 'ARGNH1': 1.65, 'ARGNH2': 1.65, 'ASPN':1.65, 'ASPCA':1.87, 'ASPC':1.76, 'ASPO':1.40, 'ASPCB':1.87, 'ASPCG':1.76, 'ASPOD1': 1.40, 'ASPOD2': 1.40, 'ASNN':1.65, 'ASNCA':1.87, 'ASNC':1.76, 'ASNO':1.40, 'ASNCB':1.87, 'ASNCG':1.76, 'ASNOD1': 1.40, 'ASNND2': 1.65, 'CYSN':1.65, 'CYSCA':1.87, 'CYSC':1.76, 'CYSO':1.40, 'CYSCB':1.87, 'CYSSG':1.85, 'GLUN':1.65, 'GLUCA':1.87, 'GLUC':1.76, 'GLUO':1.40, 'GLUCB':1.87, 'GLUCG':1.87, 'GLUCD':1.76, 'GLUOE1': 1.40, 'GLUOE2': 1.40, 'GLNN':1.65, 'GLNCA':1.87, 'GLNC':1.76, 'GLNO':1.40, 'GLNCB':1.87, 'GLNCG':1.87, 'GLNCD':1.76, 'GLNOE1': 1.40, 'GLNNE2': 1.65, 'GLYN':1.65, 'GLYCA':1.87, 'GLYC':1.76, 'GLYO':1.40, 'HISN':1.65, 'HISCA':1.87, 'HISC':1.76, 'HISO':1.40, 'HISCB':1.87, 'HISCG':1.76, 'HISND1': 1.65, 'HISCD2': 1.76, 'HISCE1': 1.76, 'HISNE2': 1.65, 'ILEN':1.65, 'ILECA':1.87, 'ILEC':1.76, 'ILEO':1.40, 'ILECB':1.87, 'ILECG1': 1.87, 'ILECG2': 1.87, 'ILECD1': 1.87, 'LEUN':1.65, 'LEUCA':1.87, 'LEUC':1.76, 'LEUO':1.40, 'LEUCB':1.87, 'LEUCG':1.87, 'LEUCD1': 1.87, 'LEUCD2': 1.87, 'LYSN':1.65, 'LYSCA':1.87, 'LYSC':1.76, 'LYSO':1.40, 'LYSCB':1.87, 'LYSCG':1.87, 'LYSCD':1.87, 'LYSCE':1.87, 'LYSNZ':1.50, 'METN':1.65, 'METCA':1.87, 'METC':1.76, 'METO':1.40, 'METCB':1.87, 'METCG':1.87, 'METSD':1.85, 'METCE':1.87, 'PHEN':1.65, 'PHECA':1.87, 'PHEC':1.76, 'PHEO':1.40, 'PHECB':1.87, 'PHECG':1.76, 'PHECD1': 1.76, 'PHECD2': 1.76, 'PHECE1': 1.76, 'PHECE2': 1.76, 'PHECZ':1.76, 'PRON':1.65, 'PROCA':1.87, 'PROC':1.76, 'PROO':1.40, 'PROCB':1.87, 'PROCG':1.87, 'PROCD':1.87, 'SERN':1.65, 'SERCA':1.87, 'SERC':1.76, 'SERO':1.40, 'SERCB':1.87, 'SEROG':1.40, 'THRN':1.65, 'THRCA':1.87, 'THRC':1.76, 'THRO':1.40, 'THRCB':1.87, 'THROG1': 1.40, 'THRCG2': 1.87, 'TRPN':1.65, 'TRPCA':1.87, 'TRPC':1.76, 'TRPO':1.40, 'TRPCB':1.87, 'TRPCG':1.76, 'TRPCD1': 1.76, 'TRPCD2': 1.76, 'TRPNE1': 1.65, 'TRPCE2': 1.76, 'TRPCE3': 1.76, 'TRPCZ2': 1.76, 'TRPCZ3': 1.76, 'TRPCH2': 1.76, 'TYRN':1.65, 'TYRCA':1.87, 'TYRC':1.76, 'TYRO':1.40, 'TYRCB':1.87, 'TYRCG':1.76, 'TYRCD1': 1.76, 'TYRCD2': 1.76, 'TYRCE1': 1.76, 'TYRCE2': 1.76, 'TYRCZ':1.76, 'TYROH':1.40, 'VALN':1.65, 'VALCA':1.87, 'VALC':1.76, 'VALO':1.40, 'VALCB':1.87, 'VALCG1': 1.87, 'VALCG2': 1.87}
class AccessibilityScorer():
	def __init__(self, coords, atm_keys):
		self.faces = {}
		self.faces_tetrahedrons1 = {}
		self.faces_tetrahedrons2 = {}
		self.removed_faces = {}
		
		self.coords = coords
		self.atm_keys = atm_keys
	
	def get_accessible_residues_and_their_neighbors(self):
		
		accessible_residues = {}
		direct_neighbors = {}
		tri = Delaunay(self.coords)
		updated_cavity_set = True
		
		for indx, tetrahedron in enumerate(tri.simplices):
			tetrahedron.sort()
			for i in range(4):
				mask = np.ones(4, np.bool)
				mask[i] = 0
				self.fill_data_dicts(" ".join(np.char.mod('%d', tetrahedron[mask])), indx)
		
		while updated_cavity_set:
			updated_cavity_set = False
			for face, num_tetrahedrons in self.faces.items():
				if num_tetrahedrons == 1:
					a, b, c = face.split()
					if self.VDW_distance(a, b) >=2.8 or self.VDW_distance(a, c) >= 2.8 or self.VDW_distance(c, b) >= 2.8:
						tetrahedron = tri.simplices[self.faces_tetrahedrons1[face]]
						tetrahedron_indx = self.faces_tetrahedrons1[face]
						for i in range(4):
							mask = np.ones(4, np.bool)
							mask[i] = 0
							self.update_data_dicts(" ".join(np.char.mod('%d', tetrahedron[mask])), tetrahedron_indx)
						updated_cavity_set = True
		
		for face, num_tetrahedrons in self.faces.items():
			if num_tetrahedrons == 1 or self.removed_faces[face] == 1:
				a, b, c = face.split()
				self.add_accessible_atm(a, accessible_residues)
				self.add_accessible_atm(b, accessible_residues)
				self.add_accessible_atm(c, accessible_residues)
		
		#get tri direct neighbors
		for face, num_tetrahedrons in self.faces.items():
			if num_tetrahedrons == 1:
				a, b, c = face.split()
				self.connect_neighbor_atms(a, b, direct_neighbors)
				self.connect_neighbor_atms(a, c, direct_neighbors)
				self.connect_neighbor_atms(b, c, direct_neighbors)
				
		#sets to lists to make them compatible with json format
		for res_key in accessible_residues:
			accessible_residues[res_key]['accessible_atms'] = list(accessible_residues[res_key]['accessible_atms'])
		for res_key in direct_neighbors:
			direct_neighbors[res_key] = list(direct_neighbors[res_key])
		
		return accessible_residues, direct_neighbors

	def fill_data_dicts(self, face, indx):
		if face in self.faces:
	   		self.faces[face]+=1
	   		self.faces_tetrahedrons2[face] = indx
		else:
	   		self.faces[face]=1
	   		self.faces_tetrahedrons1[face] = indx
	   		self.faces_tetrahedrons2[face] = -1
	   		self.removed_faces[face] = 0

	def VDW_rad(self, indx):
		res_key, res_name, atm = self.atm_keys[int(indx)].split('_')
		rad_key = res_name+atm
		return rad_siz[rad_key] if rad_key in rad_siz else 1.7
		
	def VDW_distance(self, atm1_indx, atm2_indx):
		return euclidean(self.coords[int(atm1_indx)], self.coords[int(atm2_indx)])-self.VDW_rad(atm1_indx)-self.VDW_rad(atm2_indx)

	def update_data_dicts(self, face, indx):
		self.faces[face]-=1
		if self.faces[face] == 0:
			self.removed_faces[face] = 1
		if self.faces_tetrahedrons1[face] == indx:
			self.faces_tetrahedrons1[face] = self.faces_tetrahedrons2[face]

	def add_accessible_atm(self, atm_indx, accessible_residues):
		atm_key = self.atm_keys[int(atm_indx)]
		res_key, res_name, atm = atm_key.split('_')
		if res_key not in accessible_residues:
			accessible_residues[res_key] = {}
			accessible_residues[res_key]['accessible_atms'] = set()
			accessible_residues[res_key]['side_chain_score'] = 0
								
		accessible_residues[res_key]['accessible_atms'].add(atm)
		accessible_residues[res_key]['any_atm_score'] = 1
		if atm not in {'CA', 'C', 'N', 'O'}:
			accessible_residues[res_key]['side_chain_score'] = 1

	def connect_neighbor_atms(self, atm1_indx, atm2_indx, direct_neighbors):
		atm1_key = self.atm_keys[int(atm1_indx)]
		res1_key, res1_name, atm1 = atm1_key.split('_')
		atm2_key = self.atm_keys[int(atm2_indx)]
		res2_key, res2_name, atm2 = atm2_key.split('_')
		if res1_key != res2_key:
			if res1_key not in direct_neighbors:
				direct_neighbors[res1_key] = set()
			direct_neighbors[res1_key].add(res2_key)
			if res2_key not in direct_neighbors:
				direct_neighbors[res2_key] = set()
			direct_neighbors[res2_key].add(res1_key)
