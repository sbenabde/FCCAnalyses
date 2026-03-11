from argparse import ArgumentParser
import ROOT

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
        self.input_dir = '/eos/experiment/fcc/ee/analyses_storage/BSM/LLPs/DarkPhotons'
        self.output_dir = "STAGE1_output"
        
        self.analysis_name = 'My Analysis'
        self.n_threads = 1


    def analyzers(self, dframe):

        TTree_Branch_Name_parents = '_Particle_parents'
        TTree_Branch_Name_daughters = '_Particle_daughters'
        TTree_Muon_Name = 'Muon_objIdx'
        TTree_EflowTrack_Name = '_EFlowTrack_trackStates'
            
        dframe2 = (
            dframe
            .Alias("Particle0", f"{TTree_Branch_Name_parents}.index")
            .Alias("Particle1", f"{TTree_Branch_Name_daughters}.index")
            .Alias('Muon0', f"{TTree_Muon_Name}.index")
            .Alias('EFlowTracks', f"{TTree_EflowTrack_Name}")

#---------- Generated muons ------------------------------------------------------------------------------------------------------------------------------------------------------
            .Define("GenMuon_PID",        "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)") #Keep particle only if its a muon
            .Define("FSGenMuon",          "FCCAnalyses::MCParticle::sel_genStatus(1)(GenMuon_PID)") #Keep muon only if its final state (FS)
            
            .Define("MC_PDG",             "FCCAnalyses::MCParticle::get_pdg(FSGenMuon)")            #Gets PDGID of particle collection in bracket
            .Define("MC_n",               "int(MC_PDG.size())")
            .Define("MC_M1_idx",          "myUtils::get_MCMother1(FSGenMuon, Particle0)")
            .Define("MC_M1_part",         "ROOT::VecOps::Take(Particle, MC_M1_idx)")                #mother particles
            .Define("MC_M1_pdg",          "FCCAnalyses::MCParticle::get_pdg(MC_M1_part)")

            .Define("n_FSGenMuon",        "FCCAnalyses::MCParticle::get_n(FSGenMuon)")              #Get number of final state generated muons
            .Define("FSGenMuon_e",        "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_e(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_p",        "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_p(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")

            .Define("FSGenMuon_pt",       "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_pt(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_px",       "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_px(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_py",       "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_py(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_pz",       "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_pz(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_eta",      "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_eta(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_theta",    "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_theta(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_phi",      "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_phi(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_charge",   "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_charge(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
        
            .Define("FSGenMuon_vertex_x", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_vertex_x(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_vertex_y", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_vertex_y(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_vertex_z", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_vertex_z(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
           
            .Define("FSGen_Lxy",   "return sqrt(FSGenMuon_vertex_x*FSGenMuon_vertex_x + FSGenMuon_vertex_y*FSGenMuon_vertex_y)")
            .Define("FSGen_Lxyz",  "return sqrt(FSGenMuon_vertex_x*FSGenMuon_vertex_x + FSGenMuon_vertex_y*FSGenMuon_vertex_y + FSGenMuon_vertex_z*FSGenMuon_vertex_z)")
            
   
#---------- Reconstructed muons ------------------------------------------------------------------------------------------------------------------------------------------------------

            .Define("RecoMuons",        "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
            .Define("n_RecoMuons",      "ReconstructedParticle::get_n(RecoMuons)")                                   

            .Define("RecoMuon_e",       "ReconstructedParticle::get_e(RecoMuons)")
            .Define("RecoMuon_p",       "ReconstructedParticle::get_p(RecoMuons)")
            .Define("RecoMuon_pt",      "ReconstructedParticle::get_pt(RecoMuons)")
            .Define("RecoMuon_px",      "ReconstructedParticle::get_px(RecoMuons)")
            .Define("RecoMuon_py",      "ReconstructedParticle::get_py(RecoMuons)")
            .Define("RecoMuon_pz",      "ReconstructedParticle::get_pz(RecoMuons)")
		    .Define("RecoMuon_eta",     "ReconstructedParticle::get_eta(RecoMuons)")
            .Define("RecoMuon_theta",   "ReconstructedParticle::get_theta(RecoMuons)")
		    .Define("RecoMuon_phi",     "ReconstructedParticle::get_phi(RecoMuons)")
            .Define("RecoMuon_charge",  "ReconstructedParticle::get_charge(RecoMuons)")

             #Muon pairs for Dark photon reconstruction           
            .Define('PairedMuons', 'get_best_paired_indices(RecoMuon_eta, RecoMuon_phi, RecoMuon_charge)')
            .Define('Pair1', 'PairedMuons.size() > 0 ? PairedMuons[0]:std::vector<int> {-1, -1}')
            .Define('Pair2', 'PairedMuons.size() > 1 ? PairedMuons[1]:std::vector<int> {-1, -1}')

            .Define("MuonPair1",              "ReconstructedParticle::get(Pair1, RecoMuons)")

            .Define("MuonPair1_e",             "ReconstructedParticle::get_e(MuonPair1)")
            .Define("MuonPair1_total_e",       "ROOT::VecOps::Sum(MuonPair1_e)")
            .Define("MuonPair1_pt",            "ReconstructedParticle::get_pt(MuonPair1)")
            .Define("MuonPair1_total_pt",      "ROOT::VecOps::Sum(MuonPair1_pt)")
            .Define("MuonPair1_px",            "ReconstructedParticle::get_px(MuonPair1)")
            .Define("MuonPair1_total_px",      "ROOT::VecOps::Sum(MuonPair1_px)")
            .Define("MuonPair1_py",            "ReconstructedParticle::get_py(MuonPair1)")
            .Define("MuonPair1_total_py",      "ROOT::VecOps::Sum(MuonPair1_py)")
            .Define("MuonPair1_pz",            "ReconstructedParticle::get_pz(MuonPair1)")
            .Define("MuonPair1_total_pz",      "ROOT::VecOps::Sum(MuonPair1_pz)")
            .Define("MuonPair1_charge",        "ReconstructedParticle::get_charge(MuonPair1)")
            .Define("MuonPair1_total_charge",  "ROOT::VecOps::Sum(MuonPair1_charge)")
            .Define("MuonPair1_InvMass",       "sqrt(MuonPair1_e*MuonPair1_e - MuonPair1_px*MuonPair1_px - MuonPair1_py*MuonPair1_py - MuonPair1_pz*MuonPair1_pz)")
            .Define("MuonPair1_total_InvMass", "sqrt(MuonPair1_total_e*MuonPair1_total_e - MuonPair1_total_px*MuonPair1_total_px - MuonPair1_total_py*MuonPair1_total_py - MuonPair1_total_pz*MuonPair1_total_pz)")
            .Define("MuonPair1_dR",            "get_pair_dR(Pair1, RecoMuon_eta, RecoMuon_phi)")    
            
            .Define("MuonPair2",               "ReconstructedParticle::get(Pair2, RecoMuons)")

            .Define("MuonPair2_e",             "ReconstructedParticle::get_e(MuonPair2)")
            .Define("MuonPair2_total_e",       "ROOT::VecOps::Sum(MuonPair2_e)")
            .Define("MuonPair2_pt",            "ReconstructedParticle::get_pt(MuonPair2)")
            .Define("MuonPair2_total_pt",      "ROOT::VecOps::Sum(MuonPair2_pt)")
            .Define("MuonPair2_px",            "ReconstructedParticle::get_px(MuonPair2)")
            .Define("MuonPair2_total_px",      "ROOT::VecOps::Sum(MuonPair2_px)")
            .Define("MuonPair2_py",            "ReconstructedParticle::get_py(MuonPair2)")
            .Define("MuonPair2_total_py",      "ROOT::VecOps::Sum(MuonPair2_py)")
            .Define("MuonPair2_pz",            "ReconstructedParticle::get_pz(MuonPair2)")
            .Define("MuonPair2_total_pz",      "ROOT::VecOps::Sum(MuonPair2_pz)")
            .Define("MuonPair2_charge",        "ReconstructedParticle::get_charge(MuonPair2)")
            .Define("MuonPair2_total_charge",  "ROOT::VecOps::Sum(MuonPair2_charge)")
            .Define("MuonPair2_InvMass",       "sqrt(MuonPair2_e*MuonPair2_e - MuonPair2_px*MuonPair2_px - MuonPair2_py*MuonPair2_py - MuonPair2_pz*MuonPair2_pz)")
            .Define("MuonPair2_total_InvMass", "sqrt(MuonPair2_total_e*MuonPair2_total_e - MuonPair2_total_px*MuonPair2_total_px - MuonPair2_total_py*MuonPair2_total_py - MuonPair2_total_pz*MuonPair2_total_pz)")
            .Define("MuonPair2_dR",            "get_pair_dR(Pair2, RecoMuon_eta, RecoMuon_phi)")    

            #4 selected muons (pair1 + pair2)
            .Define("MuonPairs_e",             "ROOT::VecOps::Sum(MuonPair1_e) + ROOT::VecOps::Sum(MuonPair2_e)")
            .Define("MuonPairs_px",            "ROOT::VecOps::Sum(MuonPair1_px) + ROOT::VecOps::Sum(MuonPair2_px)")
            .Define("MuonPairs_py",            "ROOT::VecOps::Sum(MuonPair1_py) + ROOT::VecOps::Sum(MuonPair2_py)")
            .Define("MuonPairs_pz",            "ROOT::VecOps::Sum(MuonPair1_pz) + ROOT::VecOps::Sum(MuonPair2_pz)")
            .Define("MuonPairs_charge",        "ROOT::VecOps::Sum(MuonPair1_charge) + ROOT::VecOps::Sum(MuonPair2_charge)")

            .Define("MuonPairs_InvMass", "sqrt(MuonPairs_e*MuonPairs_e - MuonPairs_px*MuonPairs_px - MuonPairs_py*MuonPairs_py - MuonPairs_pz*MuonPairs_pz)")

            .Define("Selected_muons",   "ReconstructedParticle::merge(MuonPair1, MuonPair2)")
            .Define("N_Selected_muons", "int(Selected_muons.size())")



#---------- Vertexing  ------------------------------------------------------------------------------------------------------------------------------------------------------


            # MC event primary vertex
            .Define("MC_PrimaryVertex",     "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)(Particle)" ) #21 is the PDG ID of the collision point, at coo (0,0,0)
            .Define("n_tracks",             "ReconstructedParticle2Track::getTK_n(EFlowTracks)")    #number of tracks

            #First, reconstruct a vertex from all tracks 
            #Input parameters are 1 = primary vertex, EFlowTracks contains all tracks, bool beamspotconstraint = true, bsc sigma x/y/z
            .Define("VertexObject_allTracks", "VertexFitterSimple::VertexFitter_Tk(1, EFlowTracks, true, 4.5, 20e-3, 300)")
            .Define("RecoedPrimaryTracks",    "VertexFitterSimple::get_PrimaryTracks(EFlowTracks, true, 4.5, 20e-3, 300, 0., 0., 0.)")  #Select the tracks that are reconstructed  as primaries
            .Define("n_RecoedPrimaryTracks",  "ReconstructedParticle2Track::getTK_n(RecoedPrimaryTracks)") #Number of reconstructed primary tracks
            .Define("PrimaryVertexObject",    "VertexFitterSimple::VertexFitter_Tk(1, RecoedPrimaryTracks, true, 4.5, 20e-3, 300) ")  #The final primary vertex
            .Define("PrimaryVertex",          "VertexingUtils::get_VertexData(PrimaryVertexObject)")


            #Muon Pairs Vertexing
            .Define("MuonPair1_tracks",         "ReconstructedParticle2Track::getRP2TRK(MuonPair1, EFlowTracks)")
            .Define("MuonPair2_tracks",         "ReconstructedParticle2Track::getRP2TRK(MuonPair2, EFlowTracks)")

            .Define("DV1_VertexObject",         "if(MuonPair1_tracks.size() >= 2) return VertexFitterSimple::VertexFitter_Tk(MuonPair1_tracks.size(), MuonPair1_tracks); else return VertexingUtils::FCCAnalysesVertex();")
            .Define("DV2_VertexObject",         "if(MuonPair2_tracks.size() >= 2) return VertexFitterSimple::VertexFitter_Tk(MuonPair2_tracks.size(), MuonPair2_tracks); else return VertexingUtils::FCCAnalysesVertex();")
            
            .Define("DV1_VertexData",           "VertexingUtils::get_VertexData(DV1_VertexObject)")
            .Define("DV2_VertexData",           "VertexingUtils::get_VertexData(DV2_VertexObject)")

            .Define("DV1_chi2",                 "DV1_VertexData.chi2")
            .Define("DV2_chi2",                 "DV2_VertexData.chi2")
            
            .Define("DV1_Lxyz",                 "sqrt(pow(DV1_VertexData.position[0],2) + pow(DV1_VertexData.position[1],2) + pow(DV1_VertexData.position[2],2))")
            .Define("DV2_Lxyz",                 "sqrt(pow(DV2_VertexData.position[0],2) + pow(DV2_VertexData.position[1],2) + pow(DV2_VertexData.position[2],2))")
            
            .Define("DV1_invM",                 "VertexingUtils::get_invM_pairs(DV1_VertexObject, 0.105658, 0.105658)")
            .Define("DV2_invM",                 "VertexingUtils::get_invM_pairs(DV2_VertexObject, 0.105658, 0.105658)")
          
            .Define("n_DVs",                    "VertexingUtils::get_VertexNtrk(DV1_VertexObject)")
        

            #Reco Muons vertexing            
            .Define("RecoMuons_tracks",             "ReconstructedParticle2Track::getRP2TRK(RecoMuons, EFlowTracks)")
            .Define("RecoMuons_VertexObject",       "if(RecoMuons_tracks.size() >= 2) return VertexFitterSimple::VertexFitter_Tk(RecoMuons_tracks.size(), RecoMuons_tracks); else return VertexingUtils::FCCAnalysesVertex();")
            .Define("RecoMuons_VertexData",         "VertexingUtils::get_VertexData(RecoMuons_VertexObject)")
            .Define("RecoMuons_chi2",               "RecoMuons_VertexData.chi2")
            .Define("RecoMuons_Lxyz",               "sqrt(pow(RecoMuons_VertexData.position[0],2) + pow(RecoMuons_VertexData.position[1],2) + pow(RecoMuons_VertexData.position[2],2))")
            
            .Define("n_GlobalDVs",                  "int(RecoMuons_chi2 >= 0)")
            # .Define("Global_mass",                  "if(RecoMuons.size() >= 2) return ReconstructedParticle::get_invariant_mass(RecoMuons); else return -1.0;")

#---------- Jet Reconstruction ------------------------------------------------------------------------------------------------------------------------------------------------------
            
            .Define("RP_noMu", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, RecoMuons)") #Particle collection without muons

            .Define("pseudo_jets_noMu", #Jet clustering
                    "FCCAnalyses::JetClusteringUtils::set_pseudoJets("
                    "ReconstructedParticle::get_px(RP_noMu),"
                    "ReconstructedParticle::get_py(RP_noMu),"
                    "ReconstructedParticle::get_pz(RP_noMu),"
                    "ReconstructedParticle::get_e (RP_noMu))")      

            #ee_kt (Durham): clustering_ee_kt(exclusive (jet #), cut (same as exclusive if > 0), (0=sort by pT, 1=sort by E), recombination=0)
            .Define("clustered_durham2_noMu", "JetClustering::clustering_ee_kt(2, 2, 0, 0)(pseudo_jets_noMu)")
            .Define("jets_durham2_noMu",      "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_durham2_noMu)")

            #All jets (actually there are only 2 so this is leading and subleading together)
            .Define("zjj_e",  "FCCAnalyses::JetClusteringUtils::get_e (jets_durham2_noMu)")
            .Define("zjj_px", "FCCAnalyses::JetClusteringUtils::get_px(jets_durham2_noMu)")
            .Define("zjj_py", "FCCAnalyses::JetClusteringUtils::get_py(jets_durham2_noMu)")
            .Define("zjj_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets_durham2_noMu)")
            .Define("zjj_pt", "return sqrt(zjj_px*zjj_px + zjj_py*zjj_py);")
            
            .Define("n_zjj",  "int(zjj_e.size())")

            .Define("zjj_leading_pt",    "return float(zjj_pt.at(0))")
            .Define("zjj_subleading_pt", "return float(zjj_pt.at(1))")
            
            .Define("zjj_e_sum",  "if (n_zjj>1) return float(zjj_e.at(0)  + zjj_e.at(1));  else return float(-1.);")
            .Define("zjj_px_sum", "if (n_zjj>1) return float(zjj_px.at(0) + zjj_px.at(1)); else return float(-1.);")
            .Define("zjj_py_sum", "if (n_zjj>1) return float(zjj_py.at(0) + zjj_py.at(1)); else return float(-1.);")
            .Define("zjj_pz_sum", "if (n_zjj>1) return float(zjj_pz.at(0) + zjj_pz.at(1)); else return float(-1.);")
            .Define("zjj_pt_sum", "if (n_zjj>1) return float(sqrt((zjj_px_sum*zjj_px_sum) + (zjj_py_sum*zjj_py_sum))); else return float(-1.);")           

            .Define("zjj_invMass",
                    "if (n_zjj>1) return float(sqrt(zjj_e_sum*zjj_e_sum"
                    " - zjj_px_sum*zjj_px_sum - zjj_py_sum*zjj_py_sum - zjj_pz_sum*zjj_pz_sum));"
                    " else return float(-1.);")
        )
        return dframe2

    #Mandatory: output function, please make sure you return the branch list as a python list
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            # #Gen Muons
            # "n_FSGenMuon",
            # "FSGenMuon_e",
            # "FSGenMuon_p",
            # "FSGenMuon_pt",
            # "FSGenMuon_px",
            # "FSGenMuon_py",
            # "FSGenMuon_pz",
            # "FSGenMuon_eta",
            # "FSGenMuon_theta",
            # "FSGenMuon_phi",
            # "FSGenMuon_charge",
            # "FSGen_Lxy",
            # "FSGen_Lxyz",
            # "MC_n",
            # "MC_PDG",
            # "MC_M1_idx",
            # "MC_M1_part",
            # "MC_M1_pdg",

            #Reco Muons
            "n_RecoMuons",
            'RecoMuon_pt',
            'RecoMuon_eta',
            'RecoMuon_p',
            'RecoMuon_e',
            'RecoMuon_px', 
            'RecoMuon_py', 
            'RecoMuon_pz',
            'RecoMuon_theta',
            'RecoMuon_phi',
            'RecoMuon_charge',

            'MuonPair1_charge',
            'MuonPair2_charge',
            'MuonPair1_InvMass',
            'MuonPair2_InvMass',
            "MuonPairs_charge",
            "MuonPairs_InvMass",
            "MuonPair1_dR",
            "MuonPair2_dR",

            'MuonPair1_total_charge',
            'MuonPair1_total_InvMass',
            'MuonPair2_total_charge',
            'MuonPair2_total_InvMass',        

            #Reco Jets
            'n_zjj',
            'zjj_e',
            'zjj_pt',
            'zjj_px',
            'zjj_py',
            'zjj_pz',
            'zjj_invMass',
            'zjj_leading_pt',
            'zjj_subleading_pt',

            #Vertexing
            'n_DVs', 
            'DV1_Lxyz', 
            # 'DV2_Lxyz', 
            # 'DV1_invM',
            # 'DV2_invM',

            'RecoMuons_Lxyz',
            # 'n_GlobalDVs',

        ]
        return branch_list