from ROOT import *

class Particle():
    """
    Class for implementing particles in event detection. Uses pyROOT's 
    TLorentzVector to store values for the particle's kinematic variables.
    """
    def __init__(self):
        # Class init function. Sets atribute TLV to store kinematic info
        self.TLV=TLorentzVector()
 
    def GetTLV (self):    
        return self.TLV

    def Pt(self):
        # Returns transverse momentum
        TLV = self.TLV
        return TLV.Pt()
    
    def P(self):
        # Returns full momentum
        TLV = self.TLV
        return TLV.P()
    
    def Pl(self):
        # Returns longitudinal momentum
        p = self.TLV.P()
        pt= self.TLV.Pt()
        return TMath.Sqrt(p*p-pt*pt)

    def Eta(self):
        # Returns jet pseudorapidity
        TLV = self.TLV
        return TLV.Eta()

    def Phi(self):
        TLV = self.TLV
        return TLV.Phi()

    ### Delta methods

    def DeltaR(self, v2):
        TLV1 = self.TLV
        TLV2 = v2.GetTLV()
        return TLV1.DeltaR(TLV2)

    def DeltaEta(self, v2):
        return self.Eta() - v2.Eta()

    def DeltaPhi(self, v2):
        TLV1 = self.TLV
        TLV2 = v2.GetTLV()
        return TLV1.DeltaPhi(TLV2)

    def sDeltaPT(self, v2):
        return self.Pt() - v2.Pt()

    def vDeltaPT(self, v2):
        TLV1 = self.TLV
        TLV2 = v2.GetTLV()
        a=TVector2(TLV1.Px(), TLV1.Py())
        b=TVector2(TLV2.Px(), TLV2.Py())
        c=a-b
        return c.Mod()

    def vDeltaP(self,v2):
        TLV1 = self.TLV
        TLV2 = v2.GetTLV()
        a=TVector3(TLV1.Px(), TLV1.Py(), TLV1.Pz())
        b=TVector3(TLV2.Px(), TLV2.Py(), TLV2.Pz())
        c=a-b
        return c.Mag()

class JetVector(Particle):
    """
    Class for hadronic jets in event detection. 
    """
    def __init__(self, event, j):
        """
        Use super-class init function and receives parameters to set 
        the values for kinematic variables
        """
        super().__init__()
        self.TLV.SetPtEtaPhiM(
            event.GetLeaf("Jet.PT").GetValue(j), 
            event.GetLeaf("Jet.Eta").GetValue(j), 
            event.GetLeaf("Jet.Phi").GetValue(j), 
            event.GetLeaf("Jet.Mass").GetValue(j)
        )
        self.BTag   = event.GetLeaf("Jet.BTag").GetValue(j)
        self.Charge = event.GetLeaf("Jet.Charge").GetValue(j)
        self.TauTag = event.GetLeaf("Jet.TauTag").GetValue(j)
        
    def getCharge(self):
        return self.Charge

class MuonVector(Particle):
    def __init__(self, event, j):
        super().__init__()
        self.TLV.SetPtEtaPhiM(
            event.GetLeaf("Muon.PT").GetValue(j), 
            event.GetLeaf("Muon.Eta").GetValue(j), 
            event.GetLeaf("Muon.Phi").GetValue(j), 
            0.1056583755
        )
        self.Charge = event.GetLeaf("Muon.Charge").GetValue(j)

    ### Retrieval methods
    def getCharge(self):
        return self.Charge
    
class ElectronVector(Particle):
    def __init__(self, event, j):
        super().__init__()
        self.TLV.SetPtEtaPhiM(
            event.GetLeaf("Electron.PT").GetValue(j), 
            event.GetLeaf("Electron.Eta").GetValue(j), 
            event.GetLeaf("Electron.Phi").GetValue(j), 
            0.000511
        )
        self.Charge = event.GetLeaf("Electron.Charge").GetValue(j)
    
    ### Retrieval methods
    def getCharge(self):
        return self.Charge