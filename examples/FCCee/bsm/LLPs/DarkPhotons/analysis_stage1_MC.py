from argparse import ArgumentParser
import ROOT
import copy
from addons.FastJet.jetClusteringHelper import ExclusiveJetClusteringHelper

ROOT.gInterpreter.Declare("""
#include <vector>
#include <cmath>
#include <algorithm>

std::vector<std::vector<int>> get_best_paired_indices(ROOT::VecOps::RVec<float> eta, 
                                                     ROOT::VecOps::RVec<float> phi, 
                                                     ROOT::VecOps::RVec<float> charge){
    std::vector<std::vector<int>> all_pairs;
    if (eta.size() < 4) return all_pairs;         //Need at least 4 muons to produce 2 pairs

    std::vector<bool> used(eta.size(), false);

    // Find the first best pair
    double min_dR1 = 999.0;
    int idx1 = -1; int idx2 = -1;

    for (size_t i = 0; i < eta.size(); ++i) {               //size_t creates a non negative counter at i = 0, then adds to i with +ii for every iteration until we reach the size of eta.size.
        for (size_t j = i + 1; j < eta.size(); ++j) {
            
            if (charge[i] == charge[j]){                     //Only if the muons have different charge will we look at the dR
                continue;
                }
            
            double D_eta = eta[i] - eta[j];
            double D_phi = phi[i] - phi[j];
            while (D_phi >  M_PI) D_phi -= 2.0 * M_PI;      //M_PI is pi constant, this line checks the periodicity of the angle
            while (D_phi < -M_PI) D_phi += 2.0 * M_PI;      //Making sure we remain between 0 en 180 degrees
            double current_dR = std::sqrt(D_eta*D_eta+ D_phi*D_phi);
        
            if(current_dR < min_dR1){
                min_dR1 = current_dR;
                idx1 = i; idx2 = j;
            }
        }
    }
    if (idx1 != -1) {
        all_pairs.push_back({idx1, idx2});
        used[idx1] = true; used[idx2] = true; 
    }
    double min_dR2 = 999.0;
    int idx3 = -1; int idx4 = -1;

    for (size_t i = 0; i < eta.size(); ++i) {                   //size_t creates a non negative counter at i = 0, then adds to i with +ii for every iteration until we reach the size of eta.size.
        if (used[i]) continue;
        for (size_t j = i + 1; j < eta.size(); ++j) {
            if (used[j] || charge[i] == charge[j]) continue;                 //Only if the muons have different charge will we look at the dR
                
            double D_eta = eta[i] - eta[j];
            double D_phi = phi[i] - phi[j];
            while (D_phi >  M_PI) D_phi -= 2.0 * M_PI;      //M_PI is pi constant, this line checks the periodicity of the angle
            while (D_phi < -M_PI) D_phi += 2.0 * M_PI;      //Making sure we remain between 0 en 180 degrees
            double current_dR = std::sqrt(D_eta*D_eta+ D_phi*D_phi);
        
            if(current_dR < min_dR2){
                min_dR2 = current_dR;
                idx3 = i; idx4 = j;
            }
        }
    }
    if (idx3 != -1) all_pairs.push_back({idx3, idx4});
    
    return all_pairs;   //Return index of muon 1 and muon 2 that have shortest dR
}

double get_pair_dR(std::vector<int> pair_indices,
                 ROOT::VecOps::RVec<float> eta, 
                 ROOT::VecOps::RVec<float> phi) {

    if (pair_indices.size() < 2 || pair_indices[0] == -1) return -1.0;

    int i = pair_indices[0];
    int j = pair_indices[1];

    double D_eta = eta[i] - eta[j];
    double D_phi = phi[i] - phi[j];
    
    while (D_phi >  M_PI) D_phi -= 2.0 * M_PI;
    while (D_phi < -M_PI) D_phi += 2.0 * M_PI;

    return std::sqrt(D_eta * D_eta + D_phi * D_phi);
}
""")

