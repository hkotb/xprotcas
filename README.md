# xProtCAS: a toolkit for extracting conserved accessible surfaces from protein structures

Pipeline to score residues and extract patches from the protein surface based on their conservation. Hence, it can be used to find accessible, functional regions or binding interfaces.

## Table of contents
* [Description](#description)
* [Software prerequisites](#software-prerequisites)
* [Installation methods](#installation-methods)
* [Usage](#usage)
* [Input files](#input-files)
* [Output files](#output-files)
* [License](#license)
* [Reference](#reference)

## Description

![xProtCAS workflow](https://raw.githubusercontent.com/hkotb/xProtCAS/main/img/workflow.png)

The workflow of the framework includes five major steps: (i) definition of the autonomous structural units of a protein; (ii) calculation of the residue-centric conservation, accessibility and topology metrics for the structural unit; (iii) creation of an edge-weighted directed graph encoding the structural and evolutionary properties for the structural unit; (iv) definition the conserved accessible surfaces using hierarchical clustering of eigenvector centrality scores; and (v) scoring and annotation of the conserved accessible surfaces. For more details, please refer to the paper.

## Software prerequisites

The pipeline relies on external software/libraries to handle protein databank files, compute mathematical/geometric features, and run graph algorithms.
The following is the list of required libraries and programs, as well as the version on which it was tested (in parenthesis).

* [Python](https://www.python.org/) (3.8)
* [BioPython](https://github.com/biopython/biopython) (1.78) . To parse PDB files. 
* [NetworkX](https://networkx.org/) (2.8) . To run graph algorithms (Centrality and Community Detection).
* [NumPy](https://numpy.org/) (1.20.1) . To handle N-dimensional arrays.
* [SciPy](https://scipy.org/) (1.8.1) . To implement the Delaunay triangulation and Mann-Whitney U test.
* [Scikit-Learn](https://scikit-learn.org/stable/) (0.24.1) . To run hierarchical clustering.
* [Requests](https://pypi.org/project/requests/) (2.25.1) .  To send HTTP requests.
* [Pymol](https://pymol.org/2/) (2.4) . To visualise files of the detected patches (optional).

## Installation methods

Choose one of the three following installation methods. However, using our prebuild docker image is the easiest way to get started.

### Install manually

Install dependencies in the [Software prerequisites](#software-prerequisites) section and clone the repository to a local directory:

```
git clone https://github.com/hkotb/xProtCAS.git
cd xProtCAS/src
```
> **Note**
> It is more convenient to make `xProtCAS/src` your current working directory before running the pipeline using python commands on your local machine, as the default input and output pathes are relative pathes.

### Build a docker image

To build a Docker image from the provided Dockerfile run the following steps:

```
git clone https://github.com/hkotb/xProtCAS.git
cd xProtCAS/
docker build -t xprotcas .
```
> **Note**
> You have to abide by the name you choose while using your built image later (*xprotcas*).

### Pull a prebuilt docker image

To pull our prebuilt image run the following command:

```
docker pull hkotb/xprotcas
```
> **Note**
> You have to abide by the name of the prebuilt image while using it later (*hkotb/xprotcas*).

## Usage

Run the pipeline help to display all arguments and their usage:
```
python pipeline_starter.py -h
```
##### output
```
usage: pipeline_starter.py [-h] [--output OUTPUT] [--input INPUT] [--uniprot UNIPROT] [--pdb PDB] [--create_pymol_session {true,false}] [--pdb_file PDB_FILE] [--conservations_file CONSERVATIONS_FILE]
                           [--split_into_domains {true,false}] [--predicted_aligned_error_file PREDICTED_ALIGNED_ERROR_FILE] [--orthdb_taxon_id {metazoa,qfo,vertebrates,mammalia}]
                           [--number_of_iterations NUMBER_OF_ITERATIONS] [--log {debug,info,warning,error,critical}] [--slim_server SLIM_SERVER]

Run functional regions detector.

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT       Path to an output directory where the pipeline results will be saved.
  --input INPUT         Path to the directory where the input files should be saved.
  --uniprot UNIPROT     UniProt accession, --uniprot or --pdb should be passed, not both of them.
  --pdb PDB             PDB id, --uniprot or --pdb should be passed, not both of them.
  --create_pymol_session {true,false}
                        PyMol session will be created if this option is true and PyMol is installed. (default: true)
  --pdb_file PDB_FILE   The file name of the resolved or predicted structure (in PDB format) (should be saved in the input directory). If it is passed, the pipeline will use it and not download a pdb
                        file based on uniprot/pdb options.
  --conservations_file CONSERVATIONS_FILE
                        The name of conservation scores file (should be saved in the input directory). If it is passed, the pipeline will use it and not call SLiM RESTful APIs to get the conservation
                        scores based on uniprot/pdb options.
  --split_into_domains {true,false}
                        If true, the pipeline will split AlphaFold predicted structure into domains. (default: true)
  --predicted_aligned_error_file PREDICTED_ALIGNED_ERROR_FILE
                        The name of AlphaFold predicted aligned error file (should be saved in the input directory). If it is passed, the pipeline will use it instead of trying to download it from
                        AlphaFold database. It is used in splitting AlphaFold predicted structure into domains.
  --orthdb_taxon_id {metazoa,qfo,vertebrates,mammalia}
                        The search database to find orthologous sequences to the query structure. It is used by SLiM tools to generate conservations. (default: metazoa)
  --number_of_iterations NUMBER_OF_ITERATIONS
                        Maximum number of iterations the pipeline will perform (per each chain/domain). (default: 20)
  --log {debug,info,warning,error,critical}
                        Specify the logging level. (default: info)
  --slim_server SLIM_SERVER
                        SLiM tools server url.

```

#### Example 1
To run the pipeline on uniprot accession Q9Y2M5 use the command:
```
python pipeline_starter.py --uniprot Q9Y2M5
```
using docker:
```
docker run -t -d --name my_xprotcas_container hkotb/xprotcas
docker exec -it my_xprotcas_container python pipeline_starter.py --uniprot Q9Y2M5
docker cp my_xprotcas_container:/home/submitter/output ./
docker stop my_xprotcas_container
docker rm my_xprotcas_container
```
> **Note**
> The `run` command creates a container, `exec` uses the created container to run the command, `cp` copies the output from inside the container to your local mahcine, `stop` and `rm` to stop the container and remove it. We prefer to use `cp` command over mounting local directories as docker volumes to avoid any permission probelmes between the host and the container.

#### Example 2
To run the pipeline on specific files on your local machine:
```
python pipeline_starter.py --pdb_file AF-Q9Y2M5-F1-model_v2.pdb --predicted_aligned_error_file AF-Q9Y2M5-F1-predicted_aligned_error_v2.json --conservations_file Q9Y2M5.json
```
> **Note**
> Assuming the files are placed in the default input directory, there is no need to pass --input argument.

using docker:
```
docker run -t -d --name my_xprotcas_container hkotb/xprotcas
docker cp ./input my_xprotcas_container:/home/submitter/
docker exec -it my_xprotcas_container python pipeline_starter.py --pdb_file AF-Q9Y2M5-F1-model_v2.pdb --predicted_aligned_error_file AF-Q9Y2M5-F1-predicted_aligned_error_v2.json --conservations_file Q9Y2M5.json
docker cp my_xprotcas_container:/home/submitter/output ./
docker stop my_xprotcas_container
docker rm my_xprotcas_container
```
> **Note**
> We have added here one extra `cp` step to copy the input directory from your local machine to the container before executing the command.

#### Example 3
To run the pipeline on uniprot accession Q9Y2M5 but with a specific conservations file from your local machine:
```
python pipeline_starter.py --uniprot Q9Y2M5 --conservations_file Q9Y2M5.json
```
using docker:
```
docker run -t -d --name my_xprotcas_container hkotb/xprotcas
docker cp ./input my_xprotcas_container:/home/submitter/
docker exec -it my_xprotcas_container python pipeline_starter.py --uniprot Q9Y2M5 --conservations_file Q9Y2M5.json
docker cp my_xprotcas_container:/home/submitter/output ./
docker stop my_xprotcas_container
docker rm my_xprotcas_container
```

#### Example 4
To run the pipeline on PDB ID 6GY5:
```
python pipeline_starter.py --pdb 6GY5
```
using docker:
```
docker run -t -d --name my_xprotcas_container hkotb/xprotcas
docker exec -it my_xprotcas_container python pipeline_starter.py --pdb 6GY5
docker cp my_xprotcas_container:/home/submitter/output ./
docker stop my_xprotcas_container
docker rm my_xprotcas_container
```
To run the four previous examples in sequence using docker:
```
docker run -t -d --name my_xprotcas_container hkotb/xprotcas
docker cp ./input my_xprotcas_container:/home/submitter/
docker exec -it my_xprotcas_container python pipeline_starter.py --uniprot Q9Y2M5
docker exec -it my_xprotcas_container python pipeline_starter.py --pdb_file AF-Q9Y2M5-F1-model_v2.pdb --predicted_aligned_error_file AF-Q9Y2M5-F1-predicted_aligned_error_v2.json --conservations_file Q9Y2M5.json
docker exec -it my_xprotcas_container python pipeline_starter.py --uniprot Q9Y2M5 --conservations_file Q9Y2M5.json
docker exec -it my_xprotcas_container python pipeline_starter.py --pdb 6GY5
docker cp my_xprotcas_container:/home/submitter/output ./
docker stop my_xprotcas_container
docker rm my_xprotcas_container
```

## Input files

The pipeline will grab them automatically, but you can optionally provide them.

    .
    ├── PDB                     # Downlaoded from PDB or Alphafold databases
    ├── Conservations           # Create one from SLiM tools RESTful APIs
    ├── Predicted aligned error # Downaloaded from Alphafold database

#### Conservations file format

If you want to create your own conservations file, instead of using results returned from SLiM tools RESTful APIs, follow the following format:
```
{
   "data":{
      "A":{
         "317":0.6376021525986822,
         "318":0.8349590754476021,
         "319":0.6597751935569642,
         
         .
         .
         .
         
         "599":0.17295363833060104,
         "600":0.21248774408861887,
         "601":0.14574453946172294
      },
      "U":{
         "1334":0.6756696043085054,
         "1335":0.5544372819953505,
         "1336":0.5697273349944153,
         
         .
         .
         .
         
         "1342":0.1550935920994699,
         "1343":0.09108525697019905,
         "1344":0.07128042175662261
      }
   }
}
```
Where "A" and "U" are the chains in the pdb file. "317":0.6376021525986822 assigns conservation score 0.6376021525986822 to the residue with sequence number 317, etc.

## Output files

The pipeline will produce the following files:

    .
    ├── *.pdb                               # The downlaoded PDB file (if you didn't use --pdb_file).
    ├── *.conservations.json                # The created conservations file from SLiM tools RESTful APIs (if you didn't use --conservations_file).
    ├── *-predicted_aligned_error_v2.json   # Downaloaded predicted aligned error file (if you used --uniprot, --split_into_domains was true, and didn't use --predicted_aligned_error_file).
    ├── merged_data.json                    # The results, including centrality scores and ranked patches.
    ├── *.pse                               # PyMOL session file (if PyMOL is installed and --create_pymol_session is true).

#### merged_data.json file format

The merged_data.json file is the major output of the pipeline and it has the following format:

    .
    ├── chain 
    │   ├── domain
    │   │   ├── "residues"
    │   │   │   ├── residue's sequence number
    │   │   │   │   ├── "accessibility"          # Always has the value 1 as the results contain accessible residues only.
    │   │   │   │   ├── "direct_neighbors"       # List of neighbour residues to this specific residue in the Delaunay triangulation.
    │   │   │   │   ├── "conservation"           # Conservation score of this specific residue (from the conservations file)
    │   │   │   │   ├── "score_1"                # The centrality score for this residue on the first iteration.
    .   .   .   .   .
    .   .   .   .   .
    .   .   .   .   .
    │   │   │   │   └── "score_X"               # The centrality score for this residue on Xth iteration. X is the iteration when this residue was selected in the patch of central residues.
    .   .   .   .
    .   .   .   .
    .   .   .   .
    │   │   │   └── residue's sequence number
    │   │   ├── "patch_1"                             # The first patch. This is the patch extracted in the first iteration of the pipeline.
    │   │   │   ├── "residues"                        # List of residues in the first patch.
    │   │   │   ├── "patch_conservation_mean"         # Mean patch conservation.
    │   │   │   ├── "patch_conservation_difference"   # The difference between mean patch conservation and mean non-patch conservation.
    │   │   │   └── "patch_conservation_pvalue"       # p-value of the Mann-Whitney U test of patch conservations to the non-patch conservations.
    .   .   .
    .   .   .
    .   .   .
    │   │   └── "patch_Y"                       # The Yth patch. This is the patch extracted in the Yth iteration of the pipeline. Y is also the last iteration when the pipeline managed to extract a patch. It may equal to --number_of_iterations, but problems might happen like centrality algorithm didn't converge or found a null graph which stops the pipeline from iterating.

##### Example:
```
{
   "A":{
      "1":{
         "residues":{
            "318": {
               "accessibility": 1,
               "direct_neighbors": [
                  "598",
                  "551",
                  "338",
                  "600",
                  "553",
                  "319",
                  "554"
               ],
               "conservation": 0.8349590754476024,
               "score_1": 0.00033068561774767614,
               "score_2": 0.003976137444726946,
               "score_3": 0.004157688400901547,
               "score_4": 0.03592842084943813,
               "score_5": 0.01930988819468361,
               "score_6": 0.19329758289234808
            },
            
            .
            .
            .
            
            
            "599": {
               "accessibility": 1,
               "direct_neighbors": [
                  "387",
                  "365",
                  "600",
                  "319",
                  "321"
               ],
               "conservation": 0.17295363833060104,
               "score_1": 0.00010753379553353566,
               "score_2": 0.0022105078526197678,
               "score_3": 0.001117286314411295,
               "score_4": 0.013368541320983066,
               "score_5": 0.0013258888042676014,
               "score_6": 0.01427290268982088,
               "score_7": 0.05193837060072906,
               "score_8": 1.6861154589542962e-7,
               "score_9": 0.00037484282552134704,
               "score_10": 0.000017629096441159546,
               "score_11": 0.04617722058371434,
               "score_12": -1.2681081705743956e-15,
               "score_13": 1.7241949030324695e-15,
               "score_14": 0.2616932881394638
            },
            "600": {
               "accessibility": 1,
               "direct_neighbors": [
                  "599",
                  "362",
                  "365",
                  "318",
                  "598",
                  "319"
               ],
               "conservation": 0.21248774408861887,
               "score_1": 0.0000761960316721797,
               "score_2": 0.0016847472149046766,
               "score_3": 0.000997893003956213,
               "score_4": 0.01343725373983663,
               "score_5": 0.004481525100512187,
               "score_6": 0.04512572092482299,
               "score_7": 0.04099458733679399,
               "score_8": 2.031085956839882e-7,
               "score_9": 0.0004508437188904322,
               "score_10": 0.000021196411712485968,
               "score_11": 0.055361193620167434,
               "score_12": -1.4889439728584647e-15,
               "score_13": 1.9990920480167914e-15,
               "score_14": 0.3074308020579626
            }
         },
         "patch_1": {
            "residues": [
               "405",
               "421",
               "499",
            
            .
            .
            .
            
               "562",
               "592",
               "326"
            ],
            "patch_conservation_mean": 0.9575961426660872,
            "patch_conservation_difference": 0.30507939164836484,
            "patch_conservation_pvalue": 8.596211261183572e-7
         },
         
         .
         .
         .
         
         "patch_20": {
            "residues": [
               "508",
               "506",
               "507"
            ],
            "patch_conservation_mean": 0.187915590231306,
            "patch_conservation_difference": -0.4941059262313974,
            "patch_conservation_pvalue": 0.9934569500920662
         }
      },
      "2":{
         "residues":{
            "41": {
               "accessibility": 1,
               "direct_neighbors": [
                  "43",
                  "42"
               ],
               "conservation": 0.31485642770736555,
               "score_1": 4.095330317951117e-9,
               "score_2": 0.000004357793466783931,
               "score_3": 0.000015317220742269545,
               "score_4": 0.0000010318277367862613,
               "score_5": 0.00000546114369877771,
               "score_6": 0.000028724474458458038,
               "score_7": -7.920020924280168e-18,
               "score_8": 0.0006733410768030233,
               "score_9": 0.000003798160113791288,
               "score_10": 5.376602530989818e-18,
               "score_11": 0.003945267490756683,
               "score_12": -8.031149324261881e-17,
               "score_13": -8.451131673320225e-17,
               "score_14": -6.493675595735365e-16,
               "score_15": -2.0968819501682493e-15,
               "score_16": -4.76131098384193e-16,
               "score_17": 0.47769033067499245
            },
            
            .
            .
            .
            
            "312": {
               "accessibility": 1,
               "direct_neighbors": [
                  "222",
                  "221",
                  "310",
                  "309",
                  "311",
                  "223"
               ],
               "conservation": 0.8056384639036711,
               "score_1": 0.05457085596700717
            }
         },
         "patch_1": {
            "residues": [
               "295",
               "294",
            
            .
            .
            .
            
               "281",
               "312"
            ],
            "patch_conservation_mean": 0.8518427508531001,
            "patch_conservation_difference": 0.21933607974408698,
            "patch_conservation_pvalue": 3.1043509158711496e-7
         },
         
         .
         .
         .
         
         "patch_20": {
            "residues": [
               "56",
               "57",
               "60",
               "53",
               "58",
               "54"
            ],
            "patch_conservation_mean": 0.21788566503943327,
            "patch_conservation_difference": -0.46527161683305185,
            "patch_conservation_pvalue": 0.9998017813668787
         }
      }
   }
}
```

#### Visualise PyMOL session file

*.pse file can be loaded using PyMOL. It enables the virtualisation of all the detected patches with their ranks.

Example:
![PyMOL session](https://raw.githubusercontent.com/hkotb/xProtCAS/main/img/pymol.gif)
> **Note**
> In this example, chain A is split into two domains, A1 and A2. A.excluded contains the excluded residues, whether because they are in the protein's core or disordered. The red colours on the 3D structure represent high scores, while blue is for average scores.

## License

This source code is licensed under the MIT license found in the `LICENSE` file in the root directory of this source tree.

## Reference

If you find the pipeline useful in your research, we ask that you cite our paper:
```
Coming soon
```

