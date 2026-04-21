import ROOT

#Input directory where the files produced in the pre-selection stages are
inputDir = "STAGE1_output"
#Output directory where the resulting files will be stored
outputDir = "FINAL_output/signal"

#Run over the full statistics from stage1 input file
processList = {
        #Signal
        'dark_photons_mZd360MeV_e_1e-5':{},
        'dark_photons_mZd1100MeV_e_3.12e-6':{},
        'dark_photons_mZd7000MeV_e_2.7e-7':{},

        #Background
        #'bkg_ee_qqH_HZZ_4l':{},
        #'bkg_ee_qqH_HZZ_4mu':{},
 
        #'wzp6_ee_qqH_HZZ_ecm240':{},
        #'wzp6_ee_bbH_HZZ_ecm240':{},
        #'wzp6_ee_qqH_ecm240':{},

        #'wzp6_ee_mumuH_Hmumu_ecm240':{},

        #'wzp6_ee_qqH_Hmumu_ecm240':{},
        #'wzp6_ee_ccH_Hmumu_ecm240':{},
        #'wzp6_ee_bbH_Hmumu_ecm240':{},

       #'wzp6_ee_qqH_HZZ_llll_ecm240':{},

        #'wzp6_ee_qqH_HWW_ecm240':{},
        #'wzp6_ee_ccH_HWW_ecm240':{},
        #'wzp6_ee_bbH_HWW_ecm240':{},

        # 'wzp6_ee_mumuH_Hbb_ecm240':{},
        
        #'p8_ee_ZZ_ecm240':{},
        #'p8_ee_WW_ecm240':{},
}

#Need this block to add the cross sections of the self generated samples, otherwise it sets to 1.0 pb
procDictAdd = {
    'dark_photons_mZd360MeV_e_1e-5':         {"crossSection": 2.543e-06},
    'dark_photons_mZd1100MeV_e_3.12e-6':     {"crossSection": 2.816e-06},
    'dark_photons_mZd7000MeV_e_2.7e-7':      {"crossSection": 1.116e-06},
    'bkg_ee_qqH_HZZ_4l':                     {"crossSection": 1.229e-05},
    'bkg_ee_qqH_HZZ_4mu':                    {"crossSection": 3.222e-06},
}

processLabels = {
    # #signals
    'dark_photons_mZd360MeV_e_1e-5':     r"m$_{Z_D}$=360MeV, $\epsilon$=1*10$^{-5}$",
    'dark_photons_mZd1100MeV_e_3.12e-6': r"m$_{Z_D}$=1100MeV, $\epsilon$=3.12*10$^{-6}$",
    'dark_photons_mZd7000MeV_e_8.8e-7':  r"m$_{Z_D}$=7000MeV, $\epsilon$=8.8*10$^{-7}$",
    
    #Backgrounds
    'bkg_ee_qqH_HZZ_4l':            r"Z #\rightarrow qq, h #\rightarrow ZZ #\rightarrow 4l",
    'bkg_ee_qqH_HZZ_4mu':           r"Z #\rightarrow qq, h #\rightarrow ZZ #\rightarrow 4mu",
    
    
    'wzp6_ee_qqH_HZZ_ecm240':       r"Z #\rightarrow qq, h #\rightarrow ZZ",
    'wzp6_ee_bbH_HZZ_ecm240':       r"Z #\rightarrow bb, h #\rightarrow ZZ",
    'wzp6_ee_qqH_ecm240':           r"ee #\rightarrow Zh, Z #\rightarrow qq",

    'wzp6_ee_qqH_Hmumu_ecm240':     r"Z #\rightarrow qq, h #\rightarrow #mu #mu",
    'wzp6_ee_ccH_Hmumu_ecm240':     r"Z #\rightarrow cc, h #\rightarrow #mu #mu",
    'wzp6_ee_bbH_Hmumu_ecm240':     r"Z #\rightarrow bb, h #\rightarrow #mu #mu",
    
    'wzp6_ee_qqH_HZZ_llll_ecm240':  r"Z #\rightarrow qq, h #\rightarrow ZZ #\rightarrow llll",

    'wzp6_ee_qqH_HWW_ecm240':       r"Z #\rightarrow qq, h #\rightarrow WW",
    'wzp6_ee_ccH_HWW_ecm240':       r"Z #\rightarrow cc, h #\rightarrow WW",
    'wzp6_ee_bbH_HWW_ecm240':       r"Z #\rightarrow bb, h #\rightarrow WW",

    'wzp6_ee_mumuH_Hbb_ecm240':     r"Z #\rightarrow #mu #mu, h #\rightarrow bb",
   
    'p8_ee_ZZ_ecm240':              r"ee #\rightarrow ZZ",
    'p8_ee_WW_ecm240':              r"ee #\rightarrow WW",
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
        '(n_RecoMuons >= 4)',
        '(Sum(RecoMuon_charge > 0) >= 2 && Sum(RecoMuon_charge < 0) >= 2)',
        '(zjj_invMass > 70 && zjj_invMass < 110)',
        '(zjj_invMass > 75 && zjj_invMass < 105)',
        '(zjj_invMass > 80 && zjj_invMass < 100)',
        '(zjj_invMass > 85 && zjj_invMass < 95)',
        '(MuonPair1_total_InvMass < 11 && MuonPair2_total_InvMass < 11)',
        '(MuonPairs_InvMass > 120 && MuonPairs_InvMass < 130)',
        '(All(DV_lxyz > 3))',

]

