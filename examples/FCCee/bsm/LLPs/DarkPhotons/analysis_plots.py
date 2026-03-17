import ROOT

# global parameters
intLumi = 10.8e+06 #in pb-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
# scaleSig       = 1
# scaleBack      = 1
normalize      = True
ana_tex        = 'e^{+}e^{-} #rightarrow Zh, Z #rightarrow qq, h #rightarrow Z_{d} Z_{d}, Z_{d} #rightarrow #mu^{+} #mu^{-}'
delphesVersion = '3.4.2'
energy         = 240
collider       = 'FCC-ee'
inputDir       = "FINAL_output/"
formats        = ['png']
yaxis          = ['lin','log']
stacksig       = ['nostack']
outdir         = 'PLOTS_output/Normalized/All_BG'
splitLeg       = False

variables = ['n_RecoMuons',
            'RecoMuon_pt',

            'n_zjj',
            'zjj_pt',
            'zjj_leading_pt',
            'zjj_subleading_pt',
            'zjj_invMass',

            'MuonPairs_InvMass',
            "MuonPair1_dR",
            "MuonPair2_dR",
            'MuonPair1_total_InvMass',
            'MuonPair2_total_InvMass',
                        
]

#Dictionary with the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Normalize']  = [
    "selNone",
    "Preselection",
    "Z-mass",
    "Z-mass2",
    "Z-mass3",
    "Z-mass4",
    "Full_selection",
    "Full_selection2",
    "Full_selection3",
    "Full_selection4",
]

extralabel = {}
extralabel['selNone'] = r"No selection"
extralabel['Preselection'] = r"Preselection"
extralabel['Z-mass']  = r"n_{zjj} >= 2 & 70 < m_{Z} < 110 GeV"
extralabel['Z-mass2']  = r"n_{zjj} >= 2 & 75 < m_{Z} < 105 GeV"
extralabel['Z-mass3']  = r"n_{zjj} >= 2 & 80 < m_{Z} < 100 GeV"
extralabel['Z-mass4']  = r"n_{zjj} >= 2 & 85 < m_{Z} < 95 GeV"
extralabel['Full_selection'] = r"Full Selection"
extralabel['Full_selection2'] = r"Full Selection2"
extralabel['Full_selection3'] = r"Full Selection3"
extralabel['Full_selection4'] = r"Full Selection4"


plots = {}
plots['Normalize'] = {
      'signal':{'dark_photons_mZd360MeV_e_1e-5':['dark_photons_mZd360MeV_e_1e-5'],
                'dark_photons_mZd1100MeV_e_3.12e-6':['dark_photons_mZd1100MeV_e_3.12e-6'],
                'dark_photons_mZd7000MeV_e_2.7e-7':['dark_photons_mZd7000MeV_e_2.7e-7'],
                },
        'backgrounds':{ 'wzp6_ee_bbH_HZZ_ecm240':['wzp6_ee_bbH_HZZ_ecm240'],
                        'wzp6_ee_qqH_Hmumu_ecm240':['wzp6_ee_qqH_Hmumu_ecm240'],
                        'wzp6_ee_ccH_Hmumu_ecm240':['wzp6_ee_ccH_Hmumu_ecm240'],
                        'wzp6_ee_bbH_Hmumu_ecm240':['wzp6_ee_bbH_Hmumu_ecm240'],
                        'wzp6_ee_qqH_HZZ_llll_ecm240':['wzp6_ee_qqH_HZZ_llll_ecm240'],
                        'wzp6_ee_qqH_HWW_ecm240':['wzp6_ee_qqH_HWW_ecm240'],
                        'wzp6_ee_ccH_HWW_ecm240':['wzp6_ee_ccH_HWW_ecm240'],
                        'wzp6_ee_bbH_HWW_ecm240':['wzp6_ee_bbH_HWW_ecm240'],
                        'wzp6_ee_mumuH_Hbb_ecm240':['wzp6_ee_mumuH_Hbb_ecm240'],
                        'p8_ee_ZZ_ecm240':['p8_ee_ZZ_ecm240'],
                        'p8_ee_WW_ecm240':['p8_ee_WW_ecm240'],

                }
            }

linestyle = {}
colors = {}
colors['dark_photons_mZd360MeV_e_1e-5'] = ROOT.kViolet+7
colors['dark_photons_mZd1100MeV_e_3.12e-6'] = ROOT.kMagenta+3
colors['dark_photons_mZd7000MeV_e_2.7e-7'] = ROOT.kPink+8

colors['wzp6_ee_bbH_HZZ_ecm240'] = ROOT.kSpring+1
colors['wzp6_ee_qqH_Hmumu_ecm240'] = ROOT.kRed-8
colors['wzp6_ee_ccH_Hmumu_ecm240'] = ROOT.kRed-9
colors['wzp6_ee_bbH_Hmumu_ecm240'] = ROOT.kRed-10
colors['wzp6_ee_qqH_HZZ_llll_ecm240'] = ROOT.kOrange-9
colors['wzp6_ee_qqH_HWW_ecm240'] = ROOT.kGreen-7
colors['wzp6_ee_ccH_HWW_ecm240'] = ROOT.kGreen-8
colors['wzp6_ee_bbH_HWW_ecm240'] = ROOT.kGreen-9
colors['wzp6_ee_mumuH_Hbb_ecm240'] = ROOT.kBlue-10
colors['p8_ee_ZZ_ecm240'] = ROOT.kMagenta-10
colors['p8_ee_WW_ecm240'] = ROOT.kMagenta-9

legend = {}
legend['dark_photons_mZd360MeV_e_1e-5']     = '360MeV, 1#times10^{-5}'
legend['dark_photons_mZd1100MeV_e_3.12e-6'] = '1100MeV, 3.12#times10^{-6}'
legend['dark_photons_mZd7000MeV_e_2.7e-7']  = '7000MeV, 2.7#times10^{-7}'

legend['wzp6_ee_bbH_HZZ_ecm240'] =       r"z #rightarrow bb, h #rightarrow ZZ"
legend['wzp6_ee_qqH_Hmumu_ecm240'] =     r"z #rightarrow qq, h #rightarrow #mu #mu"
legend['wzp6_ee_ccH_Hmumu_ecm240'] =     r"z #rightarrow cc, h #rightarrow #mu #mu"
legend['wzp6_ee_bbH_Hmumu_ecm240'] =     r"z #rightarrow bb, h #rightarrow #mu #mu"
legend['wzp6_ee_qqH_HZZ_llll_ecm240'] =  r"z #rightarrow qq, h #rightarrow ZZ #rightarrow llll"
legend['wzp6_ee_qqH_HWW_ecm240'] =       r"z #rightarrow qq, h #rightarrow WW"
legend['wzp6_ee_ccH_HWW_ecm240'] =       r"z #rightarrow cc, h #rightarrow WW"
legend['wzp6_ee_bbH_HWW_ecm240'] =       r"z #rightarrow bb, h #rightarrow WW"
legend['wzp6_ee_mumuH_Hbb_ecm240'] =     r"z #rightarrow #mu #mu, h #rightarrow bb"
legend['p8_ee_ZZ_ecm240'] =              r"e^{+}e^{-} #rightarrow ZZ"
legend['p8_ee_WW_ecm240'] =              r"e^{+}e^{-} #rightarrow WW"
