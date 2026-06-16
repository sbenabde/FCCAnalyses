import os
import sys
import time
import glob
import logging
import importlib.util
import pathlib
import json
import math
from typing import Any
import os    
import re
import ROOT  # type: ignore
import cppyy  # type: ignore
from anascript import get_element, get_attribute
from process import get_process_dict
from frame import generate_graph

LOGGER = logging.getLogger('FCCAnalyses.run_final')

ROOT.gROOT.SetBatch(True)


#------------------------------------------------------------------------------
def get_entries(infilepath: str) -> tuple[int, int]:

    events_processed = 0
    events_in_ttree = 0

    with ROOT.TFile(infilepath, 'READ') as infile:
        try:
            meta = infile.Get('eventsProcessed')
            if meta:
                events_processed = meta.GetVal()
            else:
                raise AttributeError

        except AttributeError:
            LOGGER.warning('Missing eventsProcessed → falling back to TTree entries')
            events_processed = -1
        try:
            tree = infile.Get("events")
            events_in_ttree = tree.GetEntries()

            if events_processed <= 0:
                events_processed = events_in_ttree

        except AttributeError:
            LOGGER.error('Missing "events" TTree!')
            sys.exit(3)

    return events_processed, events_in_ttree


#------------------------------------------------------------------------------
def get_processes(rdf_module: object) -> list[str]:
    '''
    Get processes from the analysis script or find them in the input directory.
    TODO: filter out files without .root suffix
    '''
    process_list: list[str] = get_attribute(rdf_module, 'processList', [])
    input_dir: str = get_attribute(rdf_module, 'inputDir', '')
    if not process_list:
        files_or_dirs = glob.glob(f'{input_dir}/*')
        process_list = [pathlib.Path(p).stem for p in files_or_dirs]
        info_msg = f'Found {len(process_list)} processes in the input ' \
                   'directory:'
        for process_name in process_list:
            info_msg += f'\n  - {process_name}'
        LOGGER.info(info_msg)

    return process_list


#------------------------------------------------------------------------------
def save_results(results: dict[str, dict[str, Any]],
                 rdf_module: object,
                 process_dict: dict[str, Any]) -> None:
    '''
    Save results into various formats, depending on the analysis script.
    '''
    output_dir: str = get_attribute(rdf_module, 'outputDir', '.')

    if get_attribute(rdf_module, 'saveJSON', False):
        json_path: str = os.path.join(output_dir, 'results.json')
        LOGGER.info('Saving results into JSON file:\n%s', json_path)
        save_json(results, json_path)

    if get_attribute(rdf_module, 'saveTabular', False):
        cut_labels: dict[str, str] = get_attribute(rdf_module, 'cutLabels',
                                                   None)
        tables_path: str = os.path.join(output_dir, '0.outputTabular.tex')
        LOGGER.info('Saving results in LaTeX tables to:\n%s', tables_path)
        save_tables(results, tables_path, process_dict, cut_labels)


#------------------------------------------------------------------------------
def save_json(results: dict[str, dict[str, Any]],
              outpath: str) -> None:
    '''
    Save results into a JSON file.
    '''
    with open(outpath, 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile)