#Dictionary with the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    "selNone": "n_zjj >= 0",
   
    #For event selection
    "2_jets": f'{cuts[0]}',
    "4_muons":f'{cuts[1]}',
    "4OS_muons":f'{cuts[2]}',

    "Preselection": f'{cuts[0]} && {cuts[1]} && {cuts[2]}', 

    #"Z-mass": f'{cuts[0]} && {cuts[3]}',
    #"Full_Zselection": f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[3]}',
    
    "Leptonic_InvM": f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[7]}',
    "4mu_InvM": f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[8]}',
    "DV_lxyz": f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[9]}',
    "Full_selection": f'{cuts[0]} && {cuts[1]} && {cuts[2]} && {cuts[7]} && {cuts[8]} && {cuts[9]}',

}

cutLabels = {
    "selNone": "Before selection",
    #For event selection
    "2_jets" :      r"n_zjj >= 2",
    "4_muons" :     r"n_RecoMu >= 4",
    "4OS_muons" :   r"Opposite charge muons",

    "Preselection": r"Preselection",

    #"Z-mass" :      r"70 < m_{Z} < 110 GeV",
    #"Full_Zselection" : r"Full Selection",
   
    "Leptonic_InvM" :  r"Leptonic_InvM",
    "4mu_InvM" :       r"4mu_InvM",
    "DV_lxyz" :        r"DV_lxyz",
    "Full_selection" : r"Full_selection",
    }

# Dictionary for the output variables/histograms. The key is the name of the
# variable in the output files. "name" is the name of the variable in the input
# file, "title" is the x-axis label of the histogram, "bin" the number of bins
# of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum
# x-axis value.


histoList = {   
    'n_RecoMuons':                          {"name":'n_RecoMuons',               "title": "Number of reco. muons",            "bin":10,  "xmin":-0.5, "xmax":9.5},
    'RecoMuon_pt':                          {"name":'RecoMuon_pt',               "title": "Reco muons p_{T} [GeV]",           "bin":100, "xmin":0,    "xmax":150},
    'Selected_muons_pt':                    {"name":'Selected_muons_pt',         "title": "Selected 4#mu p_{T} [GeV]",                 "bin":100, "xmin":0,    "xmax":100},
    'Selected_muons_eta':                   {"name":'Selected_muons_eta',        "title": "Selected 4#mu #eta",                        "bin":100, "xmin":-3,   "xmax":3},
    
    'n_zjj':                                {"name":'n_zjj',                     "title": "Number of reco. jets",             "bin":20,  "xmin":-0.5, "xmax":19.5},       
    'zjj_invMass':                          {"name":'zjj_invMass',               "title": "M_{jj} [GeV]",                     "bin":100, "xmin":50,   "xmax":150},     
    'zjj_pt':                               {"name":'zjj_pt',                    "title": "Jets p_{T} [GeV]",                 "bin":100, "xmin":0,    "xmax":150},    
    'zjj_leading_pt':                       {"name":'zjj_leading_pt',            "title": "Leading jet p_{T} [GeV]",          "bin":100, "xmin":0,    "xmax":150},    
    'zjj_subleading_pt':                    {"name":'zjj_subleading_pt',         "title": "Subleading jet p_{T} [GeV]",       "bin":100, "xmin":0,    "xmax":150},    

    "MuonPairs_InvMass":                    {"name":'MuonPairs_InvMass',         "title": "M_{4#mu} [GeV]",                   "bin":100, "xmin":115,  "xmax":135},            
    "MuonPairs_InvMass_long_range":         {"name":'MuonPairs_InvMass',         "title": "M_{4#mu} [GeV]",                   "bin":100, "xmin":0,    "xmax":135},            
    "MuonPair1_total_InvMass":              {"name":'MuonPair1_total_InvMass',   "title": "M_{#mu_{1}#mu_{2}} [GeV]",         "bin":100, "xmin":-0.5, "xmax":9.5},  
    "MuonPair1_total_InvMass_long_range":   {"name":'MuonPair1_total_InvMass',   "title": "M_{#mu_{1}#mu_{2}} [GeV]",         "bin":100, "xmin":0,    "xmax":110},  
    "MuonPair2_total_InvMass":              {"name":'MuonPair2_total_InvMass',   "title": "M_{#mu_{3}#mu_{4}} [GeV]",         "bin":100, "xmin":-0.5, "xmax":9.5},  
    "MuonPair2_total_InvMass_long_range":   {"name":'MuonPair2_total_InvMass',   "title": "M_{#mu_{3}#mu_{4}} [GeV]",         "bin":100, "xmin":0,    "xmax":110},  
 
    "MuonPair1_dR":                         {"name":'MuonPair1_dR',              "title": "Pair1 dR",                         "bin":100, "xmin":0,    "xmax":1},  
    "MuonPair2_dR":                         {"name":'MuonPair2_dR',              "title": "Pair2 dR",                         "bin":100, "xmin":0,    "xmax":1.5},  
    
    'RP_noMu_InvM':                         {"name":'RP_noMu_InvM',              "title": "RP_noMu M_{jj} [GeV]",             "bin":100, "xmin":50,   "xmax":150},     
    
    "n_DVs":                                {"name":'n_DVs',                     "title": "Number of DV muon pairs",          "bin":5,  "xmin":-0.5,   "xmax":4.5},    
    "DV1_Lxyz":                             {"name":'DV1_Lxyz',                  "title": "L_{xyz} DV_1 [mm]",                "bin":100, "xmin":0,     "xmax":800},  
    "DV2_Lxyz":                             {"name":'DV2_Lxyz',                  "title": "L_{xyz} DV_2 [mm]",                "bin":100, "xmin":0,     "xmax":800},  
    "DV_lxyz":                              {"name":'DV_lxyz',                   "title": "L_{xyz} [mm]",                     "bin":100, "xmin":0,     "xmax":800},  
}