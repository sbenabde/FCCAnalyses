import ROOT

inputDir = "STAGE1_output/gen"
outputDir = "FINAL_output/gen/"

processList = {
        #Signal
        'dark_photons_mZd360MeV_e_1e-5':{},
        'dark_photons_mZd1100MeV_e_3.12e-6':{},
        'dark_photons_mZd7000MeV_e_2.7e-7':{},
        'wzp6_ee_qqH_HZZ_llll_ecm240':{},
}

#Need this block to add the cross sections of the self generated samples, otherwise it sets to 1.0 pb
procDictAdd = {
    'dark_photons_mZd360MeV_e_1e-5':         {"crossSection": 2.543e-06},
    'dark_photons_mZd1100MeV_e_3.12e-6':     {"crossSection": 2.816e-06},
    'dark_photons_mZd7000MeV_e_2.7e-7':      {"crossSection": 1.116e-06},
}

processLabels = {
    # #signals
    'dark_photons_mZd360MeV_e_1e-5':     r"m$_{Z_D}$=0.36 GeV, $\epsilon$=1*10$^{-5}$",
    'dark_photons_mZd1100MeV_e_3.12e-6': r"m$_{Z_D}$=1.1 GeV, $\epsilon$=3.12*10$^{-6}$",
    'dark_photons_mZd7000MeV_e_8.8e-7':  r"m$_{Z_D}$=7 GeV, $\epsilon$=2.7*10$^{-7}$",
    'wzp6_ee_qqH_HZZ_llll_ecm240':       r"h #to ZZ #to 4 #ell"
}

procDict = "FCCee_procDict_winter2023_IDEA.json"
intLumi = 10.8e+06  #pb-1
doScale = True
nCPUS = 4
doHistos = True
saveTabular = True
saveJSON = True
 
cutList = {"selNone": "n_FSGenMuon >=0"}
cutLabels = {"selNone": "Before selection"}
histoList = {   
    'FSGenMuon_pt':        {"name":'FSGenMuon_pt',        "title": "Truth #mu p_{T} [GeV]",             "bin":50, "xmin":0, "xmax":100},
    'FSGenMuon_eta':       {"name":'FSGenMuon_eta',       "title": "Truth #mu #eta",                    "bin":50, "xmin":-3,"xmax":3},
    'FSGenMuon_phi':       {"name":'FSGenMuon_phi',       "title": "Truth #mu #phi ",                   "bin":50, "xmin":-4,"xmax":4},
    'n_FSGenMuon':         {"name":'n_FSGenMuon',         "title": "Truth number of #mu",               "bin":6,   "xmin":2.5,"xmax":8.5},
    'FSGen_Lxyz':          {"name":'FSGen_Lxyz',          "title": "Truth #mu L_{xyz} [mm]",            "bin":50, "xmin":0, "xmax":800},
    'Muons_daughters_Lxyz':{"name":'Muons_daughters_Lxyz',"title": "Truth #mu L_{xyz} [mm]",            "bin":50, "xmin":0, "xmax":800},
    'GenZ_InvM':           {"name":'GenZ_InvM',           "title": "Truth M_{Z} [GeV]",                 "bin":50, "xmin":70, "xmax":110},
    'Jet_InvM':            {"name":'Jet_InvM',            "title": "Truth M_{jj} [GeV]",                "bin":50, "xmin":50, "xmax":150},
    'Muons_daughters_InvM':{"name":'Muons_daughters_InvM',"title": "Truth M_{4#mu} [GeV]",              "bin":50, "xmin":50, "xmax":150},
}