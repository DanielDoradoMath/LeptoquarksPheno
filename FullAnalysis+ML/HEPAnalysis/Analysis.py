import os
import csv
from ROOT import *
import pandas as pd
from HEPAnalysis.Particle import Particle
from HEPAnalysis.Particle import JetVector
from HEPAnalysis.Particle import MuonVector
from HEPAnalysis.Particle import ElectronVector
from etaprogress.progress import ProgressBar

class DelphesSignal():
    def __init__(self, signal_name=None):
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
        self.declareHistos()


    def declareHistos(self):
        self.hist_list=TList()

        def defineHisto(name, title, x_label, y_label, bins, lo, hi):
            h=TH1F(name, "{}; {}; {}".format(title, x_label, y_label), bins, lo, hi)
            h.SetDirectory(0)
            self.hist_list.Add(h)

        #cutflow histogram to record the absolute efficiency of each cut
        defineHisto('e-cutflow', 'Cutflow (electrons)', 'Cut', 'Events', 10, 0, 10)
        defineHisto('mu-cutflow', 'Cutflow (muons)', 'Cut', 'Events', 10, 0, 10)
        #CutFlowHist

        #Histogram to record  Number of Jets  reported by Delphes
        defineHisto('n_jets', 'Number of Jets', 'Jet multiplicity', 'Events', 10, 0, 10)
        
        #Histogram to record  Number of good Jets reconstructed
        defineHisto('n_good_jets',
            'Number of Good Jets', 'Jet multiplicity', 'Events',
            10,0,10
        )

        return self.hist_list
        
    def getTree(self,path, bkg=False):
        path_to_signal=path
        tree = TChain('Delphes;1')
        if not(bkg):
            ev_dir = path_to_signal + "/Events/"
            dirs=next(os.walk(ev_dir))[1]
            for folder in dirs :
                directory = str(folder+'/tag_1_delphes_events.root')
                tree.Add(ev_dir + directory)
            return tree
        else:
            ev_dir=path
            dirs=next(os.walk(ev_dir))[1]
            for folder in dirs :
                if (folder !="Cards" and folder != "ParamCard"):
                    directory=ev_dir+folder
                    directory+= "/Events/run_01"  +"/m_delphes_events.root"
                    tree.Add(directory)
            return tree


    # def writelist(self):
    #     os.system("rm -rf {self.name}.root")
    #     f =TFile(self.name+".root","RECREATE")
    #     self.hist_list.Write("histlist", TObject.kSingleKey)
    #     f.ls()
    #     print(self.name+" Done!")
    

    def getGoodJets(self,event):
        part_dic = {
            'l_jets' : [],
            'b_jets' : [],
            'tau_jets' : [],
            'muons' : [],
            'electrons' : [],
            'other_jets' : [],
            'all_jets' : []
        }

        Ljet_Pt_cut=30.
        Ljet_Eta_cut=5.

        bjet_Pt_cut=30.
        bjet_Eta_cut=2.5

        taujet_Pt_cut=20.
        taujet_Eta_cut=2.5

        lepton_Pt_cut = 24.
        lepton_Eta_cut = 2.3

        n_jets=event.Jet.GetEntries()
        
        for j in range(n_jets):
            jet=JetVector(event, j)
            #Classify by type jet according to its Tag
            #apply its corresponding kinematic cut.
            if( jet.BTag==0 and jet.TauTag==0):
                ptcut= (jet.Pt()>= Ljet_Pt_cut)
                etacut= (abs(jet.Eta())<= Ljet_Eta_cut)
                if (ptcut and etacut ):
                    part_dic['l_jets'] += [jet]
            elif( jet.BTag==1 and jet.TauTag==0): 
                ptcut= (jet.Pt()>= bjet_Pt_cut)
                etacut= (abs(jet.Eta())<= bjet_Eta_cut)
                if (ptcut and etacut ):
                    part_dic['b_jets'] += [jet]
            elif( jet.BTag==0 and jet.TauTag==1): 
                ptcut= (jet.Pt()>= taujet_Pt_cut)
                etacut= (abs(jet.Eta())<= taujet_Eta_cut)
                if (ptcut and etacut ):
                    part_dic['tau_jets'] += [jet]
            else: 
                ptcut= (jet.Pt()>= Ljet_Pt_cut)
                etacut= (abs(jet.Eta())<= Ljet_Eta_cut)
                if (ptcut and etacut ):
                    part_dic['other_jets'] += [jet]

        n_muons = event.Muon.GetEntries()

        for i in range(n_muons):
            muon = MuonVector(event, i)
            ptcut= (muon.Pt()>= lepton_Pt_cut)
            etacut= (abs(muon.Eta())<= lepton_Eta_cut)
            if (ptcut and etacut ):
                part_dic['muons'] += [muon]

        n_electrons = event.Electron.GetEntries()

        for i in range(n_electrons):
            electron = ElectronVector(event, i)
            ptcut= (electron.Pt()>= lepton_Pt_cut)
            etacut= (abs(electron.Eta())<= lepton_Eta_cut)
            if (ptcut and etacut ):
                part_dic['electrons'] += [electron]
                
        part_dic['all_jets']+=part_dic['l_jets']
        part_dic['all_jets']+=part_dic['b_jets']
        part_dic['all_jets']+=part_dic['tau_jets']
        part_dic['all_jets']+=part_dic['other_jets']

        
        for key in part_dic:
            part_dic[key].sort(reverse = True, key = Particle.Pt)
        
        return part_dic


    def eventSelection(self):
        nEvents=self.tree.GetEntries()
        bar = ProgressBar(nEvents, max_width=60)
        printEachPercent=10.0
        bar.numerator = 0
        print(self.name, bar)
        nSplits=int(100/printEachPercent)
        last_printed=0

        try:
            os.system("mkdir DataFiles")
        except:
            pass

        f_electrons = open('DataFiles/'+self.name+"_electrons.csv", "w")
        f_muons = open('DataFiles/'+self.name+"_muons.csv", "w")

        column_names = ['M(b+tau)', 
                        'Pt(b+tau)',
                        'M(b+tau+MET)',
                        'Pt(b+tau+MET)',
                        'M(b+lpt)',
                        'Pt(b+lpt)',
                        'M(b+lpt+MET)',
                        'Pt(b+lpt+MET)',
                        'Pt(jet)',
                        'Pt(b-jet)',
                        'Pt(tau)',
                        'Pt(lpt)',
                        'eta(jet)',
                        'eta(b-jet)',
                        'eta(tau)',
                        'eta(lpt)',
                        'phi(jet)',
                        'phi(b-jet)',
                        'phi(tau)',
                        'phi(lpt)',
                        'vDeltaPT(jet b-jet)',
                        'vDeltaPT(jet tau)',
                        'vDeltaPT(jet lpt)',
                        'vDeltaPT(b-jet tau)',
                        'vDeltaPT(b-jet lpt)',
                        'vDeltaPT(tau lpt)',
                        'vDeltaP(jet b-jet)',
                        'vDeltaP(jet tau)',
                        'vDeltaP(jet lpt)',
                        'vDeltaP(b-jet tau)',
                        'vDeltaP(b-jet lpt)',
                        'vDeltaP(tau lpt)',
                        'sDeltaPT(jet b-jet)',
                        'sDeltaPT(jet tau)',
                        'sDeltaPT(jet lpt)',
                        'sDeltaPT(b-jet tau)',
                        'sDeltaPT(b-jet lpt)',
                        'sDeltaPT(tau lpt)',
                        'DeltaPhi(jet b-jet)',
                        'DeltaPhi(jet tau)',
                        'DeltaPhi(jet lpt)',
                        'DeltaPhi(b-jet tau)',
                        'DeltaPhi(b-jet lpt)',
                        'DeltaPhi(tau lpt)',
                        'DeltaEta(jet b-jet)',
                        'DeltaEta(jet tau)',
                        'DeltaEta(jet lpt)',
                        'DeltaEta(b-jet tau)',
                        'DeltaEta(b-jet lpt)',
                        'DeltaEta(tau lpt)',
                        'q(tau)*q(lpt)']

        header_row = ''
        for i, feature in enumerate(column_names):
            header_row+=str(feature)
            if i<len(column_names)-1:
                header_row+=","
        header_row+="\n"

        f_electrons.write(header_row)
        f_muons.write(header_row)


        
        for i, event in enumerate(self.tree):
            n_jets=event.Jet.GetEntries()
            self.hist_list.FindObject("e-cutflow").Fill(0)
            self.hist_list.FindObject("mu-cutflow").Fill(0)
            self.hist_list.FindObject("n_jets").Fill(n_jets)
                
            n_leptons = event.Electron.GetEntries() + event.Muon.GetEntries()
            
            if not(n_jets>2 and n_leptons>0): continue
            self.hist_list.FindObject("e-cutflow").Fill(1)
            self.hist_list.FindObject("mu-cutflow").Fill(1)
            
            #let's try to identify all the good jets
            jets = self.getGoodJets(event)

            # Update particle numbers with good jets
            n_jets = len(jets['all_jets'])
            n_leptons = len(jets['muons']) + len(jets['electrons'])

            self.hist_list.FindObject("n_good_jets").Fill(n_jets)
            
            #Discard events with less than two good jets
            if not (n_jets>2): continue
            self.hist_list.FindObject("e-cutflow").Fill(2)
            self.hist_list.FindObject("mu-cutflow").Fill(2)

            #Discard events without b-jets
            if not (len(jets['b_jets'])>0): continue
            self.hist_list.FindObject("e-cutflow").Fill(3)
            self.hist_list.FindObject("mu-cutflow").Fill(3)

            #Discard events without light-jets
            if not (len(jets['l_jets'])>0): continue
            self.hist_list.FindObject("e-cutflow").Fill(4)
            self.hist_list.FindObject("mu-cutflow").Fill(4)

            #Discard events without tau-jets
            if not (len(jets['tau_jets'])>0): continue
            self.hist_list.FindObject("e-cutflow").Fill(5)
            self.hist_list.FindObject("mu-cutflow").Fill(5)

            #Discard events with more than one tau-jet
            if not (len(jets['tau_jets'])==1): continue
            self.hist_list.FindObject("e-cutflow").Fill(6)
            self.hist_list.FindObject("mu-cutflow").Fill(6)

            #Discard events without leptons
            if not (n_leptons>0): continue
            self.hist_list.FindObject("e-cutflow").Fill(7)
            self.hist_list.FindObject("mu-cutflow").Fill(7)

            #Discard events with more than one lepton
            if not (n_leptons==1): continue
            self.hist_list.FindObject("e-cutflow").Fill(8)
            self.hist_list.FindObject("mu-cutflow").Fill(8)

            if len(jets['electrons'])==1:
                electronic = True
                self.hist_list.FindObject("e-cutflow").Fill(9)
                lepton = jets['electrons'][0]
                #Discard events in which the tau-jet and the lepton have the same charge
                qt1 =jets['tau_jets'][0].getCharge()
                qt2 =lepton.getCharge()
                if ( qt1*qt2>0 ): continue
                self.hist_list.FindObject("e-cutflow").Fill(10)
            else:
                electronic = False
                self.hist_list.FindObject("mu-cutflow").Fill(9)
                lepton = jets['muons'][0]
                #Discard events in which the tau-jet and the lepton have the same charge
                qt1 =jets['tau_jets'][0].getCharge()
                qt2 =lepton.getCharge()
                if ( qt1*qt2>0 ): continue
                self.hist_list.FindObject("mu-cutflow").Fill(10)
            
            
            j=jets['l_jets'][0]
            b=jets['b_jets'][0]
            tau=jets['tau_jets'][0]
            
            met=event.GetLeaf("MissingET.MET").GetValue()
            met_phi=event.GetLeaf("MissingET.Phi").GetValue()
            met_eta=event.GetLeaf("MissingET.Eta").GetValue()

            metTLV=TLorentzVector()
            metTLV.SetPtEtaPhiE(met,met_eta,met_phi,met)

            LQ = b.TLV + tau.TLV
            LQ_MET = LQ + metTLV
            LQ_lept = b.TLV + lepton.TLV
            LQ_leptMET = LQ_lept + metTLV
            row=[
                LQ.M(),
                LQ.Pt(),
                LQ_MET.M(),
                LQ_MET.Pt(),
                LQ_lept.M(),
                LQ_lept.Pt(),
                LQ_leptMET.M(),
                LQ_leptMET.Pt(),
                j.Pt(),
                b.Pt(),
                tau.Pt(),
                lepton.Pt(),
                j.Eta(),
                b.Eta(),
                tau.Eta(),
                lepton.Eta(),
                j.Phi(),
                b.Phi(),
                tau.Phi(),
                lepton.Phi(),
                j.vDeltaPT(b),
                j.vDeltaPT(tau),
                j.vDeltaPT(lepton),
                b.vDeltaPT(tau),
                b.vDeltaPT(lepton),
                tau.vDeltaPT(lepton), 
                j.vDeltaP(b),
                j.vDeltaP(tau),
                j.vDeltaP(lepton),
                b.vDeltaP(tau),
                b.vDeltaP(lepton),
                tau.vDeltaP(lepton),
                j.sDeltaPT(b),
                j.sDeltaPT(tau),
                j.sDeltaPT(lepton),
                b.sDeltaPT(tau),
                b.sDeltaPT(lepton),
                tau.sDeltaPT(lepton),
                j.DeltaPhi(b),
                j.DeltaPhi(tau),
                j.DeltaPhi(lepton),
                b.DeltaPhi(tau),
                b.DeltaPhi(lepton),
                tau.DeltaPhi(lepton),
                j.DeltaEta(b),
                j.DeltaEta(tau),
                j.DeltaEta(lepton),
                b.DeltaEta(tau),
                b.DeltaEta(lepton),
                tau.DeltaEta(lepton),
                qt1*qt2
            ]
            
            row_str = str(row)
            row_str = row_str[1:-1]
            row_str += "\n"

            if electronic:
                f_electrons.write(row_str)
            else:
                f_muons.write(row_str)
            
            if int(nSplits*(i)/nEvents)!=last_printed:
                last_printed=int(nSplits*i/nEvents)
                bar.numerator=i
        
        f_electrons.close()
        f_muons.close()
        print(self.name + ': selection done!')
        
        return self.hist_list