#Mandatory: Analysis class where the user defines the operations on the dataframe
class Analysis():

    def __init__(self, cmdline_args):

        self.process_list = {
            'dark_photons_mZd360MeV_e_1e-5':{},
            'dark_photons_mZd1100MeV_e_3.12e-6':{},
            'dark_photons_mZd7000MeV_e_2.7e-7':{},
        }
        # self.input_dir = '/eos/experiment/fcc/ee/analyses_storage/BSM/LLPs/DarkPhotons'
        self.input_dir = '/eos/user/s/sbenabde/MG5_aMC_v3_5_11/Root_files_HAHM_New/'
        self.output_dir = "STAGE1_output/gen"
        
        self.analysis_name = 'My Analysis'
        self.n_threads = 1


    def analyzers(self, dframe):

        TTree_Branch_Name_parents = '_Particle_parents'
        TTree_Branch_Name_daughters = '_Particle_daughters'
        TTree_Muon_Name = 'Muon_objIdx'
        TTree_Electron_Name = 'Electron_objIdx'
        TTree_EflowTrack_Name = '_EFlowTrack_trackStates'
        TTree_MCRecoAssociations0 = '_MCRecoAssociations_rec'
        TTree_MCRecoAssociations1 = '_MCRecoAssociations_sim'
            
        dframe2 = (
            dframe
            .Alias("Particle0", f"{TTree_Branch_Name_parents}.index")
            .Alias("Particle1", f"{TTree_Branch_Name_daughters}.index")
            .Alias('Muon0', f"{TTree_Muon_Name}.index")
            .Alias('Electron0', f"{TTree_Electron_Name}.index")
            .Alias('EFlowTracks', f"{TTree_EflowTrack_Name}")
            .Alias("MCRecoAssociations0", f"{TTree_MCRecoAssociations0}.index")
            .Alias("MCRecoAssociations1", f"{TTree_MCRecoAssociations1}.index")
#---------- Generated muons ------------------------------------------------------------------------------------------------------------------------------------------------------
        
            .Define("GenMuon_PID",        "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)") #Keep particle only if its a muon
            .Define("FSGenMuon",          "FCCAnalyses::MCParticle::sel_genStatus(1)(GenMuon_PID)") #Keep muon only if its final state (FS)
            .Define("n_FSGenMuon",        "FCCAnalyses::MCParticle::get_n(FSGenMuon)")              #Get number of final state generated muons
            
            .Define("FSGenMuon_e",        "FCCAnalyses::MCParticle::get_e(FSGenMuon)")
            .Define("FSGenMuon_p",        "FCCAnalyses::MCParticle::get_p(FSGenMuon)")
            .Define("FSGenMuon_pt",       "FCCAnalyses::MCParticle::get_pt(FSGenMuon)")
            .Define("FSGenMuon_px",       "FCCAnalyses::MCParticle::get_px(FSGenMuon)")
            .Define("FSGenMuon_py",       "FCCAnalyses::MCParticle::get_py(FSGenMuon)")
            .Define("FSGenMuon_pz",       "FCCAnalyses::MCParticle::get_pz(FSGenMuon)")
            .Define("FSGenMuon_eta",      "FCCAnalyses::MCParticle::get_eta(FSGenMuon)")
            .Define("FSGenMuon_theta",    "FCCAnalyses::MCParticle::get_theta(FSGenMuon)")
            .Define("FSGenMuon_phi",      "FCCAnalyses::MCParticle::get_phi(FSGenMuon)")
            .Define("FSGenMuon_charge",   "FCCAnalyses::MCParticle::get_charge(FSGenMuon)")
            .Define("FSGenMuon_mass",     "FCCAnalyses::MCParticle::get_mass(FSGenMuon)")
        
            .Define("FSGenMuon_vertex_x", " FCCAnalyses::MCParticle::get_vertex_x(FSGenMuon)")
            .Define("FSGenMuon_vertex_y", " FCCAnalyses::MCParticle::get_vertex_y(FSGenMuon)")
            .Define("FSGenMuon_vertex_z", " FCCAnalyses::MCParticle::get_vertex_z(FSGenMuon)")
           
            .Define("FSGen_Lxy",   "return sqrt(FSGenMuon_vertex_x*FSGenMuon_vertex_x + FSGenMuon_vertex_y*FSGenMuon_vertex_y)")
            .Define("FSGen_Lxyz",  "return sqrt(FSGenMuon_vertex_x*FSGenMuon_vertex_x + FSGenMuon_vertex_y*FSGenMuon_vertex_y + FSGenMuon_vertex_z*FSGenMuon_vertex_z)")
            
#---------- Generated Muon Daughters ------------------------------------------------------------------------------------------------------------------------------------------------------

            #Get collection of indices of the muons that come from the Higgs boson (including the Higgs boson itself)
            .Define("Daughters_indices",    "FCCAnalyses::MCParticle::get_indices(25, {13, -13, 13, -13}, true, true, true, true)(Particle, Particle1)")
            .Define("Daughters_size",       "Daughters_indices.size()")
            .Define("Daughters",            "ROOT::VecOps::Take(Particle, Daughters_indices)")
            .Define("DaughtersPDG",         'FCCAnalyses::MCParticle::get_pdg(Daughters)')

            #Extract Higgs parent from the index collection
            .Define("Higgs_mom",         "FCCAnalyses::MCParticle::sel_pdgID(25, true)(Daughters)")
            .Define("n_Higgs_mom",       "Higgs_mom.size()")
            .Define("Higgs_mom_mass",    "FCCAnalyses::MCParticle::get_mass(Higgs_mom)")

            #Extract Muon daughters from the index collection
            .Define("Muons_daughters",      "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Daughters)")
            .Define("n_Muons_daughters",    "Muons_daughters.size()")
            .Define("Muons_daughters_mass", "FCCAnalyses::MCParticle::get_mass(Muons_daughters)")

            #.Define("Muons_daughters_e",    "FCCAnalyses::MCParticle::get_e(Muons_daughters)")
            .Define("Muons_daughters_p",    "FCCAnalyses::MCParticle::get_p(Muons_daughters)")
            .Define("Muons_daughters_px",   "FCCAnalyses::MCParticle::get_px(Muons_daughters)")
            .Define("Muons_daughters_py",   "FCCAnalyses::MCParticle::get_py(Muons_daughters)")
            .Define("Muons_daughters_pz",   "FCCAnalyses::MCParticle::get_pz(Muons_daughters)")

            .Define("Muons_daughters_e",    "sqrt(Muons_daughters_p*Muons_daughters_p + Muons_daughters_mass*Muons_daughters_mass)")

            #Need sum to get the invariant mass of the Higgs candidate
            .Define("Muon_Total_e",         "ROOT::VecOps::Sum(Muons_daughters_e)")
            .Define("Muon_Total_px",        "ROOT::VecOps::Sum(Muons_daughters_px)")
            .Define("Muon_Total_py",        "ROOT::VecOps::Sum(Muons_daughters_py)")
            .Define("Muon_Total_pz",        "ROOT::VecOps::Sum(Muons_daughters_pz)")

            .Define('Muon_Total_e_size',    'Muons_daughters_e.size()')

            .Define("Muons_daughters_InvM", "sqrt(Muon_Total_e*Muon_Total_e - Muon_Total_px*Muon_Total_px - Muon_Total_py*Muon_Total_py - Muon_Total_pz*Muon_Total_pz)")
            
            .Define("Muons_daughters_x", "if (n_Muons_daughters>0) return FCCAnalyses::MCParticle::get_vertex_x(Muons_daughters); else return FCCAnalyses::MCParticle::get_genStatus(Muons_daughters);")
            .Define("Muons_daughters_y", "if (n_Muons_daughters>0) return FCCAnalyses::MCParticle::get_vertex_y(Muons_daughters); else return FCCAnalyses::MCParticle::get_genStatus(Muons_daughters);")
            .Define("Muons_daughters_z", "if (n_Muons_daughters>0) return FCCAnalyses::MCParticle::get_vertex_z(Muons_daughters); else return FCCAnalyses::MCParticle::get_genStatus(Muons_daughters);")
           
            .Define("Muons_daughters_Lxy",   "return sqrt(Muons_daughters_x*Muons_daughters_x + Muons_daughters_y*Muons_daughters_y)")
            .Define("Muons_daughters_Lxyz",  "return sqrt(Muons_daughters_x*Muons_daughters_x + Muons_daughters_y*Muons_daughters_y + Muons_daughters_z*Muons_daughters_z)")

#---------- Generated Z_D Sons ------------------------------------------------------------------------------------------------------------------------------------------------------

            #Get collection of indices of the dark photons that come from the Higgs boson (including the Higgs boson itself)
            .Define("Sons_indices",         "FCCAnalyses::MCParticle::get_indices(25, {1023, -1023}, false, true, true, true)(Particle, Particle1)")
            .Define("Sons_size",            "Sons_indices.size()")
            .Define("Sons",                 "ROOT::VecOps::Take(Particle, Sons_indices)")
            .Define("SonsPDG",              'FCCAnalyses::MCParticle::get_pdg(Sons)')
            
             #Extract Higgs parent from the index collection
            .Define("Higgs_dad",            "FCCAnalyses::MCParticle::sel_pdgID(25, true)(Sons)")
            .Define("n_Higgs_dad",          "Higgs_dad.size()")
            .Define("Higgs_dad_mass",       "FCCAnalyses::MCParticle::get_mass(Higgs_dad)")

             #Extract dark photons Sons from the index collection
            .Define("Z_sons",               "FCCAnalyses::MCParticle::sel_pdgID(1023, true)(Sons)")
            .Define("n_Z_sons",             "Z_sons.size()")
            .Define("Z_sons_mass",          "FCCAnalyses::MCParticle::get_mass(Z_sons)")

            .Define("Z_sons_e",             "FCCAnalyses::MCParticle::get_e(Z_sons)")
            .Define("Z_sons_p",             "FCCAnalyses::MCParticle::get_p(Z_sons)")
            .Define("Z_sons_px",            "FCCAnalyses::MCParticle::get_px(Z_sons)")
            .Define("Z_sons_py",            "FCCAnalyses::MCParticle::get_py(Z_sons)")
            .Define("Z_sons_pz",            "FCCAnalyses::MCParticle::get_pz(Z_sons)")

            .Define("Z_sons_InvM",          "sqrt(Z_sons_e*Z_sons_e - Z_sons_px*Z_sons_px - Z_sons_py*Z_sons_py - Z_sons_pz*Z_sons_pz)")

            .Define("mu_e_indices",        "FCCAnalyses::MCParticle::get_indices(25, {13, -13, 11, -11}, true, true, true, true)(Particle, Particle1)")
            .Define("mu_tau_indices",      "FCCAnalyses::MCParticle::get_indices(25, {13, -13, 15, -15}, true, true, true, true)(Particle, Particle1)")
            .Define("e_mu_indices",        "FCCAnalyses::MCParticle::get_indices(25, {11, -11, 13, -13}, true, true, true, true)(Particle, Particle1)")
            .Define("e_tau_indices",       "FCCAnalyses::MCParticle::get_indices(25, {11, -11, 15, -15}, true, true, true, true)(Particle, Particle1)")
            .Define("e_e_indices",         "FCCAnalyses::MCParticle::get_indices(25, {11, -11, 11, -11}, true, true, true, true)(Particle, Particle1)")
            .Define("tau_mu_indices",      "FCCAnalyses::MCParticle::get_indices(25, {15, -15, 13, -13}, true, true, true, true)(Particle, Particle1)")
            .Define("tau_tau_indices",     "FCCAnalyses::MCParticle::get_indices(25, {15, -15, 15, -15}, true, true, true, true)(Particle, Particle1)")
            .Define("tau_e_indices",       "FCCAnalyses::MCParticle::get_indices(25, {15, -15, 11, -11}, true, true, true, true)(Particle, Particle1)")

            .Define("All_lepton_Indices", 
                """
                ROOT::VecOps::RVec<int> res;
                res = ROOT::VecOps::Concatenate(mu_e_indices, mu_tau_indices);
                res = ROOT::VecOps::Concatenate(res, e_mu_indices);
                res = ROOT::VecOps::Concatenate(res, e_tau_indices);
                res = ROOT::VecOps::Concatenate(res, e_e_indices);
                res = ROOT::VecOps::Concatenate(res, tau_mu_indices);
                res = ROOT::VecOps::Concatenate(res, tau_tau_indices);
                res = ROOT::VecOps::Concatenate(res, tau_e_indices);
                res = ROOT::VecOps::Concatenate(res, Daughters_indices);
                
                // Use standard C++ to unique the collection
                std::sort(res.begin(), res.end());
                res.erase(std::unique(res.begin(), res.end()), res.end());
                
                return res;
                """)

#---------- Generated Z ------------------------------------------------------------------------------------------------------------------------------------------------------

            .Define("GenZ_PID",           "FCCAnalyses::MCParticle::sel_pdgID(23, true)(Particle)") #Keep particle only if its a Z boson
            .Define("n_gen_Z",            "GenZ_PID.size()")
            .Define("GenZ_e",             "if (n_gen_Z>0) return FCCAnalyses::MCParticle::get_e(GenZ_PID); else return FCCAnalyses::MCParticle::get_genStatus(GenZ_PID);")
            .Define("GenZ_px",            "if (n_gen_Z>0) return FCCAnalyses::MCParticle::get_px(GenZ_PID); else return FCCAnalyses::MCParticle::get_genStatus(GenZ_PID);")
            .Define("GenZ_py",            "if (n_gen_Z>0) return FCCAnalyses::MCParticle::get_py(GenZ_PID); else return FCCAnalyses::MCParticle::get_genStatus(GenZ_PID);")
            .Define("GenZ_pz",            "if (n_gen_Z>0) return FCCAnalyses::MCParticle::get_pz(GenZ_PID); else return FCCAnalyses::MCParticle::get_genStatus(GenZ_PID);")
            .Define("GenZ_InvM",          "if (n_gen_Z>0) return FCCAnalyses::MCParticle::get_mass(GenZ_PID); else return FCCAnalyses::MCParticle::get_genStatus(GenZ_PID);")
            
#---------- Generated Jets ------------------------------------------------------------------------------------------------------------------------------------------------------
            
            .Filter("All_lepton_Indices.size() > 0")
            .Define("All_Indices", "ROOT::VecOps::RVec<int> indices(Particle.size()); std::iota(indices.begin(), indices.end(), 0); return indices;")

            #Function to create collection with all the indices that are not used for particles within the Higgs decay into leptons. All the remaining indices should be those of particles coming from the jets
            .Define("is_not_higgs_mask", 
                """
                ROOT::VecOps::RVec<int> mask;
                for (int i : All_Indices) {
                    bool found = false;
                    for (int j : All_lepton_Indices) {
                        if (i == j) { found = true; break; }
                    }
                    mask.push_back(!found);
                }
                return mask;
                """)

            .Define("Jets",             "Particle[is_not_higgs_mask]")
            .Define("Jet_Particles",    "FCCAnalyses::MCParticle::sel_genStatus(1)(Jets)") #Get the final state jet particle
            .Define("n_genJet",         "Jet_Particles.size()")

            .Define("Jet_e",            "FCCAnalyses::MCParticle::get_e(Jet_Particles)")
            .Define("Jet_p",            "FCCAnalyses::MCParticle::get_p(Jet_Particles)")
            .Define("Jet_px",           "FCCAnalyses::MCParticle::get_px(Jet_Particles)")
            .Define("Jet_py",           "FCCAnalyses::MCParticle::get_py(Jet_Particles)")
            .Define("Jet_pz",           "FCCAnalyses::MCParticle::get_pz(Jet_Particles)")

            .Define("Jet_e_tot",        "ROOT::VecOps::Sum(Jet_e)")
            .Define("Jet_p_tot",        "ROOT::VecOps::Sum(Jet_p)")
            .Define("Jet_px_tot",       "ROOT::VecOps::Sum(Jet_px)")
            .Define("Jet_py_tot",       "ROOT::VecOps::Sum(Jet_py)")
            .Define("Jet_pz_tot",       "ROOT::VecOps::Sum(Jet_pz)")

            .Define("Jet_InvM",         "sqrt(Jet_e_tot*Jet_e_tot - Jet_px_tot*Jet_px_tot - Jet_py_tot*Jet_py_tot - Jet_pz_tot*Jet_pz_tot)")
        )
        return dframe2

    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            'FSGenMuon_pt',
            'FSGenMuon_eta',
            'FSGenMuon_phi',
            'n_FSGenMuon',
            'FSGen_Lxyz',
            'Muons_daughters_Lxyz',
            'GenZ_InvM',
            'Jet_InvM',
            'Muons_daughters_InvM',
        ]
        return branch_list