# ------------------------------------------------------------------------------
def save_tables(results: dict[str, dict[str, Any]],
                           outpath: str,
                           process_dict: dict[str, Any],
                           cut_labels: dict[str, str] = None) -> None:

    def latex_safe(s: str) -> str:
        return (s.replace(">=", "$\\geq$")
                 .replace("<=", "$\\leq$")
                 .replace("#", "\\#"))

    cut_names = list(results[next(iter(results))].keys())
    if not cut_names:
        raise ValueError("No results found")

    if cut_labels is None:
        cut_labels = {c: c for c in cut_names}

    cut_labels["all_events"] = "All events"

    signal_names = [n for n in results if "dark_photons" in n]
    background_names = [n for n in results if n not in signal_names]

    if len(signal_names) == 0:
        raise ValueError("No signal samples found")

    def get_mass(name: str) -> float:
        match = re.search(r"mZd(\d+)MeV", name)
        return float(match.group(1)) if match else 0.0

    def get_epsilon(name: str) -> float:
            match = re.search(r"_e_(.*)", name)
            try:
                return float(match.group(1)) if match else 0.0
            except ValueError:
                return 0.0

    signal_names.sort(key=lambda n: (get_mass(n), get_epsilon(n)))
    
    if len(background_names) == 0:
        background_names = []

    def get_bkg(cut):
        return sum(results[b][cut]["n_events"] for b in background_names)

    def get_bkg_unc(cut):
        return math.sqrt(sum(results[b][cut]["uncertainty"] ** 2 for b in background_names))


    with open(outpath, "w", encoding="utf-8") as outfile:
        outfile.write("\\begin{table}[H]\n")
        outfile.write("\\centering\n")
        outfile.write("\\resizebox{\\textwidth}{!}{\n")

        n_sig = len(signal_names)

        col_format = "|l||" + "c|" * n_sig + "c||" + "c|" * n_sig + "|"
        outfile.write(f"\\begin{{tabular}}{{{col_format}}} \\hline\n")

        #Header
        outfile.write(" & ")
        outfile.write(f"\\multicolumn{{{n_sig}}}{{c|}}{{\\textbf{{Signal}}}} & ")

        if background_names:
            outfile.write("\\textbf{Bkg} & ")
        else:
            outfile.write("\\textbf{No Bkg} & ")

        outfile.write(f"\\multicolumn{{{n_sig}}}{{c|}}{{\\textbf{{$S/\\sqrt{{S+B}}$}}}} \\\\ \\hline\n")

        #Signal labels
        outfile.write("\\textbf{Selection}")

        for sig in signal_names:
            match = re.search(r"mZd(\d+)", sig)
            label = f"{match.group(1)} MeV" if match else sig
            outfile.write(f" & \\textbf{{{latex_safe(label)}}}")

        if background_names:
            outfile.write(" & \\textbf{Background}")
        else:
            outfile.write(" & -")

        for sig in signal_names:
            match = re.search(r"mZd(\d+)", sig)
            label = f"{match.group(1)} MeV" if match else sig
            outfile.write(f" & \\textbf{{{latex_safe(label)}}}")

        for sig in signal_names:
            match = re.search(r"mZd(\d+)", sig)
            label = f"{match.group(1)} MeV" if match else sig
            outfile.write(f" & \\textbf{{{latex_safe(label)}}}")

        outfile.write(" \\\\ \\hline \\hline\n")

        #Cross sections
        outfile.write("\\textbf{Cross Section [pb]}")
        for _ in signal_names:
            outfile.write(" & -")
        outfile.write(" & -")
        for _ in signal_names:
            outfile.write(" & -")
        for _ in signal_names:
            outfile.write(" & -")
        outfile.write(" \\\\ \\hline \\hline\n")

        for cut in cut_names:
            label = latex_safe(cut_labels.get(cut, cut))
            outfile.write(label)

            s_vals = []
            for sig in signal_names:
                s = results[sig][cut]["n_events"]
                u = results[sig][cut]["uncertainty"]

                s_vals.append(s)
                outfile.write(f" & {s:.2f} $\\pm$ {u:.2f}")

            if background_names:
                b = get_bkg(cut)
                b_u = get_bkg_unc(cut)
                outfile.write(f" & {b:.2f} $\\pm$ {b_u:.2f}")
            else:
                b = 0.0
                outfile.write(" & -")

            #S/sqrt(S+B)
            for s in s_vals:
                if (s + b) > 0:
                    sig = s / math.sqrt(s + b)
                    outfile.write(f" & {sig:.3f}")
                else:
                    outfile.write(" & -")

            if cut in ["Preselection", "Total_Selection"]:
                outfile.write(" \\\\ \\hline\n")
            else:
                outfile.write(" \\\\\n")
                
        #Footer
        outfile.write("\\end{tabular}\n")
        outfile.write("}\n")
        outfile.write("\\caption{Signal yields, background, $S/B$, and $S/\\sqrt{S+B}$.}\n")
        outfile.write("\\label{tab:final_significance_updated}\n")
        outfile.write("\\end{table}\n")

       
# #------------------------------------------------------------------------------
# def save_tables(results: dict[str, dict[str, Any]],
#                            outpath: str,
#                            process_dict: dict[str, Any],
#                            cut_labels: dict[str, str] = None) -> None:

