# import ROOT in batch mode
import ROOT
ROOT.gROOT.SetBatch(True)

ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Handle, Events

#name = "ZGamma"
#events = Events("root://cmsxrootd.hep.wisc.edu//store/user/nsmith/ZG_Inclusive_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/ZHinv2015/patTuple_cfg-006B5ECF-8124-E211-9AF8-002618943982.root")
#eventWeight = 123.9/6321549
name = "DY"
events = Events("root://cmsxrootd.hep.wisc.edu//store/user/dntaylor/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/Fall2014PATTuples_V1/patTuple_cfg-00037C53-AAD1-E111-B1BE-003048D45F38.root")
eventWeight = 3503.71/30459503

handleGenParticles  = Handle ("std::vector<reco::GenParticle>")
labelGenParticles = ("genParticles")

def lorentz(particle) :
    return ROOT.TLorentzVector(particle.px(), particle.py(), particle.pz(), particle.energy())

def searchTree(particle, condition) :
    for i in range(particle.numberOfDaughters()) :
        daughter = particle.daughter(i)
        if condition(daughter) :
            return daughter
        else :
            return searchTree(daughter, condition)
    print "If here, we failed to find a final state lepton! Where'd it go?!"

ROOT.gStyle.SetMarkerSize(0.3)

hdR = ROOT.TH1F("deltaR", "FSR;#DeltaR #gamma-l;d#sigma [pb]", 50, 0, 4)
hpt = ROOT.TH1F("pt", "FSR;#gamma p_{T};d#sigma [pb]", 50, 0, 50)
hdRISR = ROOT.TH1F("deltaRISR", "ISR;#DeltaR ISR #gamma-l;d#sigma [pb]", 50, 0, 4)
hptISR = ROOT.TH1F("ptISR", "ISR;ISR #gamma p_{T};d#sigma [pb]", 50, 0, 50)
hdRISR.SetLineColor(ROOT.kRed)
hdRISR.SetMarkerColor(ROOT.kRed)
hptISR.SetLineColor(ROOT.kRed)
hptISR.SetMarkerColor(ROOT.kRed)
hdRISR.SetLineStyle(ROOT.kDashed)
hptISR.SetLineStyle(ROOT.kDashed)

nevents = 0
for i,event in enumerate(events):
    nevents += 1
    if i%100 == 0 :
        print "Event", i
    event.getByLabel(labelGenParticles, handleGenParticles)
    particles = handleGenParticles.product()

    leptons = []
    photons = []
    for particle in particles :
        if particle.status() == 1 and abs(particle.pdgId()) in [11,13,15] :
            leptons.append(particle)
        elif particle.status() == 1 and particle.pdgId() == 22 and abs(particle.mother(0).pdgId()) < 25 :
            photons.append(particle)

    if len(photons) == 0 or len(leptons) == 0 :
        continue
    leadingPhoton = max(photons, key=lambda p : p.pt())
    closestLepton = min(leptons, key=lambda p : lorentz(p).DeltaR(lorentz(leadingPhoton)))

    dR = lorentz(leadingPhoton).DeltaR(lorentz(closestLepton))
    pt = leadingPhoton.pt()

    if abs(leadingPhoton.mother(0).pdgId()) in [11,13,15,22] \
            and leadingPhoton.mother(0).mother(0).pdgId() in [22,23,leadingPhoton.mother(0).pdgId()] :
        hdR.Fill(dR, eventWeight)
        hpt.Fill(pt, eventWeight)
    elif abs(leadingPhoton.mother(0).pdgId()) in [1,2,3,4,5,6,21] \
            or (leadingPhoton.mother(0).pdgId() == 22 and abs(leadingPhoton.mother(0).mother(0).pdgId()) in [1,2,3,4,5,6,21]) :
        hdRISR.Fill(dR, eventWeight)
        hptISR.Fill(pt, eventWeight)
    else :
        print "Missed ISR/FSR photon"
        print "mother id: %d" % leadingPhoton.mother(0).pdgId()
        print "grandmother id: %d" % leadingPhoton.mother(0).mother(0).pdgId()

print "Total nevents processed = %d" % nevents

c = ROOT.TCanvas("canvas", "asdf")
stack = ROOT.THStack("dr", ";#DeltaR #gamma-l;d#sigma [pb]")
stack.Add(hdR, "histex0")
stack.Add(hdRISR, "histex0")
stack.Draw("nostack")
c.BuildLegend()
c.Print("plots/%sGenInfo/deltaR.pdf"%name)
c.Print("plots/%sGenInfo/deltaR.root"%name)

c.Clear()

stack2 = ROOT.THStack("dr", ";#gamma p_{T};d#sigma [pb]")
stack2.Add(hpt, "histex0")
stack2.Add(hptISR, "histex0")
stack2.Draw("nostack")
c.BuildLegend()
c.Print("plots/%sGenInfo/pt.pdf"%name)
c.Print("plots/%sGenInfo/pt.root"%name)
