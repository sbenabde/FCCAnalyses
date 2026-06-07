import ROOT
intLumi = 10.8e+06 #in pb-1

ana_tex        = 'e^{+}e^{-} #rightarrow Zh, Z #rightarrow qq, h #rightarrow Z_{d} Z_{d}, Z_{d} #rightarrow #mu^{+} #mu^{-}'
delphesVersion = '3.4.2'
energy         = 240
collider       = 'FCC-ee'
inputDir       = "FINAL_output/gen/"
formats        = ['png']
yaxis          = ['lin','log']
stacksig       = ['nostack']
outdir         = 'PLOTS_output/'
splitLeg       = False

variables = ["FSGenMuon_phi",
            "FSGenMuon_pt",
            "FSGenMuon_eta", 
            'n_FSGenMuon',   
            'FSGen_Lxyz', 
            'Muons_daughters_Lxyz',   
            'GenZ_InvM',   
            'Jet_InvM',   
            'Muons_daughters_InvM',          
]
selections = {}
selections['Lumi']=['selNone']
selections['Normalize'] =["selNone"]

extralabel = {}
extralabel['selNone'] = ""

plots = {}
my_samples = {
      'signal':{'dark_photons_mZd360MeV_e_1e-5':['dark_photons_mZd360MeV_e_1e-5'],
                'dark_photons_mZd1100MeV_e_3.12e-6':['dark_photons_mZd1100MeV_e_3.12e-6'], 
                'dark_photons_mZd7000MeV_e_2.7e-7':['dark_photons_mZd7000MeV_e_2.7e-7']},
      'backgrounds':{'wzp6_ee_qqH_HZZ_llll_ecm240':['wzp6_ee_qqH_HZZ_llll_ecm240'],
                  },            
            }
plots['Lumi'] = {**my_samples, 'normalize': False, 'ytitle': 'Events'}
plots['Normalize'] = {**my_samples, 'normalize': True, 'ytitle': 'Normalized to 1'}


colors = {}
colors['dark_photons_mZd360MeV_e_1e-5'] = ROOT.kViolet+7
colors['dark_photons_mZd1100MeV_e_3.12e-6'] = ROOT.kMagenta+3
colors['dark_photons_mZd7000MeV_e_2.7e-7'] = ROOT.kPink+8
colors['wzp6_ee_qqH_HZZ_llll_ecm240'] = ROOT.kViolet-9

legend = {}
legend['dark_photons_mZd360MeV_e_1e-5']     = '0.36 GeV, 1#times10^{-5}'
legend['dark_photons_mZd1100MeV_e_3.12e-6'] = '1.1 GeV, 3.12#times10^{-6}'
legend['dark_photons_mZd7000MeV_e_2.7e-7']  = '7 GeV, 2.7#times10^{-7}'
legend['wzp6_ee_qqH_HZZ_llll_ecm240']       = r'h #rightarrow ZZ #rightarrow llll'