#     def latex_safe(s: str) -> str:
#         return (s.replace(">=", "$\\geq$")
#                  .replace("<=", "$\\leq$")
#                  .replace("#", "\\#"))

#     #Keep only selected cuts
#     selected_cuts = ["selNone", "Preselection", "Total_Selection"]
#     available_cuts = list(results[next(iter(results))].keys())
#     cut_names = [c for c in selected_cuts if c in available_cuts]

#     if not cut_names:
#         raise ValueError("Required cuts not found in results")

#     if cut_labels is None:
#         cut_labels = {
#             "selNone":          r"Before Selection",
#             "Preselection":     r"Preselection",
#             "Total_Selection" : r"Total Selection",
#     }

#     signal_names = [n for n in results if "dark_photons" in n]
#     background_names = [n for n in results if n not in signal_names]

#     if len(signal_names) == 0:
#         raise ValueError("No signal samples found")

#     def get_mass(name: str) -> float:
#         match = re.search(r"mZd(\d+)MeV", name)
#         return float(match.group(1)) if match else 0.0

#     def get_epsilon(name: str) -> float:
#             match = re.search(r"_e_(.*)", name)
#             try:
#                 return float(match.group(1)) if match else 0.0
#             except ValueError:
#                 return 0.0

#     signal_names.sort(key=lambda n: (get_mass(n), get_epsilon(n)))
    
#     if len(background_names) == 0:
#         background_names = []

#     def get_bkg(cut):
#         return sum(results[b][cut]["n_events"] for b in background_names)

#     def get_bkg_unc(cut):
#         return math.sqrt(sum(results[b][cut]["uncertainty"] ** 2 for b in background_names))


#         # --- LaTeX Export ---
#     latex_header = r"""
#     \begin{longtable}[c]{|c|c|c||c|c|c|}
#     \caption{Signal yields after each respective selection cut.} \label{tab:yields_all_signal} \\
#     \hline
#     \textbf{mass [GeV]} & $\varepsilon$ & $\sigma$ [pb] & \textbf{Before selection} & \textbf{Preselection} & \textbf{Total Selection} \\ \hline
#     \endfirsthead
#     \hline
#     \textbf{mass [GeV]} & $\varepsilon$ & $\sigma$ [pb] & \textbf{Before selection} & \textbf{Preselection} & \textbf{Total Selection} \\ \hline
#     \endhead
#     """
#     with open(outpath, "w", encoding="utf-8") as outfile:
#         outfile.write(latex_header)

#         last_mass = None

#         #Signal rows
#         for sig in signal_names:
#             current_mass = get_mass(sig)
            
#             #Draw a hline between different mass groups
#             if last_mass is not None and current_mass != last_mass:
#                 outfile.write(r"\hline" + "\n")
#             last_mass = current_mass

#             #Extract mass and epsilon string
#             match = re.search(r"mZd(\d+)MeV_e_(.*)", sig)
            
#             xsec = process_dict[sig].get("crossSection", 0.0)
#             if match:
#                 mev_val = int(match.group(1))
#                 gev_val = mev_val / 1000.0
#                 epsilon_raw = match.group(2)
#                 epsilon_formatted = epsilon_raw.replace("e", r"\times 10^{") + "}" if "e" in epsilon_raw else epsilon_raw
#                 outfile.write(f"{gev_val:g} & ${epsilon_formatted}$ & {xsec}")
#             else:
#                 # Fallback
#                 outfile.write(f"{sig} & -")

#             for cut in cut_names:
#                 s = results[sig][cut]["n_events"]
#                 u = results[sig][cut]["uncertainty"]
#                 outfile.write(f" & {s:.2f} $\\pm$ {u:.2f}")
                
#             outfile.write(r" \\" + "\n")

#         # Table Footer        
#         outfile.write(r"\hline" + "\n")
#         outfile.write(r"\end{longtable}" + "\n")
#----------------------------------------------------------------------------------------

