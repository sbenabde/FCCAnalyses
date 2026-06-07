import ROOT

#inputDir = "STAGE1_output"  #Local
inputDir = "/eos/experiment/fcc/ee/analyses_storage/BSM/LLPs/DarkPhotons/Stage1_output_backgrounds/" #Central
outputDir = "/eos/experiment/fcc/ee/analyses_storage/BSM/LLPs/DarkPhotons/Final_output_background_test"
# outputDir = "/eos/user/s/sbenabde/FCCAnalyses/examples/FCCee/bsm/LLPs/DarkPhotons/FINAL_output/submission/wzp6_ee_qqH_HZZ_llll_ecm240"


processList = {
        'dark_photons_mZd360MeV_e_1e-5':{},
        'dark_photons_mZd1100MeV_e_3.12e-6':{},
        'dark_photons_mZd7000MeV_e_2.7e-7':{},

        #Background

        # #Local
        # 'bkg_ee_qqH_HZZ_4l':{},
        # 'bkg_ee_qqH_HZZ_4mu':{},

        #Central
        #'wzp6_ee_qqH_HZZ_ecm240':{},
 
        #'wzp6_ee_bbH_HZZ_ecm240':{},
        #'wzp6_ee_qqH_ecm240':{},

        #'wzp6_ee_mumuH_Hmumu_ecm240':{},

        #'wzp6_ee_qqH_Hmumu_ecm240':{},
        #'wzp6_ee_ccH_Hmumu_ecm240':{},
        #'wzp6_ee_bbH_Hmumu_ecm240':{},

        'wzp6_ee_qqH_HZZ_llll_ecm240':{},

        #'wzp6_ee_qqH_HWW_ecm240':{},
        #'wzp6_ee_ccH_HWW_ecm240':{},
        #'wzp6_ee_bbH_HWW_ecm240':{},

        #'wzp6_ee_mumuH_Hbb_ecm240':{},
        
        'p8_ee_ZZ_ecm240':{},
        'p8_ee_WW_ecm240':{},

}

#Need this block to add the cross sections of the self generated samples, otherwise it sets to 1.0 pb
procDictAdd = {
    'dark_photons_mZd360MeV_e_1e-5': {"crossSection": 2.543e-06, "scaleFactor": 1.7230473095e+00, "scaleFactorHiggs": 3.6781582138e+00},
    'dark_photons_mZd1100MeV_e_3.12e-6': {"crossSection": 2.816e-06, "scaleFactor": 1.2877751407e+00, "scaleFactorHiggs": 3.6796835472e+00},
    'dark_photons_mZd7000MeV_e_2.7e-7': {"crossSection": 1.116e-06, "scaleFactor": 8.8012055817e-01, "scaleFactorHiggs": 3.7475022897e+00},
}


#Link to the dictionary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Expected integrated luminosity
intLumi = 10.8e+06  #pb-1

#Whether to scale to expected integrated luminosity
doScale = True

#Number of threads to use
nCPUS = 4

#Whether to produce ROOT TTrees, default is False
doHistos = True

#Save cut yields and efficiencies in LaTeX table
saveTabular = True

# Save cut yields and efficiencies in JSON file
saveJSON = True


cuts = ['(n_zjj >= 2)', 
        '(All(zjj_pt >= 0))',
        '(n_RecoMuons >= 4)',
        '(Sum(RecoMuon_charge > 0) >= 2 && Sum(RecoMuon_charge < 0) >= 2)',
        '(MuonPairs_InvMass > 120 && MuonPairs_InvMass < 130)',
        '(MuonPair1_total_InvMass < 11 && MuonPair2_total_InvMass < 11)',
        'All((DV_lxyz > 3))',
]

#Dictionary with the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    "selNone": "n_zjj >= 0",
   
    #For event selection
    "2_jets":         f'{cuts[0]}',
    "pt":             f'{cuts[0]} && {cuts[1]}',
    "4_muons":        f'{cuts[0]} && {cuts[1]} && {cuts[2]}',
    "4OS_muons":      f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[3]}',

    "Preselection":   f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[3]}',
    
    "4mu_InvM":       f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[3]} && {cuts[4]}',
    "Leptonic_InvM":  f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[3]} && {cuts[4]} && {cuts[5]}',
    "DV_lxyz":        f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[3]} && {cuts[4]} && {cuts[5]} && {cuts[6]}',
    "Total_Selection":f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[3]} && {cuts[4]} && {cuts[5]} && {cuts[6]}',

}

cutLabels = {
    "selNone": "Before selection",
    #For event selection
    "2_jets" :          r"n_zjj >= 2",
    "4_muons" :         r"n_RecoMu >= 4",
    "4OS_muons" :       r"Opposite charge muons",

    "Preselection":     r"Preselection",

    "4mu_InvM" :        r"120 < M_{4\mu} < 130 GeV",
    "Leptonic_InvM" :   r"M_{2\mu} < 11 GeV",
    "DV_lxyz" :         r"L_{xyz} > 3 mm",
    "Total_Selection" : r"Total Selection",
    }

