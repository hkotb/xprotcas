# Help page for xProtCAS web server

## Getting Started (Home page)

| ![home page](https://raw.githubusercontent.com/hkotb/xprotcas/main/img/homepage.png) |
|:--:|
| **Figure 1** Home page of xProtCAS web server. |
- Use the text box to search a protein name, gene name, or UniProt accession.
- Select the best match from the pop-down menu.
- Click the Analyse button.

## Navigation (Analysis page)

| ![analysis page](https://raw.githubusercontent.com/hkotb/xprotcas/main/img/analysis_page1.png) |
|:--:|
| **Figure 2** The default analysis page of the xProtCAS web server. |

#### 1. Tool name (click it to take you back to the home page)
#### 2. Protein name and species (click it to open the UniProt page of the protein).
#### 3. Interactive 3D viewer of AlphaFold predicted protein structure and protein sequence.
#### 4. Button to hide/display the side menu.
#### 5. Button to open the help page.
#### 6. Button to go back to the home page.
#### 7. List of the predicted autonomous structural units with the ability to switch between them to change the viewer's perspective. Each structural unit is represented by: 
- Pfam domains interseting the structural unit and the start and end positions of the structural unit on the protein sequence. 
- The predicted pocket evaluation scores: absolute patch conservation, relative patch conservation, and relative patch conservation p-value
- Structure quality scores of the structural unit: mean AlphaFold2 pLDDT score and mean AlphaFold2 Predicted Aligned Error (PAE) score.
#### 8. Switch between different views of the selected structural unit:
- Display the separated structural unit (Default).
- Display the structural unit in the context of the full-length protein.

<table align="center">
<thead>
<tr>
<th align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="https://raw.githubusercontent.com/hkotb/xprotcas/main/img/analysis_page3.png"><img align="center" src="https://raw.githubusercontent.com/hkotb/xprotcas/main/img/analysis_page3.png" width="500" style="max-width: 100%;"></a></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><strong>Figure 4</strong> The structural unit in the context of the full-length protein.</td>
</tr>
</tbody>
</table>

- Display the graph representation of the structural unit.

<table align="center">
<thead>
<tr>
<th align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="https://raw.githubusercontent.com/hkotb/xprotcas/main/img/analysis_page4.png"><img align="center" src="https://raw.githubusercontent.com/hkotb/xprotcas/main/img/analysis_page4.png" width="450" style="max-width: 100%;"></a></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><strong>Figure 5</strong> A graph representation of the structural unit. The graph displays each residue as a node represented with a circle in the graph; the filling colour of the circle reflects the chosen scoring scheme (if any), and the blue colour of the circles' circumference shows if the residue is a contacting residue in any known interface. The circle size reflects the residue's accessibility. Neighbouring nodes are connected with edges where edge thickness represents centrality scores.</td>
</tr>
</tbody>
</table>

- Display the multiple sequence alignment of the structural unit.

<table align="center">
<thead>
<tr>
<th align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="https://raw.githubusercontent.com/hkotb/xprotcas/main/img/analysis_page5.png"><img align="center" src="https://raw.githubusercontent.com/hkotb/xprotcas/main/img/analysis_page5.png" width="500" style="max-width: 100%;"></a></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><strong>Figure 6</strong> Multiple sequence alignment view of the structural unit. A variant of the Clustal X Colour Scheme is used to colour residues, where the default scheme colours are used, plus using grey colour for negative BLOSUM64 scoring positions and circles for charged residues changes. The sequence logo shows the composition of the alignment column of each position scaled by residue accessibility to emphasise more conserved and accessible residues. Each position is hoverable and reveals a tooltip with a detailed description.</td>
</tr>
</tbody>
</table>

#### 9. Switch between different scoring schemes for colouring residues/nodes in the viewer window.
- Region: Displays the structural unit residues (coloured in red).
- Eigenvector Centrality: Centrality scores are used in colouring residues while white represents low-scoring residues, blue for the medium range, and red for the high scores.

<table align="center">
<thead>
<tr>
<th align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="https://raw.githubusercontent.com/hkotb/xprotcas/main/img/analysis_page6.png"><img align="center" src="https://raw.githubusercontent.com/hkotb/xprotcas/main/img/analysis_page6.png" width="700" style="max-width: 100%;"></a></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><strong>Figure 7</strong> Eigenvector Centrality scoring with colour slider to change the middle point cutoff.</td>
</tr>
</tbody>
</table>

- Weighted Conservation Score: WCS are used in colouring residues.
- AlphaFold2 pLDDT: pLDDT scores of the AlphaFold model are used in colouring residues.
- AlphaFold2 accessibility: Accessibility scores calculated using DSSP software are used in colouring residues.
- Tesselation accessibility all atom: Tesselation accessibility where the residue is considered accessible if any of its atoms is accessible. Accessible residues are displayed in red.
- Tesselation accessibility sidechain: Tesselation accessibility where the residue is considered accessible if any of its side chain atoms is accessible. Accessible residues are displayed in red.
#### 10. Display the loading status of the data used on this page. After loading data finishes, the related functionality on this page resumes, and data can be downloaded (Centrality data, UniProt data, AlphaFold data, Accessibility data, Contact data, Conservation data, and Alignment data).
#### 11. External links.

## Technology Stack

- Backend: [Python](https://www.python.org/) programming language is used in the backend. PDB files are parsed with [BioPython](https://github.com/biopython/biopython). Centrality and Community Detection are implemented based on [NetworkX](https://networkx.org/). [NumPy](https://numpy.org/) is used to handle N-dimensional arrays and [SciPy](https://scipy.org/) to implement the Delaunay triangulation and Mann-Whitney U test. [Scikit-Learn](https://scikit-learn.org/stable/) is used in hierarchical clustering. HTTP requests are sent with [Requests](https://pypi.org/project/requests/). APIs are built with [FastAPI](https://fastapi.tiangolo.com/), and [Apache Kafka](https://kafka.apache.org/) is used internally to import data from internal pipelines.
- Frontend: User interface is built with [React](https://react.dev/).  Network viewer is based on [Cytoscape](https://cytoscape.org/). Strucutre viewer is based on [NGL](https://nglviewer.org/).

## Contact Information and Feedback

For technical assistance or to provide feedback on your experience using the website, please contact norman.davey@icr.ac.uk.
