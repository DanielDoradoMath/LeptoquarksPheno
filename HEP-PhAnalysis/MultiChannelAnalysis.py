import os
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

class MultiChannelAnalysis():
    pass