def run(rdf_module, args) -> None:
    '''
    Let's start.
    '''
    # Load process dictionary
    proc_dict_location: str = get_attribute(rdf_module, "procDict", '')
    if not proc_dict_location:
        LOGGER.error(
            'Location of the process dictionary not provided!\nAborting...')
        sys.exit(3)

    process_dict: dict[str, Any] = get_process_dict(proc_dict_location)

    # Add processes into the dictionary
    process_dict_additions = get_attribute(rdf_module, "procDictAdd", {})
    if process_dict_additions:
        info_msg = 'Adding the following processes to the process dictionary:'
        for process_name, process_info in process_dict_additions.items():
            info_msg += f'\n  - {process_name}'
            if process_name in process_dict:
                LOGGER.debug('Process "%s" already in the dictionary.\n'
                             'Will be overwritten...', process_name)
            process_dict[process_name] = process_info
        LOGGER.info(info_msg)

    # Set multi-threading
    ncpus = get_attribute(rdf_module, "nCPUS", 4)
    if ncpus < 0:  # use all available threads
        ROOT.EnableImplicitMT()
        ncpus = ROOT.GetThreadPoolSize()
    if ncpus != 1:
        ROOT.ROOT.EnableImplicitMT(ncpus)
        ROOT.EnableThreadSafety()

    nevents_real = 0
    start_time = time.time()

    process_events = {}
    events_ttree = {}
    file_list = {}
    results = {}

    # Checking input directory
    input_dir = get_attribute(rdf_module, 'inputDir', '')
    if not input_dir:
        LOGGER.error('The "inputDir" variable is mandatory for the final '
                     'stage of the analysis!\nAborting...')
        sys.exit(3)
    if not os.path.isdir(input_dir):
        LOGGER.error('The specified input directory does not exist!\n'
                     'Aborting...')
        LOGGER.error('Input directory: %s', input_dir)
        sys.exit(3)

    if input_dir[-1] != "/":
        input_dir += "/"

    # Checking output directory
    output_dir = get_attribute(rdf_module, 'outputDir', '.')

    if output_dir[-1] != "/":
        output_dir += "/"

    if not os.path.exists(output_dir):
        LOGGER.debug('Creating output directory:\n  %s', output_dir)
        os.system(f'mkdir -p {output_dir}')

    # Cuts
    cuts: dict[str, str] = get_attribute(rdf_module, "cutList", {})

    # Find processes (samples) to run over
    process_list: list[str] = get_processes(rdf_module)

    # Find number of events per process
    for process_name in process_list:
        process_events[process_name] = 0
        events_ttree[process_name] = 0
        file_list[process_name] = ROOT.vector('string')()

        infilepath = input_dir + process_name + '.root'  # input file
        if not os.path.isfile(infilepath):
            LOGGER.debug('File %s does not exist!\nTrying if it is a '
                         'directory as it might have been processed in batch.',
                         infilepath)
        else:
            LOGGER.info('Open file:\n  %s', infilepath)
            process_events[process_name], events_ttree[process_name] = \
                get_entries(infilepath)
            file_list[process_name].push_back(infilepath)

        indirpath = input_dir + process_name

        if os.path.isdir(indirpath):
            info_msg = f'Open directory {indirpath}'
            flist = glob.glob(indirpath + '/chunk*.root')
            if len(flist) > 0:
                for filepath in flist:
                    info_msg += '\n\t' + filepath
                    chunk_process_events, chunk_events_ttree = \
                        get_entries(filepath)
                    process_events[process_name] += chunk_process_events
                    events_ttree[process_name] += chunk_events_ttree
                    file_list[process_name].push_back(filepath)
            
            else:
                root_files = glob.glob(indirpath + '/*.root')

                if len(root_files) == 0:
                    LOGGER.warning(f'No ROOT files found in {indirpath}')
                else:
                    for filepath in root_files:
                        info_msg += '\n\t' + filepath

                        nevt, ntree = get_entries(filepath)

                        process_events[process_name] += nevt
                        events_ttree[process_name] += ntree
                        file_list[process_name].push_back(filepath)

            LOGGER.info(info_msg)

    info_msg = 'Processed events:'
    for process_name, n_events in process_events.items():
        info_msg += f'\n\t- {process_name}: {n_events:,}'
    LOGGER.info(info_msg)
    info_msg = 'Events in the TTree:'
    for process_name, n_events in events_ttree.items():
        info_msg += f'\n\t- {process_name}: {n_events:,}'
    LOGGER.info(info_msg)

    # Check if there are any histograms defined
    histo_list: dict[str, dict[str, Any]] = get_attribute(rdf_module,
                                                          "histoList", {})
    if not histo_list:
        LOGGER.error('No histograms defined!\nAborting...')
        sys.exit(3)

    # Check whether to scale the results to the luminosity
    do_scale = get_attribute(rdf_module, "doScale", True)
    if do_scale:
        int_lumi = get_attribute(rdf_module, "intLumi", 1.)
        if int_lumi < 0.:
            LOGGER.error('Integrated luminosity value not valid!\nAborting...')
            sys.exit(3)

    # Check whether to save resulting TTree(s) into a file(s)
    do_tree = get_element(rdf_module, "doTree", True)

    # Main loop
    for process_name in process_list:
        LOGGER.info('Running over process: %s', process_name)

        if process_events[process_name] <= 0:
            LOGGER.error('Can\'t scale histograms, the number of processed '
                         'events for the process "%s" seems to be zero!',
                         process_name)
            sys.exit(3)

        dframe = ROOT.ROOT.RDataFrame("events", file_list[process_name])
        define_list = get_element(rdf_module, "defineList", True)
        if len(define_list) > 0:
            LOGGER.info('Registering extra DataFrame defines...')
            for define in define_list:
                dframe = dframe.Define(define, define_list[define])

        fout_list = []
        histos_list = []
        snapshots = []
        count_list = []
        cuts_list = []
        cuts_list.append(process_name)
        eff_list = []
        eff_list.append(process_name)
        results[process_name] = {}

        if do_scale:
            # Get process information from process directory
            try:
                xsec = process_dict[process_name]["crossSection"]
                br_sf = process_dict[process_name].get("scaleFactor", 1.0)
                br_sfH = process_dict[process_name].get("scaleFactorHiggs", 1.0)
                BR = process_dict[process_name].get("BR", 1.0)
            except KeyError:
                xsec = 1.0
                br_sf = 1.0
                br_sfH = 1.0   
                BR = 1.0

                LOGGER.warning('Cross-section value not found for process '
                               '"%s"!\nUsing 1.0...', process_name)

            try:
                kfactor = process_dict[process_name]["kfactor"]
            except KeyError:
                kfactor = 1.0
                LOGGER.warning('Kfactor value not found for process "%s"!\n'
                               'Using 1.0...', process_name)

            try:
                matching_efficiency = \
                    process_dict[process_name]["matchingEfficiency"]
            except KeyError:
                matching_efficiency = 1.0
                LOGGER.warning('Matching efficiency value not found for '
                               'process "%s"!\nUsing 1.0...', process_name)

            gen_sf = xsec * kfactor * matching_efficiency
            lpn = len(process_name) + 8
            LOGGER.info('Generator scale factor for "%s": %.4g',
                        process_name, gen_sf)
            LOGGER.info(' - cross-section:      ' + lpn*' ' + '%.4g pb',
                        xsec)
            LOGGER.info(' - kfactor:            ' + lpn*' ' + '%.4g', kfactor)
            LOGGER.info(' - matching efficiency:' + lpn*' ' + '%.4g',
                        matching_efficiency)
            LOGGER.info('Integrated luminosity: %.4g pb-1', int_lumi)

        # Define all histos, snapshots, etc...
        LOGGER.info('Defining cuts and histograms')
        for cut_name, cut_definition in cuts.items():
            try:
                dframe_cut = dframe.Filter(cut_definition)
            except cppyy.gbl.std.runtime_error:
                LOGGER.error('During defining of the cuts an error '
                             'occurred!\nAborting...')
                sys.exit(3)

            count_list.append(dframe_cut.Count())

            histos = []
            for hist_name, hist_definition in histo_list.items():
                # default 1D histogram, looks for the name of the column.
                if "name" in hist_definition:
                    model = ROOT.RDF.TH1DModel(
                        hist_name,
                        f';{hist_definition["title"]};',
                        hist_definition["bin"],
                        hist_definition["xmin"],
                        hist_definition["xmax"])
                    histos.append(dframe_cut.Histo1D(model,
                                                     hist_definition["name"]))
                # multi dim histogram (1, 2 or 3D)
                elif "cols" in hist_definition:
                    cols = hist_definition['cols']
                    bins = hist_definition['bins']
                    if len(bins) != len(cols):
                        LOGGER.error('Amount of columns should be equal to '
                                     'the amount of bin configs!\nAborting...')
                        sys.exit(3)
                    bins_unpacked = tuple(i for sub in bins for i in sub)
                    if len(cols) == 1:
                        histos.append(dframe_cut.Histo1D(
                            (hist_name, '', *bins_unpacked), *cols))
                    elif len(cols) == 2:
                        histos.append(dframe_cut.Histo2D(
                            (hist_name, "", *bins_unpacked), *cols))
                    elif len(cols) == 3:
                        histos.append(dframe_cut.Histo3D(
                            (hist_name, "", *bins_unpacked), *cols))
                    else:
                        LOGGER.error('Only 1, 2 or 3D histograms supported.')
                        sys.exit(3)
                else:
                    LOGGER.error('Error parsing the histogram config. Provide '
                                 'either name or cols.')
                    sys.exit(3)
            histos_list.append(histos)

            if do_tree:
                # output file for the TTree
                fout = os.path.join(output_dir,
                                    process_name + '_' + cut_name + '.root')
                fout_list.append(fout)

                opts = ROOT.RDF.RSnapshotOptions()
                opts.fLazy = True
                # Snapshots need to be kept in memory until the event loop is
                # run
                snapshots.append(dframe_cut.Snapshot("events", fout, "", opts))

        # Now perform the loop and evaluate everything at once.
        LOGGER.info('Evaluating...')
        all_events_raw = dframe.Count().GetValue()
        LOGGER.info('Done')

        nevents_real += all_events_raw
        uncertainty = ROOT.Math.sqrt(all_events_raw)

        if do_scale:
            LOGGER.info('Scaling cut yields...')
            all_events = all_events_raw * 1. * gen_sf * int_lumi / process_events[process_name]
            #all_events = all_events_raw * 1. * 2.2*10**6 * 69.91*10**(-2) * 10**(-3) * BR**2 / process_events[process_name]
            uncertainty = ROOT.Math.sqrt(all_events_raw) * gen_sf * int_lumi / process_events[process_name]
            #uncertainty = ROOT.Math.sqrt(all_events_raw) * 2.2*10**6 * 69.91*10**(-2) * 10**(-3) * BR**2 / process_events[process_name]

        else:
            all_events = all_events_raw
            uncertainty = ROOT.Math.sqrt(all_events_raw)



        results[process_name]['all_events'] = {}
        results[process_name]['all_events']['n_events_raw'] = all_events_raw
        results[process_name]['all_events']['n_events'] = all_events
        results[process_name]['all_events']['uncertainty'] = uncertainty

        for i, cut in enumerate(cuts):
            cut_result = {}
            cut_result['n_events_raw'] = count_list[i].GetValue()
            if do_scale:
                cut_result['n_events'] = cut_result['n_events_raw'] * 1. * gen_sf * int_lumi / process_events[process_name]
                #cut_result['n_events'] = cut_result['n_events_raw'] * 2.2*10**6 * 69.91*10**(-2) * 10**(-3) * BR**2 / process_events[process_name]
                cut_result['uncertainty'] = math.sqrt(cut_result['n_events_raw']) * gen_sf  * int_lumi / process_events[process_name]
                #cut_result['uncertainty'] = math.sqrt(cut_result['n_events_raw']) * 2.2*10**6 * 69.91*10**(-2) * 10**(-3) * BR**2 / process_events[process_name]
            else:
                cut_result['n_events'] = cut_result['n_events_raw']
                cut_result['uncertainty'] = math.sqrt(cut_result['n_events_raw'])
            results[process_name][cut] = cut_result

        # Cut name width
        cn_width = max(len(cn) for cn in results[process_name].keys())
        info_msg = 'Cutflow:\n'
        info_msg += '    ' + cn_width * ' ' + '        Raw events'
        if do_scale:
            info_msg += '    Scaled events'
        for cut_name, cut_result in results[process_name].items():
            if cut_name == 'all_events':
                cut_name = 'All events'
            info_msg += f'\n  - {cut_name:{cn_width}} '
            info_msg += f' {cut_result["n_events_raw"]:>16,}'
            if do_scale:
                if cut_result['n_events_raw'] != 0:
                    info_msg += f' {cut_result["n_events"]:>16.2e}'
                else:
                    info_msg += f' {"0.":>16}'

        LOGGER.info(info_msg)

        if args.graph:
            generate_graph(dframe, args)
            args.graph = False

        # And save everything
        LOGGER.info('Saving the outputs...')
        if do_scale:
            LOGGER.info('Scaling the histograms...')
        for i, cut in enumerate(cuts):
            # output file for histograms
            fhisto = os.path.join(output_dir,
                                  process_name + '_' + cut + '_histo.root')
            with ROOT.TFile(fhisto, 'RECREATE') as outfile:
                for hist in histos_list[i]:
                    hist_name = hist.GetName() + '_raw'
                    outfile.WriteObject(hist.GetValue(), hist_name)
                    if do_scale:
                        hist.Scale(gen_sf * int_lumi / process_events[process_name])
                        #hist.Scale(2.2*10**6 * 69.91*10**(-2) * 10**(-3) * BR**2 / process_events[process_name])
                    outfile.WriteObject(hist.GetValue(), hist.GetName())

                # write all metadata info to the output file
                param = ROOT.TParameter(int)("eventsProcessed",
                                             process_events[process_name])
                outfile.WriteObject(param, param.GetName())

                param = ROOT.TParameter(float)("sumOfWeights",
                                               process_events[process_name])
                outfile.WriteObject(param, param.GetName())

                param = ROOT.TParameter(bool)("scaled",
                                              do_scale)
                outfile.WriteObject(param, param.GetName())

                if do_scale:
                    param = ROOT.TParameter(float)("intLumi", int_lumi)
                    outfile.WriteObject(param, param.GetName())

                    param = ROOT.TParameter(float)("crossSection", xsec)
                    outfile.WriteObject(param, param.GetName())
                    
                    param = ROOT.TParameter(float)("scaleFactor", br_sf)
                    outfile.WriteObject(param, param.GetName())
                    
                    param = ROOT.TParameter(float)("BR", BR)
                    outfile.WriteObject(param, param.GetName())
                    
                    param = ROOT.TParameter(float)("scaleFactorHiggs", br_sfH)
                    outfile.WriteObject(param, param.GetName())

                    param = ROOT.TParameter(float)("kfactor", kfactor)
                    outfile.WriteObject(param, param.GetName())

                    param = ROOT.TParameter(float)("matchingEfficiency",
                                                   matching_efficiency)
                    outfile.WriteObject(param, param.GetName())

                    param = ROOT.TParameter(float)("generatorScaleFactor",
                                                   gen_sf)
                    outfile.WriteObject(param, param.GetName())
            if do_tree:
                # add meta info to the tree file
                fout = os.path.join(output_dir,
                                    process_name + '_' + cut + '.root')
                with ROOT.TFile(fout, 'UPDATE') as outfile:
                    # write all metadata info to the output file
                    param = ROOT.TParameter(int)("eventsProcessed",
                                                 process_events[process_name])
                    outfile.WriteObject(param, param.GetName())

                    param = ROOT.TParameter(float)("sumOfWeights",
                                                   process_events[process_name])
                    outfile.WriteObject(param, param.GetName())

                    param = ROOT.TParameter(bool)("scaled",
                                                  do_scale)
                    outfile.WriteObject(param, param.GetName())

                    if do_scale:
                        param = ROOT.TParameter(float)("intLumi", int_lumi)
                        outfile.WriteObject(param, param.GetName())

                        param = ROOT.TParameter(float)("crossSection", xsec)
                        outfile.WriteObject(param, param.GetName())

                        param = ROOT.TParameter(float)("scaleFactor", br_sf)
                        outfile.WriteObject(param, param.GetName())

                        param = ROOT.TParameter(float)("scaleFactorHiggs", br_sfH)
                        outfile.WriteObject(param, param.GetName())

                        param = ROOT.TParameter(float)("kfactor", kfactor)
                        outfile.WriteObject(param, param.GetName())

                        param = ROOT.TParameter(float)("matchingEfficiency",
                                                       matching_efficiency)
                        outfile.WriteObject(param, param.GetName())

                        param = ROOT.TParameter(float)("generatorScaleFactor",
                                                       gen_sf)
                        outfile.WriteObject(param, param.GetName())

                # Number of events from a particular cut
                nevt_cut = results[process_name][cut]['n_events_raw']
                # Number of events in file
                try:
                    nevt_infile = snapshots[i].Count().GetValue()
                except cppyy.gbl.std.runtime_error:
                    nevt_infile = 0

                if nevt_cut != nevt_infile:
                    LOGGER.error('Number of events for cut "%s" in sample '
                                 '"%s" does not match with number of saved '
                                 'events!', cut, process_name)
                    sys.exit(3)

    # Save results either to JSON or LaTeX tables
    save_results(results, rdf_module, process_dict)

    elapsed_time = time.time() - start_time

    info_msg = f"\n{' SUMMARY ':=^80}\n"
    info_msg += 'Elapsed time (H:M:S):    '
    info_msg += time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    info_msg += '\nEvents processed/second: '
    info_msg += f'{int(nevents_real/elapsed_time):,}'
    info_msg += f'\nTotal events processed:  {nevents_real:,}'
    info_msg += '\n'
    info_msg += 80 * '='
    info_msg += '\n'
    LOGGER.info(info_msg)

