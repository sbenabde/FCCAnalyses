Authors: Sarah Ben Abdesselem and Axel Gallén

This folder contains all the instructions and files needed to generate long lived dark photon samples produced in the HAHM model https://github.com/davidrcurtin/HAHM.

## Setting up the FCCAnalyses environment
The FCCAnalyses framework is the software specifically designed for FCC related analyses. It is necessary to setup the FCCAnalyses environemnt with the correct key4hep version, and stay on that same key4hep version during the entire analysis, to avoid any version mismatch between python, ROOT and the EDM4HEP output formats. 

> [!IMPORTANT]
> The recommended version is the 2024-03-10 release. 

Setup the environment as follows:

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

> [!NOTE]
> We are using the v_5.3.11 version of MadGraph and the v3 version of the HAHM model extension

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
The **proc_card_HAHM.dat** in this folder generates the process 
> $$e^+e^- \to Z h, Z \to qq, h \to Z_D Z_D, Z_D \to \mu^+\mu^-$$ 

at a center-of-mass energy of 240 GeV (Zh pole at the FCC-ee), for dark photons with a mass $$m_{Z_D}$$= 5 GeV and a coupling constant
$$\varepsilon= 10^{-6}$$. The dark scalar is decoupled by fixing the dark scalar mass to $$m_{H_s}$$=200 GeV and the coupling $$\kappa$$ is set to $$10^{-3}$$. 

Download the **proc_card_HAHM.dat**, move it to the MG5_aMC_v3.4.1/ directory and while standing in the MG5_aMC_v3.4.1/ directory, run it with 

```
./bin/mg5_aMC proc_card_HAHM.dat

```
This will generate an output folder named *dark_photons_mZd5000MeV_e_1e-6.lhe*. Within this output folder, cd to the unweighted_events.lhe.gz

```
cd /eos/user/u/username/MG5_aMC_v3_5_11/dark_photons_mZd5000MeV_e_1e-6/Events/run_01

```
then unzip the .lhe.gz file, rename it to dark_photons_mZd5000MeV_e_1e-6.lhe, copy the file to the MG5_aMC_v3.4.1/ directory (this is important for the next step see down below), and finally, change the LesHouchesVersion from 3.0 to 2.0 (to avoid crashing issues with Pythia)

```
gunzip -c unweighted_events.lhe.gz > dark_photons_mZd5000MeV_e_1e-6.lhe
cp dark_photons_mZd5000MeV_e_1e-6.lhe /eos/user/u/username/MG5_aMC_v3_5_11
sed -i "1s/3.0/2.0/" dark_photons_mZd5000MeV_e_1e-6.lhe
```

## Generating a .ROOT file in EDM4HEP format with Delphes 
The .lhe output from the previous step serves as input to generate the final .root file. In your main eos directory, get the latest Delphes IDEA card winter2023 

```
git clone https://github.com/HEP-FCC/FCC-config.git
cd FCC-config/
git checkout winter2023
cd ..
```
Then download the dark_photon_pythia_HAHM.cmnd file in this folder. Make sure to place it in the same directory ad the .lhe file (if you follower the steps above, this should be the MG5_aMC_v3.4.1/ directory). Make sure the line

```
Beams:LHEF = /eos/user/u/username/MG5_aMC_v3_5_11/dark_photons_mZd360MeV_e_9.7e-7.lhe
```
corresponds to the *absolute* path to the .lhe file. 

Now you can generate the .root file with 

```
DelphesPythia8_EDM4HEP \
    ./FCC-config/FCCee/Delphes/card_IDEA.tcl \
    ./FCC-config/FCCee/Delphes/edm4hep_IDEA.tcl \
    "dark_photon_pythia_HAHM.cmnd" \
    "dark_photons_mZd5000MeV_e_1e-6.root"
```

This .root file can now serve as input in the stage1 step of your FCCAnalysis!
