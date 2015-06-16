# import ROOT in batch mode
import ROOT
ROOT.gROOT.SetBatch(True)

ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Handle, Events

events = Events("root://cmsxrootd.hep.wisc.edu//store/user/nsmith/ZG_Inclusive_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/ZHinv2015/patTuple_cfg-006B5ECF-8124-E211-9AF8-002618943982.root")

handleGenParticles  = Handle ("std::vector<reco::GenParticle>")
labelGenParticles = ("genParticles")

def lorentz(particle) :
    return ROOT.TLorentzVector(particle.px(), particle.py(), particle.pz(), particle.energy())

hdR = ROOT.TH1F("deltaR", ";#DeltaR #gamma-l;Counts", 50, 0, 4)
hpt = ROOT.TH1F("pt", ";#gamma p_{T};Counts", 50, 0, 50)

for i,event in enumerate(events):
    if i%100 == 0 :
        print "Event", i
    event.getByLabel(labelGenParticles, handleGenParticles)
    particles = handleGenParticles.product()

    for particle in particles :
        if particle.status() == 1 and particle.pdgId() == 22 \
                and abs(particle.mother(0).pdgId()) in [11,13,15] \
                and particle.mother(0).mother(0).pdgId() == particle.mother(0).pdgId() :
            dR = lorentz(particle).DeltaR(lorentz(particle.mother(0)))
            hdR.Fill(dR)
            pt = particle.pt()
            hpt.Fill(pt)

c = ROOT.TCanvas("canvas", "asdf")
hdR.Draw()
c.Print("plots/ZGammaGenInfo/deltaR.pdf")
c.Print("plots/ZGammaGenInfo/deltaR.root")
hpt.Draw()
c.Print("plots/ZGammaGenInfo/pt.pdf")
c.Print("plots/ZGammaGenInfo/pt.root")
