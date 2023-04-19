# Help page for xProtCAS web server

## Home page

| ![home page](https://raw.githubusercontent.com/hkotb/xprotcas/main/img/homepage.png) |
|:--:|
| **Figure 1** Home page of xProtCAS web server. |
- Use the text box to search a protein name, gene name, or UniProt accession.
- Select the best match from the pop-down menu.
- Click the Analyse button.

## Analysis page

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
1. Pfam domains interseting the structural unit and the start and end positions of the structural unit on the protein sequence. 
2. The predicted pocket evaluation scores: absolute patch conservation, relative patch conservation, and relative patch conservation p-value
3. Structure quality scores of the structural unit: mean AlphaFold2 pLDDT score and mean AlphaFold2 Predicted Aligned Error (PAE) score.
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
<td align="center"><strong>Figure 5</strong> Graph representation of the structural unit. Each residue is a node represented with a circle in the graph; the filling colour of the circle reflects the chosen scoring scheme (if any), the blue colour of the circles' circumference shows if the residue is a contacting residue in any known interface, and the circle size reflects residue's accessibility. Neighbouring nodes are connected with edges where edge thickness represents centrality scores.</td>
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
<td align="center"><strong>Figure 6</strong> Multiple sequence alignment of the structural unit. An extension of the Clustal X Colour Scheme is used in colouring residues, where the default scheme colours are used, plus using grey colour for negative BLOSUM64 scoring positions and circle squares for charged residues. The top sequence logo of the positions' conservation is scaled with residues accessibility, leading to the boldness of the more conserved and accessible residues. Each position is made hoverable to make it easy to follow.</td>
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
