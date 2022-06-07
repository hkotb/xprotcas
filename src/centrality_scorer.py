import networkx as nx
import numpy as np

from sklearn.cluster import AgglomerativeClustering
from collections import deque

class CentralityScorer():

	def eigenvector_centrality(self, merged_data, max_number_of_patches, logging):
		for pdb_chain in merged_data:
			for domain in merged_data[pdb_chain]:
				previous_patches = set()
				for patch_indx in range(1, max_number_of_patches+1):
					DG=nx.DiGraph()
					for residue in merged_data[pdb_chain][domain]['residues']:
						neighbors = merged_data[pdb_chain][domain]['residues'][residue]['direct_neighbors'] if 'direct_neighbors' in merged_data[pdb_chain][domain]['residues'][residue] else []
						acc = merged_data[pdb_chain][domain]['residues'][residue]['accessibility'] if 'accessibility' in merged_data[pdb_chain][domain]['residues'][residue] else -1
						cons = merged_data[pdb_chain][domain]['residues'][residue]['conservation'] if 'conservation' in merged_data[pdb_chain][domain]['residues'][residue] else 0
						if residue not in previous_patches and acc > 0.001 and 'conservation' in merged_data[pdb_chain][domain]['residues'][residue]:
							edges = 0
							for nbr_ind, nbr in enumerate(neighbors):
								if nbr in merged_data[pdb_chain][domain]['residues'] and 'conservation' in merged_data[pdb_chain][domain]['residues'][nbr]:
									nbr_acc = merged_data[pdb_chain][domain]['residues'][nbr]['accessibility'] if 'accessibility' in merged_data[pdb_chain][domain]['residues'][nbr] else -1
									if nbr not in previous_patches and nbr_acc > 0.001:
										edges+=1
							wt = 1/edges if edges else None
							for nbr_ind, nbr in enumerate(neighbors):
								if nbr in merged_data[pdb_chain][domain]['residues'] and 'conservation' in merged_data[pdb_chain][domain]['residues'][nbr]:
									nbr_acc = merged_data[pdb_chain][domain]['residues'][nbr]['accessibility'] if 'accessibility' in merged_data[pdb_chain][domain]['residues'][nbr] else -1
									if nbr not in previous_patches and nbr_acc > 0.001:
										DG.add_weighted_edges_from([(nbr,residue,cons*wt)])


					if len(DG) > 0:
						try:
							centrality_dict = nx.eigenvector_centrality_numpy(DG, weight='weight', max_iter=1000)
						except:
							logging.info("Stopped iterating after %d iterations due to no convergence (chain %s, domain %s).", patch_indx, pdb_chain, domain)
							break

						scrs = []
						keys = []
						for residue, score in centrality_dict.items():
							merged_data[pdb_chain][domain]['residues'][residue]['score_' + str(patch_indx)] = score
							scrs.append(score)
							keys.append(residue)
						
						#cluster residues hierarchically into 2 groups based on their scores.
						X = np.array(scrs).reshape(-1, 1)
						clustering = AgglomerativeClustering(n_clusters=2).fit(X)

						#define a patch of high-scoring connected residues starting by the residue with the highest score
						queue = deque()
						max_score_index = scrs.index(max(scrs))
						high_scores_set = set(np.array(keys)[clustering.labels_==clustering.labels_[max_score_index]])
						residue = keys[max_score_index]
						queue.append(residue)
						high_scores_set.remove(residue)
						patch = []
						while len(queue)>0:
							residue = queue.popleft()
							patch.append(residue)
							if len(high_scores_set) > 0:
								for nbr in merged_data[pdb_chain][domain]['residues'][residue]['direct_neighbors']:
									if nbr in high_scores_set:
										queue.append(nbr)
										high_scores_set.remove(nbr)
										
						merged_data[pdb_chain][domain]['patch_' + str(patch_indx)] = patch
						previous_patches.update(patch)
					else:
						logging.info("Stopped iterating after %d iterations due to null graph (chain %s, domain %s).", patch_indx, pdb_chain, domain)
						break
