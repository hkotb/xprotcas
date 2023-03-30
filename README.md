# xProtCAS: a toolkit for extracting conserved accessible surfaces from protein structures

Pipeline to rank patches on the protein surface based on their evolutionary conservation. Hence, it can be used to find accessible, functional regions or pockets. The relatively high conservation property of SLiM-binding interfaces makes them more likely to be ranked first by the pipeline in SLiM-binding domains.

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

Coming soon.

## Software prerequisites

The pipeline relies on external software/libraries to handle protein databank files, compute mathematical/geometric features, and run graph algorithms.
The following is the list of required libraries and programs, as well as the version on which it was tested (in parenthesis).

* [Python](https://www.python.org/) (3.8)
* [BioPython](https://github.com/biopython/biopython) (1.78) . To parse PDB files. 
* [NetworkX](https://networkx.org/) (2.8) . To run graph algorithms (Centrality and Community Detection).
* [NumPy](https://numpy.org/) (1.20.1) . To handle N-dimensional arrays.
* [SciPy](https://scipy.org/) (1.8.1) . To implement the Delaunay triangulation.
* [Scikit-Learn](https://scikit-learn.org/stable/) (0.24.1) . To run hierarchical clustering.
* [Requests](https://pypi.org/project/requests/) (2.25.1) .  To send HTTP requests.
* [Pymol](https://pymol.org/2/) (2.4) . To visualise files of the detected patches (optional).

## Installation methods

### Install manually

Install dependencies in the [Software prerequisites](#software-prerequisites) section and clone the repository to a local directory:

```
git clone https://github.com/hkotb/pocket-detector.git
cd pocket-detector/src
```
> **Note**
> It is more convenient to make `pocket-detector/src` your current working directory before running the pipeline using python commands on your local machine, as the default input and output pathes are relative pathes.

### Build a docker image

To build a Docker image from the provided Dockerfile run the following steps:

```
git clone https://github.com/hkotb/pocket-detector.git
cd pocket-detector/
docker build -t pocket_docker .
```
> **Note**
> You have to abide by the name you choose while using your built image later (*pocket_docker*).

### Pull a prebuilt docker image

To pull the prebuilt image run the following command:

```
docker pull (coming soon)
git clone https://github.com/hkotb/pocket-detector.git
cd pocket-detector/
```
> **Note**
> You have to abide by the name of the prebuilt image while using it later (*coming soon*).

> **Note**
> When using docker to run the pipeline, it is more convenient to make `pocket-detector` your current working directory, as the docker commands in the [Usage](#usage) section assume that while copying files between the local machine and the container.

## Usage

Run the pipeline help to display all arguments and their usage:
```
python pipeline_starter.py -h
```
##### output
```
usage: pipeline_starter.py [-h] [--output OUTPUT] [--input INPUT] [--uniprot UNIPROT] [--pdb PDB] [--create_pymol_session {true,false}] [--pdb_file PDB_FILE] [--conservations_file CONSERVATIONS_FILE]
                           [--split_into_domains {true,false}] [--predicted_aligned_error_file PREDICTED_ALIGNED_ERROR_FILE] [--orthdb_taxon_id {metazoa,qfo}]
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
  --orthdb_taxon_id {metazoa,qfo}
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
docker run -t -d --name my_pocket_container pocket_docker
docker exec -it my_pocket_container python pipeline_starter.py --uniprot Q9Y2M5
docker cp my_pocket_container:/home/submitter/output ./
docker stop my_pocket_container
docker rm my_pocket_container
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
docker run -t -d --name my_pocket_container pocket_docker
docker cp ./input my_pocket_container:/home/submitter/
docker exec -it my_pocket_container python pipeline_starter.py --pdb_file AF-Q9Y2M5-F1-model_v2.pdb --predicted_aligned_error_file AF-Q9Y2M5-F1-predicted_aligned_error_v2.json --conservations_file Q9Y2M5.json
docker cp my_pocket_container:/home/submitter/output ./
docker stop my_pocket_container
docker rm my_pocket_container
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
docker run -t -d --name my_pocket_container pocket_docker
docker cp ./input my_pocket_container:/home/submitter/
docker exec -it my_pocket_container python pipeline_starter.py --uniprot Q9Y2M5 --conservations_file Q9Y2M5.json
docker cp my_pocket_container:/home/submitter/output ./
docker stop my_pocket_container
docker rm my_pocket_container
```

#### Example 4
To run the pipeline on PDB ID 6GY5:
```
python pipeline_starter.py --pdb 6GY5
```
using docker:
```
docker run -t -d --name my_pocket_container pocket_docker
docker exec -it my_pocket_container python pipeline_starter.py --pdb 6GY5
docker cp my_pocket_container:/home/submitter/output ./
docker stop my_pocket_container
docker rm my_pocket_container
```
To run the four previous examples in sequence using docker:
```
docker run -t -d --name my_pocket_container pocket_docker
docker cp ./input my_pocket_container:/home/submitter/
docker exec -it my_pocket_container python pipeline_starter.py --uniprot Q9Y2M5
docker exec -it my_pocket_container python pipeline_starter.py --pdb_file AF-Q9Y2M5-F1-model_v2.pdb --predicted_aligned_error_file AF-Q9Y2M5-F1-predicted_aligned_error_v2.json --conservations_file Q9Y2M5.json
docker exec -it my_pocket_container python pipeline_starter.py --uniprot Q9Y2M5 --conservations_file Q9Y2M5.json
docker exec -it my_pocket_container python pipeline_starter.py --pdb 6GY5
docker cp my_pocket_container:/home/submitter/output ./
docker stop my_pocket_container
docker rm my_pocket_container
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
    │   │   ├── "patch_1"                       # List of residues in the first patch. This is the patch extracted in the first iteration of the pipeline.
    .   .   .
    .   .   .
    .   .   .
    │   │   └── "patch_Y"                       # List of residues in the Yth patch. This is the patch extracted in the Yth iteration of the pipeline. Y is also the last iteration when the pipeline managed to extract a patch. It may equal to --number_of_iterations, but problems might happen like centrality algorithm didn't converge or found a null graph which stops the pipeline from iterating.

##### Example:
```
{
   "A":{
      "1":{
         "residues":{
            "569":{
               "accessibility":1,
               "direct_neighbors":[
                  "588",
                  "568",
                  "570",
                  "590",
                  "567",
                  "586",
                  "587"
               ],
               "conservation":0.9800213730114914,
               "score_1":0.053242423120163467,
               "score_2":0.06493437708360261,
               "score_3":0.14207539050855633
            },
            
            .
            .
            .
            
            
            "481":{
               "accessibility":1,
               "direct_neighbors":[
                  "482",
                  "484",
                  "488",
                  "461",
                  "483",
                  "479"
               ],
               "conservation":0.02442049018777954,
               "score_1":1.5743151237165947e-05,
               "score_2":3.6067521230009605e-05,
               "score_3":0.0001062967061076688,
               "score_4":0.000297498470140901,
               "score_5":0.003226209826219515,
               "score_6":0.0034970183811533617,
               "score_7":1.2720170094315094e-07,
               "score_8":0.00020938996371843265,
               "score_9":7.831977990248131e-17,
               "score_10":0.0011277709361562313,
               "score_11":1.6578448400169872e-05,
               "score_12":7.951245944424763e-18,
               "score_13":-3.711039523855571e-17,
               "score_14":0.001565006522628566,
               "score_15":-9.826237778743287e-17,
               "score_16":1.5226014301304893e-16,
               "score_17":1.5479693663486075e-17,
               "score_18":9.11271197709341e-16,
               "score_19":-6.831509768318384e-16,
               "score_20":5.654817645439343e-18
            },
            "433":{
               "accessibility":1,
               "direct_neighbors":[
                  "438",
                  "384",
                  "435",
                  "395"
               ],
               "conservation":0.9921633859944954,
               "score_1":0.0038023064253798412,
               "score_2":0.1166187093841972,
               "score_3":0.020399471467322534,
               "score_4":0.3401026273680234
            }
         },
         "patch_1":[
            "357",
            "404",
            "592",
            
            .
            .
            .
            
            "468",
            "596",
            "548"
         ],
         
         .
         .
         .
         
         "patch_20":[
            "429",
            "442"
         ]
      },
      "2":{
         "residues":{
            "43":{
               "accessibility":1,
               "direct_neighbors":[
                  "44",
                  "42",
                  "45"
               ],
               "conservation":0.2895153150655207,
               "score_1":5.385905385527337e-08,
               "score_2":1.4060713614160727e-05,
               "score_3":2.4619712208448296e-17,
               "score_4":5.503709193648589e-05,
               "score_5":4.7048914948664833e-17,
               "score_6":0.001995248967941242,
               "score_7":2.3937219494890312e-17,
               "score_8":-2.988131354053637e-17,
               "score_9":0.00021845395125914973,
               "score_10":0.042416629195786384,
               "score_11":1.0031818449494086e-16,
               "score_12":3.692446695015138e-17,
               "score_13":3.584953655424851e-18,
               "score_14":1.4223217634554498e-16,
               "score_15":4.2085572494897746e-17,
               "score_16":-1.6621678810559538e-18,
               "score_17":7.194404491665816e-16,
               "score_18":1.0404002054294159e-16,
               "score_19":0.586004580885965
            },
            
            .
            .
            .
            
            "223":{
               "accessibility":1,
               "direct_neighbors":[
                  "224",
                  "225",
                  "311",
                  "312",
                  "222"
               ],
               "conservation":1.0,
               "score_1":0.07161495483220802,
               "score_2":0.04890532776917767,
               "score_3":0.3663655357268663
            }
         },
         "patch_1":[
            "295",
            "294",
            
            .
            .
            .
            
            "284",
            "310"
         ],
         
         .
         .
         .
         
         "patch_20":[
            "64",
            "63",
            
            .
            .
            .
            
            "53",
            "54"
         ]
      }
   }
}
```

#### Visualise PyMOL session file

*.pse file can be loaded using PyMOL. It enables the virtualisation of all the detected patches with their ranks.

Example:
![PyMOL session](https://raw.githubusercontent.com/hkotb/pocket-detector/main/img/pymol.gif)
> **Note**
> In this example, chain A is split into two domains, A1 and A2. A.excluded contains the excluded residues, whether because they are in the protein's core or disordered. The red colours on the 3D structure represent high scores, while blue is for average scores.

## License

This source code is licensed under the MIT license found in the `LICENSE` file in the root directory of this source tree.

## Reference

If you find the pipeline useful in your research, we ask that you cite our paper:
```
Coming soon
```

