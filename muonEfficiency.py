import os, pickle

def buildMuonEfficiencyRescaleString() :
    muonIDpkl = pickle.load(open('meta/MuonEfficiencies_Run2012ReReco_53X.pkl'))
    muonISOpkl = pickle.load(open('meta/MuonEfficiencies_ISO_Run_2012ReReco_53X.pkl'))

    ptranges = ['0_0.9', '0.9_1.2', '1.2_2.1', '2.1_2.4']
    absEtaStrings = ['abs(%s)<0.9', 'abs(%s)<1.2', 'abs(%s)<2.1', 'abs(%s)<2.4']

    def buildLeg(etaVar) :
        rescaleStrings = []
        for i in range(len(ptranges)) :
            sf = muonIDpkl['Tight']['abseta_2p4pt20-500'][ptranges[i]]['data/mc']['efficiency_ratio']
            ISOsf = muonISOpkl['combRelIsoPF04dBeta<02_Tight']['abseta_2p4pt20-500'][ptranges[i]]['data/mc']['efficiency_ratio']
            rescaleStrings.append('(%s)?%f' % (absEtaStrings[i] % etaVar, sf*ISOsf))
        rescaleStrings.append('1.')
        return '(%s)' % ':'.join(rescaleStrings)

    legs = ['m1Eta', 'm2Eta']
    corrections = [buildLeg(leg) for leg in legs]

    muonHLTpkl = pickle.load(open('meta/MuHLTEfficiencies_Run_2012ABCD_53X_DR03-2.pkl'))
    HLTsf = muonHLTpkl['Mu17Mu8_OR_Mu17TkMu8']['Tight']['overall']['(20<mu1<Infty,20<mu2<Infty)']['ratio']['efficiency']
    corrections.append('(%f)'%HLTsf)

    return '*'.join(corrections)

if __name__ == '__main__' :
    print buildMuonEfficiencyRescaleString()
