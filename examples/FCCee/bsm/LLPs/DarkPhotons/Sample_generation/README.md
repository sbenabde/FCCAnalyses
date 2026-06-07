Authors: Sarah Ben Abdesselem and Axel Gallén

This folder contains all the instructions and files needed to generate long lived dark photon samples produced in the HAHM model https://github.com/davidrcurtin/HAHM.

## Setting up the FCCAnalyses environment
The FCCAnalyses framework is the software specifically designed for FCC related analyses. It is necessary to setup the FCCAnalyses environemnt with the correct key4hep version, and stay on that same key4hep version during the entire analysis, to avoid any version mismatch between python, ROOT and the EDM4HEP output formats. The recommended version is the 2024-03-10 release. Setup the environment as follows:

```
source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2024-03-10
source ./setup.sh
```
after setting up the environment (and after implementing any changes in the scripts within the FCCAnalyses/python folder), it is necessary to build the framework with the command

```
fccanalysis build -j
```

## Downloading MadGraph and the HAHM model

Once the framework is setup, you'll need to download two files:
- **MadGraph** from https://launchpad.net/mg5amcnlo
- **The HAHM model** MadGraph extension from https://github.com/davidrcurtin/HAHM \
We are using the v_5.3.11 version of MadGraph and the v3 version of the HAHM model extension

Import the MadGraph tarball and the HAHM model zip file to your eos space. If you're working from your terminal, do this with the commands

```
scp MG5_aMC_v5.3.11.tar username@lxplus.cern.ch:/path/to/your/dir
scp HAHM_MG5model_v3.zip username@lxplus.cern.ch:/path/to/your/dir
```
then, from lxplus, unzip both the tarball and the HAHM model zip file 

```
tar -xf MG5_aMC_v3.4.1.tar
tar -xf HAHM_MG5model_v3.zip
```
Finally, move both the _HAHM_variableMW_UFO_ and _HAHM_variablesw_UFO_ folders to the directory *MG5_aMC_v3_4_1/models/*.

## Generating dark photon samples with a process card

