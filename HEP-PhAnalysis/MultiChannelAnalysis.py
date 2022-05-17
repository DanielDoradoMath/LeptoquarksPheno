import os
import csv
import pandas as pd
from Particle import Particle
from Particle import JetVector
from Particle import MuonVector
from Particle import ElectronVector


# Dictionary structure containing observable name, name w/ units, min & max values
observableData = {'pt' : ('P_{t}', 'P_{t} (GeV)', 0., 1500.),
                  'eta': ('#eta', '#eta', -5., 5.),
                  'phi': ('#phi', '#phi', -3.5, 3.5),
                  'M': ('M', 'Reconstructed Mass (GeV)', 0., 2000.),
                  'DeltaEta': ('#Delta #eta', '#Delta #eta', -5., 5.),
                  'DeltaPhi': ('#Delta #phi', '#Delta #phi', -3.5, 3.5),
                  'DeltaPt': ('#Delta P_{t}', '#Delta P_{t} (GeV)', 0., 2000.)
                 }


observables = ['pt', 'eta', 'phi', 'M', 'DeltaEta', 'DeltaPhi', 'vDeltaPt', 'sDeltaPt']

class MultiChannelAnalysis():
    def __init__(self, signal_name = None, final_states = None):
        os.system("curl -O https://raw.githubusercontent.com/cfrc2694/Pheno_BSM/main/SimulationsPaths.csv")
        # Reading diccionary path
        data = {}
        with open("SimulationsPaths.csv", 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                name_signal_dict = row.pop(0)
                data[name_signal_dict] = [*row]
        self.name=signal_name
        
        # verify dictionary path
        if signal_name:
            try:
                path_to_signal = data[self.name][0] # Path
            except KeyError:
                raise Exception("Error: " + signal_name + " Signal not defined")
            bkg = data[self.name][1] # BKG
            bkg = True if bkg == "True" else False
        else:
            self.name="SingleLQ_500"
            path_to_signal = data[self.name][0]
            bkg = False
        
        self.tree = self.getTree(path_to_signal, bkg)
        load=self.name+" imported!\n"
        load+=str(self.tree.GetEntries()) + " events have been loaded from\n"
        load+=path_to_signal+"\n"
        print(load)

        self.final_states = final_states



    def getGoodJets(self, event):
        pass