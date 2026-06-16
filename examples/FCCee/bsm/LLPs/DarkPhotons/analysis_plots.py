import ROOT

# global parameters
intLumi = 10.8e+06 #in pb-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
# scaleSig       = 0.
# scaleBack      = 0.
ana_tex        = "e^{+}e^{-} #rightarrow Zh, Z #rightarrow qq, h #rightarrow A' A', A' #rightarrow #mu^{+} #mu^{-}"
delphesVersion = '3.4.2'
energy         = 240
collider       = 'FCC-ee'
inputDir       = "/eos/experiment/fcc/ee/analyses_storage/BSM/LLPs/DarkPhotons/Final_output_backgrounds/"
formats        = ['png', 'pdf']
yaxis          = ['lin','log']
# xaxis          = ['lin', 'log']
stacksig       = ['nostack']
outdir         = '/eos/user/s/sbenabde/PLOTS_output/submission/three_bkg'
splitLeg       = False

variables = [
            'n_RecoMuons',
            'RecoMuon_pt',
            'Selected_muons_pt',
            'Selected_muons_eta',

            'n_zjj',
            'zjj_invMass',
            'zjj_pt',
            'zjj_leading_pt',
            'zjj_subleading_pt',

            'MuonPairs_InvMass',
            # 'MuonPairs_InvMass_long_range',
            'MuonPair1_total_InvMass',
            # 'MuonPair1_total_InvMass_long_range',
            'MuonPair2_total_InvMass',
            # 'MuonPair2_total_InvMass_long_range',
            
            'MuonPair1_dR',
            'MuonPair2_dR',

            'DV1_Lxyz',
            'DV2_Lxyz',
            'DV_lxyz',
            'DV_lxyz_short',
            'n_DVs'
]

#Dictionary with the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Lumi']  = [
    "selNone",
    "Preselection",
    "4mu_InvM",
    "Leptonic_InvM",
    "DV_lxyz",
    "Total_Selection",
]
selections['Normalize']  = [
    "selNone",
    "Preselection",
    "4mu_InvM",
    "Leptonic_InvM",
    "DV_lxyz",
    "Total_Selection",
]

extralabel = {}
extralabel['selNone'] =         r"No selection"
extralabel['Preselection'] =    r"Preselection"
extralabel['4mu_InvM'] =        r"#splitline{Preselection}{120 GeV < M_{4#mu} < 130 GeV}"
extralabel['Leptonic_InvM'] =   r"#splitline{Preselection}{#splitline{120 GeV < M_{4#mu} < 130 GeV}{M_{2#mu} < 11 GeV}}"
extralabel['DV_lxyz'] =         r"#splitline{Preselection}{#splitline{120 GeV < M_{4#mu} < 130 GeV}{#splitline{M_{2#mu} < 11 GeV}{L_{xyz} > 3 mm}}}"
extralabel['Total_Selection'] = r"Total Selection"


plots = {}
my_samples = {
        'signal':{
                'dark_photons_mZd360MeV_e_1e-5':['dark_photons_mZd360MeV_e_1e-5'],
                'dark_photons_mZd1100MeV_e_3.12e-6':['dark_photons_mZd1100MeV_e_3.12e-6'],
                'dark_photons_mZd7000MeV_e_2.7e-7':['dark_photons_mZd7000MeV_e_2.7e-7'],

   

                # 'dark_photons_mZd10000MeV_e_6.7e-7':['dark_photons_mZd10000MeV_e_6.7e-7'],
                },
        'backgrounds':{ #'wzp6_ee_qqH_HZZ_ecm240':['wzp6_ee_qqH_HZZ_ecm240'],

                        #'bkg_ee_qqH_HZZ_4l':['bkg_ee_qqH_HZZ_4l'],
                        #'bkg_ee_qqH_HZZ_4mu':['bkg_ee_qqH_HZZ_4mu'],
                        
                        #'wzp6_ee_bbH_HZZ_ecm240':['wzp6_ee_bbH_HZZ_ecm240'],
                        #'wzp6_ee_qqH_ecm240':['wzp6_ee_qqH_ecm240'],

                        #'wzp6_ee_mumuH_Hmumu_ecm240':['wzp6_ee_mumuH_Hmumu_ecm240'],

                        #'wzp6_ee_qqH_Hmumu_ecm240':['wzp6_ee_qqH_Hmumu_ecm240'],
                        #'wzp6_ee_ccH_Hmumu_ecm240':['wzp6_ee_ccH_Hmumu_ecm240'],
                        #'wzp6_ee_bbH_Hmumu_ecm240':['wzp6_ee_bbH_Hmumu_ecm240'],

                        'wzp6_ee_qqH_HZZ_llll_ecm240':['wzp6_ee_qqH_HZZ_llll_ecm240'],

                        #'wzp6_ee_qqH_HWW_ecm240':['wzp6_ee_qqH_HWW_ecm240'],
                        #'wzp6_ee_ccH_HWW_ecm240':['wzp6_ee_ccH_HWW_ecm240'],
                        #'wzp6_ee_bbH_HWW_ecm240':['wzp6_ee_bbH_HWW_ecm240'],

                        #'wzp6_ee_mumuH_Hbb_ecm240':['wzp6_ee_mumuH_Hbb_ecm240'],

                        'p8_ee_ZZ_ecm240':['p8_ee_ZZ_ecm240'],
                        'p8_ee_WW_ecm240':['p8_ee_WW_ecm240'],

                },            
                }