#------------------------------------------------------------------------------
def run_final(parser):
    '''
    Run final stage of the analysis.
    '''

    args, _ = parser.parse_known_args()

    if args.command != 'final':
        LOGGER.error('Unknown sub-command "%s"!\nAborting...', args.command)
        sys.exit(3)

    # Check that the analysis file exists
    anapath = args.anascript_path
    if not os.path.isfile(anapath):
        LOGGER.error('Analysis script "%s" not found!\nAborting...',
                     anapath)
        sys.exit(3)

    # Load pre compiled analyzers
    LOGGER.info('Loading analyzers from libFCCAnalyses...')
    ROOT.gSystem.Load("libFCCAnalyses")
    # Is this still needed?? 01/04/2022 still to be the case
    _fcc = ROOT.dummyLoader
    LOGGER.debug(_fcc)

    # Set verbosity level
    if args.verbose:
        # ROOT.Experimental.ELogLevel.kInfo verbosity level is more
        # equivalent to DEBUG in other log systems
        LOGGER.debug('Setting verbosity level "kInfo" for RDataFrame...')
        verbosity = ROOT.Experimental.RLogScopedVerbosity(
            ROOT.Detail.RDF.RDFLogChannel(),
            ROOT.Experimental.ELogLevel.kInfo)
        LOGGER.debug(verbosity)
    if args.more_verbose:
        LOGGER.debug('Setting verbosity level "kDebug" for RDataFrame...')
        verbosity = ROOT.Experimental.RLogScopedVerbosity(
            ROOT.Detail.RDF.RDFLogChannel(),
            ROOT.Experimental.ELogLevel.kDebug)
        LOGGER.debug(verbosity)
    if args.most_verbose:
        LOGGER.debug('Setting verbosity level "kDebug+10" for '
                     'RDataFrame...')
        verbosity = ROOT.Experimental.RLogScopedVerbosity(
            ROOT.Detail.RDF.RDFLogChannel(),
            ROOT.Experimental.ELogLevel.kDebug+10)
        LOGGER.debug(verbosity)

    # Load the analysis
    anapath_abs = os.path.abspath(anapath)
    LOGGER.info('Loading analysis script:\n%s', anapath_abs)
    rdf_spec = importlib.util.spec_from_file_location('rdfanalysis',
                                                      anapath_abs)
    rdf_module = importlib.util.module_from_spec(rdf_spec)
    rdf_spec.loader.exec_module(rdf_module)

    # Merge configuration from analysis script file with command line arguments
    if get_element(rdf_module, 'graph'):
        args.graph = True

    if get_element(rdf_module, 'graphPath') != '':
        args.graph_path = get_element(rdf_module, 'graphPath')

    run(rdf_module, args)
