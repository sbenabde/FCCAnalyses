import ROOT

#Input directory where the files produced in the pre-selection stages are
inputDir = "STAGE1_output"
#Output directory where the resulting files will be stored
outputDir = "FINAL_output"

#Run over the full statistics from stage1 input file
processList = {
        #Signal
        'dark_photons_mZd360MeV_e_1e-5':{},
        'dark_photons_mZd1100MeV_e_3.12e-6':{},
        'dark_photons_mZd7000MeV_e_2.7e-7':{},
        'bkg_ee_qqH_HZZ_llll':{},

        #Background
        # 'wzp6_ee_mumuH_Hmumu_ecm240':{},
        # 'wzp6_ee_qqH_Hmumu_ecm240':{},
        # 'wzp6_ee_ccH_Hmumu_ecm240':{},
        # 'wzp6_ee_bbH_Hmumu_ecm240':{},
        'wzp6_ee_qqH_HZZ_llll_ecm240':{},
        #'wzp6_ee_qqH_ecm240':{},
        # 'wzp6_ee_qqH_HWW_ecm240':{},
        # 'wzp6_ee_ccH_HWW_ecm240':{},
        # 'wzp6_ee_bbH_HWW_ecm240':{},
        # 'wzp6_ee_mumuH_Hbb_ecm240':{},
        
        #'wzp6_ee_bbH_HZZ_ecm240':{},

        #'p8_ee_ZZ_ecm240':{},
        #'p8_ee_WW_ecm240':{},
}

#Need this block to add the cross sections of the self generated samples, otherwise it sets to 1.0 pb
procDictAdd = {
    'dark_photons_mZd360MeV_e_1e-5':      {"crossSection": 2.543e-06},
    'dark_photons_mZd1100MeV_e_3.12e-6':  {"crossSection": 2.816e-06},
    'dark_photons_mZd7000MeV_e_2.7e-7':   {"crossSection": 1.116e-06},
    'bkg_ee_qqH_HZZ_llll':                {"crossSection": 3.78e-05},
}

processLabels = {
    # #signals
    'dark_photons_mZd360MeV_e_1e-5':     r"m$_{Z_D}$=360MeV, $\epsilon$=1*10$^{-5}$",
    'dark_photons_mZd1100MeV_e_3.12e-6': r"m$_{Z_D}$=1100MeV, $\epsilon$=3.12*10$^{-6}$",
    'dark_photons_mZd7000MeV_e_8.8e-7':  r"m$_{Z_D}$=7000MeV, $\epsilon$=8.8*10$^{-7}$",
    
    #Backgrounds
    'bkg_ee_qqH_HZZ_llll':            r"Z #\rightarrow qq, h #\rightarrow ZZ #\rightarrow llll",
    
    # 'wzp6_ee_qqH_Hmumu_ecm240':     r"Z #\rightarrow qq, h #\rightarrow #mu #mu",
    # 'wzp6_ee_ccH_Hmumu_ecm240':     r"Z #\rightarrow cc, h #\rightarrow #mu #mu",
    # 'wzp6_ee_bbH_Hmumu_ecm240':     r"Z #\rightarrow bb, h #\rightarrow #mu #mu",
    'wzp6_ee_qqH_HZZ_llll_ecm240':  r"Z #\rightarrow qq, h #\rightarrow ZZ #\rightarrow llll",
    # 'wzp6_ee_qqH_HWW_ecm240':       r"Z #\rightarrow qq, h #\rightarrow WW",
    # 'wzp6_ee_ccH_HWW_ecm240':       r"Z #\rightarrow cc, h #\rightarrow WW",
    # 'wzp6_ee_bbH_HWW_ecm240':       r"Z #\rightarrow bb, h #\rightarrow WW",
    # 'wzp6_ee_mumuH_Hbb_ecm240':     r"Z #\rightarrow #mu #mu, h #\rightarrow bb",
   
    #'wzp6_ee_bbH_HZZ_ecm240':       r"Z #\rightarrow bb, h #\rightarrow ZZ",
    #'wzp6_ee_qqH_ecm240':           r"ee #\rightarrow Zh, Z #\rightarrow qq"
    # 'p8_ee_ZZ_ecm240':              r"ee #\rightarrow ZZ",
    # 'p8_ee_WW_ecm240':              r"ee #\rightarrow WW",
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
saveJSON = False


cuts = ['(n_zjj >= 2)', 
        '(n_RecoMuons >= 4)',
        '(Sum(RecoMuon_charge > 0) >= 2 && Sum(RecoMuon_charge < 0) >= 2)',
        '(zjj_invMass > 70 && zjj_invMass < 110)',
        '(zjj_invMass > 75 && zjj_invMass < 105)',
        '(zjj_invMass > 80 && zjj_invMass < 100)',
        '(zjj_invMass > 85 && zjj_invMass < 95)',

]

#Dictionary with the list of cuts. The key is the name of the selection that will be added to the output file
#Try for presel exactly 2 jets
cutList = {
    "selNone": "n_zjj >= 0",
    #For event selection
    "Preselection": f'{cuts[0]} && {cuts[1]} && {cuts[2]}', 
    "2_jets": f'{cuts[0]}',
    "Z-mass": f'{cuts[0]} && {cuts[3]}',
    "Z-mass2": f'{cuts[0]} && {cuts[4]}',
    "Z-mass3": f'{cuts[0]} && {cuts[5]}',
    "Z-mass4": f'{cuts[0]} && {cuts[6]}',
    "4_muons": f'{cuts[1]}',
    "4_opposite_charge_muons": f'{cuts[1]} && {cuts[2]}',
    "Full_selection": f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[3]}',
    "Full_selection2": f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[4]}',
    "Full_selection3": f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[5]}',
    "Full_selection4": f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[6]}',
}

