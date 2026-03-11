import ROOT

# global parameters
intLumi = 10.8e+06 #in pb-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
# scaleSig       = 0.
# scaleBack      = 0.
ana_tex        = 'e^{+}e^{-} #rightarrow Zh, Z #rightarrow qq, h #rightarrow Z_{d} Z_{d}, Z_{d} #rightarrow #mu^{+} #mu^{-}'
delphesVersion = '3.4.2'
energy         = 240
collider       = 'FCC-ee'
inputDir       = "FINAL_output/"
formats        = ['png']
yaxis          = ['lin','log']
stacksig       = ['nostack']
outdir         = 'PLOTS_output/'
splitLeg       = False

variables = ['n_RecoMuons',
            'RecoMuon_pt',

            'n_DVs',
            'DV1_Lxyz',
            # 'DV2_Lxyz',
            'RecoMuons_Lxyz',
            # 'n_GlobalDVs_raw;1',

            'n_zjj',
            'zjj_pt',
            'zjj_leading_pt',
            'zjj_subleading_pt',
            'zjj_invMass',

            'MuonPair1_charge',
            'MuonPair2_charge',
            'MuonPairs_InvMass',
            "MuonPair1_dR",
            "MuonPair2_dR",
            'MuonPair1_total_charge',
            'MuonPair1_total_InvMass',
            'MuonPair2_total_charge',
            'MuonPair2_total_InvMass',
                        
]

#Dictionary with the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['DarkPhotons']  = [
    "selNone",
    "Z-mass",
    "Z-mass2",
    "Z-mass3",
    "Z-mass4",
    "4_muons",
    "4_opposite_charge_muons",
    "Full_selection",
    "Full_selection2",
    "Full_selection3",
    "Full_selection4",
]

extralabel = {}
extralabel['selNone'] = r"No selection"
extralabel['Z-mass']  = r"n_{zjj} >= 2 & 70 < m_{Z} < 110 GeV"
extralabel['Z-mass2']  = r"n_{zjj} >= 2 & 75 < m_{Z} < 105 GeV"
extralabel['Z-mass3']  = r"n_{zjj} >= 2 & 80 < m_{Z} < 100 GeV"
extralabel['Z-mass4']  = r"n_{zjj} >= 2 & 85 < m_{Z} < 95 GeV"
extralabel['4_muons'] = r"At least 4 RecoMuons"
extralabel['4_opposite_charge_muons'] = r"At least 4 RecoMuons, 2 of each charge"
extralabel['Full_selection'] = r"Full Selection"
extralabel['Full_selection2'] = r"Full Selection2"
extralabel['Full_selection3'] = r"Full Selection3"
extralabel['Full_selection4'] = r"Full Selection4"

linestyle = {}
colors = {}
colors['dark_photons_mZd360MeV_e_1e-5'] = ROOT.kViolet-5
colors['dark_photons_mZd1100MeV_e_3.12e-6'] = ROOT.kMagenta+4
colors['dark_photons_mZd7000MeV_e_2.7e-7'] = ROOT.kPink+10
# colors['wzp6_ee_ccH_Hmumu_ecm240'] = ROOT.kBlue-10
# colors['wzp6_ee_mumuH_Hbb_ecm240'] = ROOT.kRed-10
# colors['mgp8_ee_zh_ecm240'] = ROOT.kMagenta-10
colors['wzp6_ee_bbH_HZZ_ecm240'] = ROOT.kMagenta-10

plots = {}
plots['DarkPhotons'] = {
      'signal':{'dark_photons_mZd360MeV_e_1e-5':['dark_photons_mZd360MeV_e_1e-5'],
                'dark_photons_mZd1100MeV_e_3.12e-6':['dark_photons_mZd1100MeV_e_3.12e-6'],
                'dark_photons_mZd7000MeV_e_2.7e-7':['dark_photons_mZd7000MeV_e_2.7e-7'],
                },
        'backgrounds':{#'wzp6_ee_ccH_Hmumu_ecm240':['wzp6_ee_ccH_Hmumu_ecm240'],
                    #'wzp6_ee_mumuH_Hbb_ecm240':['wzp6_ee_mumuH_Hbb_ecm240'],
                    #'mgp8_ee_zh_ecm240':['mgp8_ee_zh_ecm240'],
                    'wzp6_ee_bbH_HZZ_ecm240':['wzp6_ee_bbH_HZZ_ecm240'],
                }
            }

legend = {}
legend['dark_photons_mZd360MeV_e_1e-5'] = '360MeV, 1#times10^{-5}'
legend['dark_photons_mZd1100MeV_e_3.12e-6'] = '1100MeV, 3.12#times10^{-6}'
legend['dark_photons_mZd7000MeV_e_2.7e-7'] = '7000MeV, 2.7#times10^{-7}'
# legend['wzp6_ee_ccH_Hmumu_ecm240'] = r'Z_cc, H_mumu'
# legend['wzp6_ee_mumuH_Hbb_ecm240'] = r'Z_mumu, H_bb'
# legend['mgp8_ee_zh_ecm240'] = r'ZH'
legend['wzp6_ee_bbH_HZZ_ecm240'] = 'z #rightarrow b#bar{b}, H #rightarrow ZZ'