plots['Lumi'] = {**my_samples, 'normalize': False, 'ytitle': 'Events'}
plots['Normalize'] = {**my_samples, 'normalize': True, 'ytitle': 'Normalized to 1'}

linestyle = {}
colors = {}
purple = ROOT.TColor.GetColor("#B95E82")
pink = ROOT.TColor.GetColor("#F39F9F")
orange = ROOT.TColor.GetColor("#FFC29B")
yellow = ROOT.TColor.GetColor("#FFECC0")

green1 = ROOT.TColor.GetColor("#84B179")
green2 = ROOT.TColor.GetColor("#A2CB8B")
green3 = ROOT.TColor.GetColor("#C7EABB")


colors['dark_photons_mZd360MeV_e_1e-5']      = purple
colors['dark_photons_mZd1100MeV_e_3.12e-6']  = pink
colors['dark_photons_mZd7000MeV_e_2.7e-7']   = orange
colors['dark_photons_mZd10000MeV_e_6.7e-7']  = yellow

colors['dark_photons_mZd10000MeV_e_2.7e-7']  = ROOT.kPink-8

colors['bkg_ee_qqH_HZZ_4l']  = ROOT.kViolet-9
colors['bkg_ee_qqH_HZZ_4mu'] = ROOT.kViolet-9

colors['wzp6_ee_qqH_HZZ_ecm240'] = ROOT.kViolet-8
colors['wzp6_ee_bbH_HZZ_ecm240'] = ROOT.kViolet-7

colors['wzp6_ee_qqH_ecm240']       = ROOT.kPink+1
colors['wzp6_ee_qqH_Hmumu_ecm240'] = ROOT.kOrange-10
colors['wzp6_ee_ccH_Hmumu_ecm240'] = ROOT.kOrange-9
colors['wzp6_ee_bbH_Hmumu_ecm240'] = ROOT.kOrange-8

colors['wzp6_ee_mumuH_Hmumu_ecm240'] = ROOT.kRed-10

colors['wzp6_ee_qqH_HZZ_llll_ecm240'] = green1

colors['wzp6_ee_qqH_HWW_ecm240'] = ROOT.kPink-10
colors['wzp6_ee_ccH_HWW_ecm240'] = ROOT.kPink-9
colors['wzp6_ee_bbH_HWW_ecm240'] = ROOT.kPink-8

colors['wzp6_ee_mumuH_Hbb_ecm240'] = ROOT.kGreen-10

colors['p8_ee_ZZ_ecm240'] = green2
colors['p8_ee_WW_ecm240'] = green3

legend = {}
legend['dark_photons_mZd360MeV_e_1e-5']     = '0.36 GeV, 1#times10^{-5}'
legend['dark_photons_mZd1100MeV_e_3.12e-6'] = '1.1 GeV, 3.12#times10^{-6}'
legend['dark_photons_mZd7000MeV_e_2.7e-7']  = '7 GeV, 2.7#times10^{-7}'
legend['dark_photons_mZd10000MeV_e_6.7e-7']  = '10 GeV, 6.7#times10^{-7}'


legend['dark_photons_mZd10000MeV_e_2.7e-7']  = '10 GeV, 2.7#times10^{-7}'

legend['bkg_ee_qqH_HZZ_4l'] =            r"Z #rightarrow qq, h #rightarrow 4l self"
legend['bkg_ee_qqH_HZZ_4mu'] =           r"Z #rightarrow qq, h #rightarrow 4mu self"

legend['wzp6_ee_qqH_HZZ_ecm240'] =       r"Z #rightarrow qq, h #rightarrow ZZ"
legend['wzp6_ee_bbH_HZZ_ecm240'] =       r"Z #rightarrow bb, h #rightarrow ZZ"

legend['wzp6_ee_qqH_ecm240'] =           r"e^{+}e^{-} #rightarrow Zh, Z #rightarrow qq"

legend['wzp6_ee_qqH_Hmumu_ecm240'] =     r"z #rightarrow qq, h #rightarrow #mu #mu"
legend['wzp6_ee_ccH_Hmumu_ecm240'] =     r"z #rightarrow cc, h #rightarrow #mu #mu"
legend['wzp6_ee_bbH_Hmumu_ecm240'] =     r"z #rightarrow bb, h #rightarrow #mu #mu"

legend['wzp6_ee_mumuH_Hmumu_ecm240'] =   r"z #rightarrow #mu #mu, h #rightarrow #mu #mu"

legend['wzp6_ee_qqH_HZZ_llll_ecm240'] =  r"Z #rightarrow qq, h #rightarrow ZZ #rightarrow llll"

legend['wzp6_ee_qqH_HWW_ecm240'] =       r"z #rightarrow qq, h #rightarrow WW"
legend['wzp6_ee_ccH_HWW_ecm240'] =       r"z #rightarrow cc, h #rightarrow WW"
legend['wzp6_ee_bbH_HWW_ecm240'] =       r"z #rightarrow bb, h #rightarrow WW"

legend['wzp6_ee_mumuH_Hbb_ecm240'] =     r"z #rightarrow #mu #mu, h #rightarrow bb"

legend['p8_ee_ZZ_ecm240'] =              r"e^{+}e^{-} #rightarrow ZZ"
legend['p8_ee_WW_ecm240'] =              r"e^{+}e^{-} #rightarrow WW"