cutLabels = {
    "selNone": "Before selection",
    #For event selection
    "Preselection": "Preselection",
    "2_jets" :  r"n_zjj >= 2",
    "Z-mass" :  r"70 < m_{Z} < 110 GeV",
    "Z-mass2" :  r"75 < m_{Z} < 105 GeV",
    "Z-mass3" :  r"80 < m_{Z} < 100 GeV",
    "Z-mass4" :  r"85 < m_{Z} < 95 GeV",
    "4_muons" : r"n_RecoMuons >= 4",
    "4_opposite_charge_muons" : r"n_RecoMuons >= 4 of opposite charge",
    "Full_selection" : r"Full Selection",
    "Full_selection2" : r"Full Selection2",
    "Full_selection3" : r"Full Selection3",
    "Full_selection4" : r"Full Selection4",
    }

# Dictionary for the output variables/histograms. The key is the name of the
# variable in the output files. "name" is the name of the variable in the input
# file, "title" is the x-axis label of the histogram, "bin" the number of bins
# of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum
# x-axis value.


histoList = {   
    'n_RecoMuons':                  {"name":'n_RecoMuons',               "title": "Number of reco. muons",                       "bin":10,  "xmin":-0.5,  "xmax":9.5},
    'RecoMuon_pt':                  {"name":'RecoMuon_pt',               "title": "Reco muons p_{T} [GeV]",                      "bin":100, "xmin":0,     "xmax":150},

    'n_zjj':                        {"name":'n_zjj',                     "title": "Number of reco. jets",                        "bin":20,  "xmin":-0.5,     "xmax":19.5},    
    'n_gen_Z':                      {"name":'n_gen_Z',                   "title": "Number of gen. Z",                            "bin":10,  "xmin":-0.5,     "xmax":9.5},    
    
    'zjj_invMass':                  {"name":'zjj_invMass',               "title": "M_{jj} [GeV]",                                "bin":100, "xmin":50,    "xmax":150},     
    'GenZ_InvM':                    {"name":'GenZ_InvM',                 "title": "M_{jj} [GeV]",                                "bin":100, "xmin":50,    "xmax":150},     
    
    'zjj_pt':                       {"name":'zjj_pt',                    "title": "Jets p_{T} [GeV]",                            "bin":100, "xmin":0,     "xmax":150},    
    'zjj_leading_pt':               {"name":'zjj_leading_pt',            "title": "Leading jet p_{T} [GeV]",                     "bin":100, "xmin":0,     "xmax":150},    
    'zjj_subleading_pt':            {"name":'zjj_subleading_pt',         "title": "Subleading jet p_{T} [GeV]",                  "bin":100, "xmin":0,     "xmax":150},    

    #'MuonPair1_charge':             {"name":'MuonPair1_charge',          "title": "Charge of Pair1",                             "bin":10, "xmin":-1.5,    "xmax":1.5},     
    #'MuonPair2_charge':             {"name":'MuonPair2_charge',          "title": "Charge of Pair2",                             "bin":10, "xmin":-1.5,    "xmax":1.5},     
    #"MuonPairs_charge":             {"name":'MuonPairs_charge',          "title": "Charge of Pair1 + Pair2",                     "bin":10,  "xmin":-1.5,   "xmax":1.5},     
    "MuonPairs_InvMass":            {"name":'MuonPairs_InvMass',         "title": "M_{#mu #mu #mu #mu} [GeV]",                   "bin":100, "xmin":115,    "xmax":135},            

    #"MuonPair1_total_charge":       {"name":'MuonPair1_total_charge',    "title": "Pair1 tot. charge",                           "bin":10,  "xmin":-1.5,   "xmax":1.5},     
    "MuonPair1_total_InvMass":      {"name":'MuonPair1_total_InvMass',   "title": "M_{#mu_{1}#mu_{2}} [GeV]",                    "bin":100, "xmin":0,      "xmax":10},  
    #"MuonPair2_total_charge":       {"name":'MuonPair2_total_charge',    "title": "Pair2 tot. charge",                           "bin":10,  "xmin":-1.5,   "xmax":1.5},     
    "MuonPair2_total_InvMass":      {"name":'MuonPair2_total_InvMass',   "title": "M_{#mu_{3}#mu_{4}} [GeV]",                    "bin":100, "xmin":0,      "xmax":10},  
 
    "MuonPair1_dR":                 {"name":'MuonPair1_dR',               "title": "Pair1 dR",                                   "bin":100, "xmin":0,      "xmax":1},  
    "MuonPair2_dR":                 {"name":'MuonPair2_dR',               "title": "Pair2 dR",                                   "bin":100, "xmin":0,      "xmax":1.5},  
    
    #"n_DVs":                        {"name":'n_DVs',                      "title": "Number of DV muon pairs",                    "bin":10,  "xmin":0,      "xmax":5},    
    #"DV1_Lxyz":                     {"name":'DV1_Lxyz',                   "title": "Pair1 Lxyz",                                 "bin":100, "xmin":0,      "xmax":5},  
    # "DV2_Lxyz":                    {"name":'DV2_Lxyz',                   "title": "Pair2 Lxyz",                                 "bin":100, "xmin":-0,     "xmax":2},  
    #"RecoMuons_Lxyz":               {"name":'RecoMuons_Lxyz',             "title": "All Lxy",                                    "bin":100, "xmin":0,      "xmax":2},  
    # # "n_GlobalDVs":               {"name":'n_GlobalDVs',                "title": "Number of DV all muons",                     "bin":10,  "xmin":0,      "xmax":5},    
    # "DV1_invM":                    {"name":'DV1_invM',                   "title": "Invariant mass of DP_1 [GeV]",               "bin":100, "xmin":0,      "xmax":10},  
    # "DV2_invM":                    {"name":'DV2_invM',                   "title": "Invariant mass of DP_2 [GeV]",               "bin":100, "xmin":0,      "xmax":10},  
    # "SecondaryVertex_Lxyz":        {"name":'SecondaryVertex_Lxyz',       "title": "All Lxy",                                    "bin":100, "xmin":0,      "xmax":2},  
    #"n_total_tracks":               {"name":'n_total_tracks',             "title": "Number of DV muon pairs",                    "bin":100,  "xmin":0,     "xmax":100},    

}