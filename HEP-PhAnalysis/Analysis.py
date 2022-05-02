import os
import csv
from ROOT import *
from Particle import Particle
from Particle import JetVector
from Particle import MuonVector
from Particle import ElectronVector

class DelphesAnalysis():
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
        
        # verify dictionary path    Is name_signal bool?
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
        
        #Histograms to Record  the reconstructed mass of LQ
        defineHisto('m_LQ_tau1', 
            'M_{b+#tau} (electrons)', 'Reconstructed mass (GeV)', 'Events', 
            40, 0.0, 4000.0
        )
        defineHisto('m_LQ_tau2', 
            'M_{b+#tau} (muons)', 'Reconstructed mass (GeV)', 'Events', 
            40, 0.0, 4000.0
        )
        defineHisto('m_LQ_tau1_met', 
            'M_{b+#tau+MET}', 'Reconstructed mass (GeV)', 'Events', 
            40, 0.0, 4000.0
        )
        defineHisto('m_LQ_tau2_met', 
            'M_{b+#tau+MET}', 'Reconstructed mass (GeV)', 'Events', 
            40, 0.0, 4000.0
        )
        defineHisto('m_LQ_e', 
            'M_{b+e}', 'Reconstructed mass (GeV)', 'Events', 
            40, 0.0, 4000.0
        )
        defineHisto('m_LQ_e_met', 
            'M_{b+e+MET}', 'Reconstructed mass (GeV)', 'Events', 
            40, 0.0, 4000.0
        )
        defineHisto('m_LQ_mu', 
            'M_{b+#mu}', 'Reconstructed mass (GeV)', 'Events', 
            40, 0.0, 4000.0
        )
        defineHisto('m_LQ_mu_met', 
            'M_{b+#mu+MET}', 'Reconstructed mass (GeV)', 'Events', 
            40, 0.0, 4000.0
        )
        
        #Histograms to Record the pt of LQ

        defineHisto('pt_LQ1', 
            'Pt_{b+#tau} (electronic channel)', 'P_{t} (GeV)', 'Events', 
            40, 0.0, 2000.0
        )

        defineHisto('pt_LQ2', 
            'Pt_{b+#tau} (muonic channel)', 'P_{t} (GeV)', 'Events', 
            40, 0.0, 2000.0
        )
        
        defineHisto('pt_LQe', 
            'Pt_{b+e}', 'P_{t} (GeV)', 'Events', 
            40, 0.0, 2000.0
        )

        defineHisto('pt_LQmu', 
            'Pt_{b+#mu}', 'P_{t} (GeV)', 'Events', 
            40, 0.0, 2000.0
        )
        
        #Histograms to Record  the pt of all reconstructed jets
        
        defineHisto('pt_all_jets1', 
            'Pt_{all-jets} (electronic channel)', 'Pt(GeV)', 'Events', 
            40, 0.0, 2000.0
        )
        defineHisto('pt_all_jets2', 
            'Pt_{all-jets} (muonic channel)', 'Pt(GeV)', 'Events', 
            40, 0.0, 2000.0
        )
        
        defineHisto('pt_all_ljets1', 
            'Pt_{all-light-jets} (electronic channel)', 'Pt(GeV)', 'Events', 
            40, 0.0, 2000.0
        )
        defineHisto('pt_all_ljets2', 
            'Pt_{all-light-jets} (muonic channel)', 'Pt(GeV)', 'Events', 
            40, 0.0, 2000.0
        )
        
        defineHisto('pt_all_bjets1', 
            'Pt_{all-bjets} (electronic channel)', 'Pt(GeV)', 'Events', 
            40, 0.0, 2000.0
        )
        defineHisto('pt_all_bjets2', 
            'Pt_{all-bjets} (muonic channel)', 'Pt(GeV)', 'Events', 
            40, 0.0, 2000.0
        )
        
        defineHisto('pt_all_taujets1', 
            'Pt_{all-#tau jets} (electronic channel)', 'Pt(GeV)', 'Events', 
            40, 0.0, 2000.0
        )
        defineHisto('pt_all_taujets2', 
            'Pt_{all-#tau jets} (muonic channel)', 'Pt(GeV)', 'Events', 
            40, 0.0, 2000.0
        )
        
        #Histograms to Record  the eta of all reconstructed jets
        
        defineHisto('eta_all_jets1', 
            '#eta_{all-jets} (electronic channel)', '#eta', 'Events', 
            100, -5, 5
        )
        defineHisto('eta_all_jets2', 
            '#eta_{all-jets} (muonic channel)', '#eta', 'Events', 
            100, -5, 5
        )
        
        defineHisto('eta_all_ljets1', 
            '#eta_{all-light-jets} (electronic channel)', '#eta', 'Events', 
            100, -5, 5
        )
        defineHisto('eta_all_ljets2', 
            '#eta_{all-light-jets} (muonic channel)', '#eta', 'Events', 
            100, -5, 5
        )
        
        defineHisto('eta_all_bjets1', 
            '#eta_{all-bjets} (electronic channel)', '#eta', 'Events', 
            100, -5, 5
        )
        defineHisto('eta_all_bjets2', 
            '#eta_{all-bjets} (muonic channel)', '#eta', 'Events', 
            100, -5, 5
        )
        
        defineHisto('eta_all_taujets1', 
            '#eta_{all-#tau jets} (electronic channel)', '#eta', 'Events', 
            100, -5, 5
        )
        defineHisto('eta_all_taujets2', 
            '#eta_{all-#tau jets} (muonic channel)', '#eta', 'Events', 
            100, -5, 5
        )

        # f_states = ['b', 'tau', 'j', 'lpt', 'met']
        # observables = ['pt', 'eta', 'phi']
        # labels = ['P_{t} (GeV)', '#eta', '#phi']
        # bins = [30, 20, 20]
        # lims = [(0.0,1500.0), (-5,5), (-3.5,3.5)]

        # for i, obs in enumerate(observables[:-1]):
        #     for state in f_states[:-1]:
        #         histName = obs + '_' + state
        #         if obs=='pt':
        #             histTitle = 'P_{t}({state})'.format(state=state)
        #         else:
        #             histTitle = '{var} ({state})'.format(var=labels[i], state=state) 
        #         defineHisto(histName, histTitle, labels[i], 'Events', bins[i], lims[i][0], lims[i][1])

        #Histograms to record the pt of each output particle
        #############################
        defineHisto('pt_lead_ljet1', 
            'Pt_{j_{L}} (electronic channels)', 'P_{t} (GeV)', 'Events', 
            30, 0.0, 1500.0
        )
        defineHisto('pt_lead_ljet2', 
            'Pt_{j_{L}} (muonic channel)', 'P_{t} (GeV)', 'Events', 
            30, 0.0, 1500.0
        )

        defineHisto('pt_lead_bjet1', 
            'Pt_{b_{L}} (electronic channels)', 'P_{t} (GeV)', 'Events', 
            30, 0.0, 1500.0
        )
        defineHisto('pt_lead_bjet2', 
            'Pt_{b_{L}} (muonic channel)', 'P_{t} (GeV)', 'Events', 
            30, 0.0, 1500.0
        )
        
        defineHisto('pt_lead_tau1', 
            'Pt_{#tau} (electronic channels)', 'P_{t} (GeV)', 'Events', 
            30, 0.0, 1500.0
        )
        defineHisto('pt_lead_tau2', 
            'Pt_{#tau} (muonic channel)', 'P_{t} (GeV)', 'Events', 
            30, 0.0, 1500.0
        )

        defineHisto('pt_e', 
            'Pt_{e}', 'P_{t} (GeV)', 'Events', 
            30, 0.0, 1500.0
        )
        defineHisto('pt_mu', 
            'Pt_{#mu}', 'P_{t} (GeV)', 'Events', 
            30, 0.0, 1500.0
        )
        

        #############################
        #Histograms to record the eta of each output particle
        defineHisto('eta_lead_ljet1', 
            '#eta_{j_{L}}', '#eta', 'Events', 
            20, -5, 5
        )
        defineHisto('eta_lead_ljet2', 
            '#eta_{j_{L}}', '#eta', 'Events', 
            20, -5, 5
        )
        
        defineHisto('eta_lead_bjet1', 
            '#eta_{b_{L}}', '#eta', 'Events', 
            20, -5, 5
        )
        defineHisto('eta_lead_bjet2', 
            '#eta_{b_{L}}', '#eta', 'Events', 
            20, -5, 5
        )

        defineHisto('eta_lead_tau1', 
            '#eta_{#tau}', '#eta', 'Events', 
            20, -5, 5
        )
        defineHisto('eta_lead_tau2', 
            '#eta_{#tau}', '#eta', 'Events', 
            20, -5, 5
        )
        
        defineHisto('eta_e', 
            '#eta_{e}', '#eta', 'Events', 
            20, -5, 5
        )
        defineHisto('eta_mu', 
            '#eta_{#mu}', '#eta', 'Events', 
            20, -5, 5
        )
        
        #############################
        
        
        #Histograms to record the delta eta between each possible pair of jets
        
        defineHisto('deltaEta_tau_e',
            '#Delta #eta_{(#tau e)}', '#Delta #eta', 'Events',
            40,-5,5
        )

        defineHisto('deltaEta_tau_mu',
            '#Delta #eta_{(#tau #mu)}', '#Delta #eta', 'Events',
            40,-5,5
        )
        
        defineHisto('deltaEta_b_tau1',
            '#Delta #eta_{(b_{L} #tau_{L})} (electronic channel)', '#Delta #eta', 'Events',
            40,-5,5
        )
        defineHisto('deltaEta_b_tau2',
            '#Delta #eta_{(b_{L} #tau_{L})} (muonic channel)', '#Delta #eta', 'Events',
            40,-5,5
        )
        
        defineHisto('deltaEta_b_e',
            '#Delta #eta_{(b_{L} e)}', '#Delta #eta', 'Events',
            20,-5,5
        )
        defineHisto('deltaEta_b_mu',
            '#Delta #eta_{(b_{L} #mu)}', '#Delta #eta', 'Events',
            20,-5,5
        )


        defineHisto('deltaEta_j_tau1',
            '#Delta #eta_{(j_{L} #tau_{L})} (electronic channel)', '#Delta #eta', 'Events',
            40,-5,5
        )
        defineHisto('deltaEta_j_tau2',
            '#Delta #eta_{(j_{L} #tau_{L})} (muonic channel)', '#Delta #eta', 'Events',
            40,-5,5
        )
        
        defineHisto('deltaEta_j_e',
            '#Delta #eta_{(j_{L} e)}', '#Delta #eta', 'Events',
            40,-5,5
        )
        defineHisto('deltaEta_j_mu',
            '#Delta #eta_{(j_{L} #mu)}', '#Delta #eta', 'Events',
            40,-5,5
        )
        
        defineHisto('deltaEta_b_j1',
            '#Delta #eta_{(b_{L} j_{L})} (electronic channel)', '#Delta #eta', 'Events',
            40,-5,5
        )
        defineHisto('deltaEta_b_j2',
            '#Delta #eta_{(b_{L} j_{L})} (muonic channel)', '#Delta #eta', 'Events',
            40,-5,5
        )
        
        #############################
        
        #Histograms to record the delta phi between each possible pair of jets
        defineHisto('deltaPhi_tau_e',
            '#Delta #phi_{(#tau e)}', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        defineHisto('deltaPhi_tau_mu',
            '#Delta #phi_{(#tau #mu)}', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        
        defineHisto('deltaPhi_b_tau1',
            '#Delta #phi_{(b_{L} #tau_{L})} (electronic channel)', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        defineHisto('deltaPhi_b_tau2',
            '#Delta #phi_{(b_{L} #tau_{L})} (muonic channel)', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        
        defineHisto('deltaPhi_b_e',
            '#Delta #phi_{(b_{L} e)}', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        defineHisto('deltaPhi_b_mu',
            '#Delta #phi_{(b_{L} #mu)}', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        
        defineHisto('deltaPhi_j_tau1',
            '#Delta #phi_{(j_{L} #tau_{L})} (electronic channel)', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        defineHisto('deltaPhi_j_tau2',
            '#Delta #phi_{(j_{L} #tau_{L})} (muonic channel)', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        
        defineHisto('deltaPhi_j_e',
            '#Delta #phi_{(j_{L} e)}', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        defineHisto('deltaPhi_j_mu',
            '#Delta #phi_{(j_{L} #mu)}', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        
        defineHisto('deltaPhi_b_j1',
            '#Delta #phi_{(b_{L} j_{L})} (electronic channel)', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )
        defineHisto('deltaPhi_b_j2',
            '#Delta #phi_{(b_{L} j_{L})} (muonic channel)', '#Delta #phi', 'Events',
            28,-3.5,3.5
        )

        
        #Histograms to record the delta PT between each possible pair of jets
        defineHisto('vDeltaPT_tau_e',
            '#Delta #vec{PT}_{(#tau e)}', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        defineHisto('vDeltaPT_tau_mu',
            '#Delta #vec{PT}_{(#tau #mu)}', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        
        defineHisto('vDeltaPT_b_tau1',
            '#Delta #vec{PT}_{(b_{L} #tau_{L})} (electronic channel)', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        defineHisto('vDeltaPT_b_tau2',
            '#Delta #vec{PT}_{(b_{L} #tau_{L})} (muonic channel)', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        
        defineHisto('vDeltaPT_b_e',
            '#Delta #vec{PT}_{(b_{L} e)}', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        defineHisto('vDeltaPT_b_mu',
            '#Delta #vec{PT}_{(b_{L} #mu)}', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        
        defineHisto('vDeltaPT_j_tau1',
            '#Delta #vec{PT}_{(j_{L} #tau_{L})} (electronic channel)', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        defineHisto('vDeltaPT_j_tau2',
            '#Delta #vec{PT}_{(j_{L} #tau_{L})} (muonic channel)', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        
        defineHisto('vDeltaPT_j_e',
            '#Delta #vec{PT}_{(j_{L} e)}', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        defineHisto('vDeltaPT_j_mu',
            '#Delta #vec{PT}_{(j_{L} #mu)}', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        
        defineHisto('vDeltaPT_b_j1',
            '#Delta #vec{PT}_(b_{L} j_{L})}', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        defineHisto('vDeltaPT_b_j2',
            '#Delta #vec{PT}_(b_{L} j_{L})}', '#Delta PT (GeV)', 'Events',
            40, 0.0, 2000.0
        )
        
        return self.hist_list


    def writelist(self):
        os.system("rm -rf {self.name}.root")
        f =TFile(self.name+".root","RECREATE")
        self.hist_list.Write("histlist", TObject.kSingleKey)
        f.ls()
        print(self.name+" Done!")


    def fillJetHistos(self, JD, MET, ch_bool):

        if ch_bool:
            compl = '1'
            lepton = 'e'
            key = 'electrons'
        else:
            compl = '2'
            lepton = 'mu'
            key = 'muons'

        #All jets kinematics histos
        for jet in JD['all_jets']:
            self.hist_list.FindObject("pt_all_jets"+compl).Fill(jet.TLV.Pt())
            self.hist_list.FindObject("eta_all_jets"+compl).Fill(jet.TLV.Eta())
        
        for jet in JD['l_jets']:
            self.hist_list.FindObject("pt_all_ljets"+compl).Fill(jet.TLV.Pt())
            self.hist_list.FindObject("eta_all_ljets"+compl).Fill(jet.TLV.Eta())
            
        for jet in JD['b_jets']:
            self.hist_list.FindObject("pt_all_bjets"+compl).Fill(jet.TLV.Pt())
            self.hist_list.FindObject("eta_all_bjets"+compl).Fill(jet.TLV.Eta())
            
        for jet in JD['tau_jets']:
            self.hist_list.FindObject("pt_all_taujets"+compl).Fill(jet.TLV.Pt())
            self.hist_list.FindObject("eta_all_taujets"+compl).Fill(jet.TLV.Eta())
        
        #Reconstructed mass
        
        lqTLV=JD['b_jets'][0].TLV + JD['tau_jets'][0].TLV
        self.hist_list.FindObject("m_LQ_tau"+compl).Fill(lqTLV.M())
        self.hist_list.FindObject("pt_LQ"+compl).Fill(lqTLV.Pt())
        lqTLV = lqTLV + MET
        self.hist_list.FindObject("m_LQ_tau"+compl+'_met').Fill(lqTLV.M())
        
        lqTLV=JD['b_jets'][0].TLV + JD[key][0].TLV
        self.hist_list.FindObject("m_LQ_"+lepton).Fill(lqTLV.M())
        self.hist_list.FindObject("pt_LQ"+lepton).Fill(lqTLV.Pt())
        lqTLV = lqTLV + MET
        self.hist_list.FindObject("m_LQ_"+lepton+'_met').Fill(lqTLV.M())
        
        #Pt Histos
        
        self.hist_list.FindObject("pt_lead_ljet"+compl).Fill(
            JD['l_jets'][0].Pt()
        )
        self.hist_list.FindObject("pt_lead_bjet"+compl).Fill(
            JD['b_jets'][0].Pt()
        )
        self.hist_list.FindObject("pt_lead_tau"+compl).Fill(
            JD['tau_jets'][0].Pt()
        )
        self.hist_list.FindObject("pt_"+lepton).Fill(
            JD[key][0].Pt()
        )
        
        #Eta Histos
        
        self.hist_list.FindObject("eta_lead_ljet"+compl).Fill(
            JD['l_jets'][0].Eta()
        )
        self.hist_list.FindObject("eta_lead_bjet"+compl).Fill(
            JD['b_jets'][0].Eta()
        )
        self.hist_list.FindObject("eta_lead_tau"+compl).Fill(
            JD['tau_jets'][0].Eta()
        )
        self.hist_list.FindObject("eta_"+lepton).Fill(
            JD[key][0].Eta()
        )
        
        #Delta Eta Histos
        
        self.hist_list.FindObject("deltaEta_tau_"+lepton).Fill(
            JD['tau_jets'][0].DeltaEta(JD[key][0])
        )
        
        self.hist_list.FindObject("deltaEta_b_tau"+compl).Fill(
            JD['b_jets'][0].DeltaEta(JD['tau_jets'][0])
        )
        
        self.hist_list.FindObject("deltaEta_b_"+lepton).Fill(
            JD['b_jets'][0].DeltaEta(JD[key][0])
        )
        
        self.hist_list.FindObject("deltaEta_j_tau"+compl).Fill(
            JD['l_jets'][0].DeltaEta(JD['tau_jets'][0])
        )
        
        self.hist_list.FindObject("deltaEta_j_"+lepton).Fill(
            JD['l_jets'][0].DeltaEta(JD[key][0])
        )
        
        self.hist_list.FindObject("deltaEta_b_j"+compl).Fill(
            JD['b_jets'][0].DeltaEta(JD['l_jets'][0])
        )
        
        ########
        
        self.hist_list.FindObject("deltaPhi_tau_"+lepton).Fill(
            JD['tau_jets'][0].DeltaPhi(JD[key][0])
        )
        
        self.hist_list.FindObject("deltaPhi_b_tau"+compl).Fill(
            JD['b_jets'][0].DeltaPhi(JD['tau_jets'][0])
        )
        
        self.hist_list.FindObject("deltaPhi_b_"+lepton).Fill(
            JD['b_jets'][0].DeltaPhi(JD[key][0])
        )
        
        self.hist_list.FindObject("deltaPhi_j_tau"+compl).Fill(
            JD['l_jets'][0].DeltaPhi(JD['tau_jets'][0])
        )
        
        self.hist_list.FindObject("deltaPhi_j_"+lepton).Fill(
            JD['l_jets'][0].DeltaPhi(JD[key][0])
        )
        
        self.hist_list.FindObject("deltaPhi_b_j"+compl).Fill(
            JD['b_jets'][0].DeltaPhi(JD['l_jets'][0])
        )
        
        ########
        
        self.hist_list.FindObject("vDeltaPT_tau_"+lepton).Fill(
            JD['tau_jets'][0].vDeltaPT(JD[key][0])
        )
        
        self.hist_list.FindObject("vDeltaPT_b_tau"+compl).Fill(
            JD['b_jets'][0].vDeltaPT(JD['tau_jets'][0])
        )
        
        self.hist_list.FindObject("vDeltaPT_b_"+lepton).Fill(
            JD['b_jets'][0].vDeltaPT(JD[key][0])
        )
        
        self.hist_list.FindObject("vDeltaPT_j_tau"+compl).Fill(
            JD['l_jets'][0].vDeltaPT(JD['tau_jets'][0])
        )
        
        self.hist_list.FindObject("vDeltaPT_j_"+lepton).Fill(
            JD['l_jets'][0].vDeltaPT(JD[key][0])
        )
        
        self.hist_list.FindObject("vDeltaPT_b_j"+compl).Fill(
            JD['b_jets'][0].vDeltaPT(JD['l_jets'][0])
        )

    
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
        self.goodEventIndex=[]
        bar = ProgressBar(nEvents, max_width=60)
        printEachPercent=5.0
        bar.numerator = 0
        print(self.name, bar)
        nSplits=int(100/printEachPercent)
        last_printed=0
        f_electrons = open(self.name+"_electrons.csv", "w")
        f_muons = open(self.name+"_muons.csv", "w")
        f_track = open(self.name+'_track.csv', 'w')
        
        for i, event in enumerate(self.tree):
            n_jets=event.Jet.GetEntries()
            self.hist_list.FindObject("e-cutflow").Fill(0)
            self.hist_list.FindObject("mu-cutflow").Fill(0)
            self.hist_list.FindObject("n_jets").Fill(n_jets)
            
            if( float(i)/float(nEvents)>=0.006 ): break
                
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

            lq_TLV=b.TLV+tau.TLV
            row=[
                lq_TLV.M(),
                lq_TLV.Pt(),
                j.vDeltaPT(b),
                j.vDeltaPT(tau),
                j.vDeltaPT(lepton),
                b.vDeltaPT(tau),
                b.vDeltaPT(lepton),
                tau.vDeltaPT(tau), ###
                j.DeltaPhi(b),
                j.DeltaPhi(tau),
                j.DeltaPhi(lepton),
                b.DeltaPhi(tau),
                b.DeltaPhi(lepton),
                tau.DeltaPhi(lepton),
                j.Pt(),
                b.Pt(),
                tau.Pt(),
                lepton.Pt()
            ]
            
            str_row=""
            for feature in row:
                str_row+=str(feature)
                str_row+=","
            str_row+="\n"
            if electronic:
                f_electrons.write(str_row)
            else:
                f_muonic.write(str_row)
            
            self.fillJetHistos(jets, metTLV, electronic)
            self.goodEventIndex.append(i)
            
            if int(nSplits*(i)/nEvents)!=last_printed:
                last_printed=int(nSplits*i/nEvents)
                bar.numerator=i
                f_track.write(bar)
                
        f_track.close()
        f_electrons.close()
        f_muons.close()
        self.writelist()
        return self.goodEventIndex