# Dictionary for the output variables/histograms. 
#The key is the name of the variable in the output files. 
#"name" is the name of the variable in the input file
#"title" is the x-axis label of the histogram
#"bin" the number of bins of the histogram
#"xmin" the minimum x-axis value and "xmax" the maximum x-axis value.


histoList = {   
    'n_RecoMuons':                          {"name":'n_RecoMuons',               "title": "Number of reco. muons",            "bin":10,  "xmin":-0.5, "xmax":9.5},
    'RecoMuon_pt':                          {"name":'RecoMuon_pt',               "title": "Reco muons p_{T} [GeV]",           "bin":50, "xmin":0,    "xmax":150},
    'Selected_muons_pt':                    {"name":'Selected_muons_pt',         "title": "Selected 4#mu p_{T} [GeV]",        "bin":50, "xmin":0,    "xmax":100},
    'Selected_muons_eta':                   {"name":'Selected_muons_eta',        "title": "Selected 4#mu #eta",               "bin":50, "xmin":-3,   "xmax":3},
    
    'n_zjj':                                {"name":'n_zjj',                     "title": "Number of reco. jets",             "bin":20,  "xmin":-0.5, "xmax":19.5},       
    'zjj_invMass':                          {"name":'zjj_invMass',               "title": "M_{jj} [GeV]",                     "bin":50, "xmin":50,   "xmax":150},     
    'zjj_pt':                               {"name":'zjj_pt',                    "title": "Jets p_{T} [GeV]",                 "bin":50, "xmin":0,    "xmax":120},    
    'zjj_leading_pt':                       {"name":'zjj_leading_pt',            "title": "Leading jet p_{T} [GeV]",          "bin":50, "xmin":0,    "xmax":120},    
    'zjj_subleading_pt':                    {"name":'zjj_subleading_pt',         "title": "Subleading jet p_{T} [GeV]",       "bin":50, "xmin":0,    "xmax":120},    

    "MuonPairs_InvMass":                    {"name":'MuonPairs_InvMass',         "title": "M_{4#mu} [GeV]",                   "bin":50, "xmin":115,  "xmax":135},            
    "MuonPairs_InvMass_long_range":         {"name":'MuonPairs_InvMass',         "title": "M_{4#mu} [GeV]",                   "bin":50, "xmin":0,    "xmax":135},            
    "MuonPair1_total_InvMass":              {"name":'MuonPair1_total_InvMass',   "title": "M_{#mu_{1}#mu_{2}} [GeV]",         "bin":50, "xmin":0.5,  "xmax":11.5},  
    "MuonPair1_total_InvMass_long_range":   {"name":'MuonPair1_total_InvMass',   "title": "M_{#mu_{1}#mu_{2}} [GeV]",         "bin":50, "xmin":0,    "xmax":110},  
    "MuonPair2_total_InvMass":              {"name":'MuonPair2_total_InvMass',   "title": "M_{#mu_{3}#mu_{4}} [GeV]",         "bin":50, "xmin":0.5,  "xmax":11.5},  
    "MuonPair2_total_InvMass_long_range":   {"name":'MuonPair2_total_InvMass',   "title": "M_{#mu_{3}#mu_{4}} [GeV]",         "bin":50, "xmin":0,    "xmax":110},  
 
    "MuonPair1_dR":                         {"name":'MuonPair1_dR',              "title": "Pair1 dR",                         "bin":30, "xmin":0,    "xmax":1},  
    "MuonPair2_dR":                         {"name":'MuonPair2_dR',              "title": "Pair2 dR",                         "bin":30, "xmin":0,    "xmax":1.5},  
        
    "DV1_Lxyz":                             {"name":'DV1_Lxyz',                  "title": "L_{xyz} DV_1 [mm]",                "bin":50, "xmin":0,     "xmax":800},  
    "DV2_Lxyz":                             {"name":'DV2_Lxyz',                  "title": "L_{xyz} DV_2 [mm]",                "bin":50, "xmin":0,     "xmax":800},  
    "DV_lxyz":                              {"name":'DV_lxyz',                   "title": "L_{xyz} [mm]",                     "bin":50, "xmin":0.1,   "xmax":800},  
    "DV_lxyz_short":                        {"name":'DV_lxyz',                   "title": "L_{xyz} [mm]",                     "bin":50, "xmin":0.01,  "xmax":10},  
    "n_DVs":                                {"name":'n_DVs',                     "title": "n_DVs",                            "bin":50, "xmin":0.5,   "xmax":3.5},  
}