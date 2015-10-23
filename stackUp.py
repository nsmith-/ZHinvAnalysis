import ROOT
from meta.plotgroups import plotgroups, stack_order
import meta
from muonEfficiency import buildMuonEfficiencyRescaleString
from meta.pileupReweight import pileupReweightStrings
import math

def stackUp(**kwargs) :
    ''' Parameters:
        name
        bins
        xmin
        xmax
        trees
        (or plotfile)
        variable
        cut
        ymin
        ymax
        logY
        xtitle
        ytitle
        (this is more a log of things that need input validation later)
    '''
    name = kwargs['name']
    if 'channel' in kwargs :
        name = kwargs['channel'] + '_' + name
    cut = kwargs['cut'] if 'cut' in kwargs else ''
    if type(cut) is list :
        cut = " && ".join(cut)

    directory = ROOT.TDirectory(name+"_dir", "Helps with TTree::Draw")
    directory.cd()
    canvas = ROOT.TCanvas(name, name)
    mcStack = ROOT.THStack(name+"_hmcstack", "")
    tostack = {}
    todraw = {}

    def findGroupHist(plotgroup) :
        hist_id = "_".join([name, plotgroup, "hist"])
        if directory.Get(hist_id) :
            return directory.Get(hist_id)
        h = ROOT.TH1F(hist_id, plotgroups[plotgroup]['title'], kwargs['bins'], kwargs['xmin'], kwargs['xmax'])
        h.Sumw2()
        for optname, optvalue in plotgroups[plotgroup]['histOptions'].iteritems() :
            getattr(h, "Set"+optname)(optvalue)
        return h

    for dataname, info in meta.ZHinv_datasets.iteritems() :
        plotgroup = info['plotgroup']
        h = findGroupHist(plotgroup)
        hname = h.GetName()
        if 'plotfile' in kwargs :
            hToAdd = kwargs['plotfile'].Get('%s_%s_%s_hist' % (dataname, kwargs['proof_prefix'], name))
            if hToAdd != None and 'cutflow' not in name :
                h.Add(hToAdd)
            elif hToAdd != None :
                hCutFlow = hToAdd.Clone()
                nbins = int(math.log(hToAdd.GetNbinsX())/math.log(2))+1
                hCutFlow.SetBins(nbins, 0, nbins)
                for i in range(nbins) :
                    originalBinsToAdd = (x for x in range(2**(nbins-1)) if (x+1)%2**i==0)
                    binValues = (hToAdd.GetBinContent(b+1) for b in originalBinsToAdd)
                    hCutFlow.SetBinContent(i+1, sum(binValues))
                h.Add(hCutFlow)
            else :
                print "Can't find " + '%s_%s_hist' % (dataname, name)
        elif 'trees' in kwargs :
            if dataname not in kwargs['trees'] :
                continue
            drawCut = '(%s)' % cut if len(cut)>0 else ''
            if info['type'] == 'mc' :
                if 'mm' in name :
                    drawCut = pileupReweightStrings['%s_%s_reweight_hist' % (dataname, 'mm')]
                    drawCut += '*'+buildMuonEfficiencyRescaleString()
            returnCode = kwargs['trees'][dataname].Draw(kwargs['variable']+">>+"+hname, drawCut)
            if returnCode < 0 :
                print 'Draw command failed on dataname %s, command: %s' % (dataname, kwargs['variable']+">>+"+hname)
        if info['type'] == 'mc' and not 'signal' in info.get('flags',[]) :
            tostack[plotgroup] = h
        elif info['type'] == 'data' :
            todraw[h] = "pex0"
        else :
            todraw[h] = "hist ex0"

    hstackErrors = ROOT.TH1F("_".join([name, "hstackErrors"]), 'Stat. Error', kwargs['bins'], kwargs['xmin'], kwargs['xmax'])
    hstackErrors.SetDirectory(0)
    hstackErrors.Sumw2()
    hstackErrors.SetFillColor(ROOT.kGray+2)
    hstackErrors.SetFillStyle(3013)
    hstackErrors.SetMarkerSize(0)
    for group in stack_order :
        h = tostack[group]
        h.SetLineColor(ROOT.TColor.GetColorDark(h.GetFillColor()))
        h.SetDirectory(0)
        hstackErrors.Add(h)
        mcStack.Add(h, "hist")

    mcStack.Draw()
    mcStack.SetMinimum(kwargs['ymin'])
    mcStack.SetMaximum(kwargs['ymax'])
    # FIXME: all hists should get titles
    mcStack.GetXaxis().SetTitle(kwargs['xtitle'])
    mcStack.GetYaxis().SetTitle(kwargs['ytitle'])

    if 'xlabels' in kwargs :
        for b, label in enumerate(kwargs['xlabels']) :
            mcStack.GetXaxis().SetBinLabel(b+1, label)

    hstackErrors.Draw("E2 same")

    for h, style in todraw.iteritems() :
        h.SetDirectory(0)
        h.Draw(style+"same")

    if kwargs.get('logY', False) :
        canvas.SetLogy()

    legend = ROOT.TLegend(.5, .7, .92, .88)
    for group in stack_order :
        h = tostack[group]
        legend.AddEntry(h, h.GetTitle(), "f")
    for h, style in todraw.iteritems() :
        entrystyle = 'l'
        nosame = h.GetDrawOption().replace('same','')
        if 'p' in nosame :
            entrystyle = 'p'
            if 'e' in nosame :
                entrystyle += 'e'
        legend.AddEntry(h, h.GetTitle(), entrystyle)
    legend.SetName(name+"_legend")
    legend.SetNColumns(3)
    legend.SetColumnSeparation(0.1)
    legend.SetFillColorAlpha(ROOT.kWhite, 0)
    legend.Draw()

    # Transfer object ownership to canvas
    for h in todraw.iterkeys() :
        ROOT.SetOwnership(h, False)
    ROOT.SetOwnership(hstackErrors, False)
    ROOT.SetOwnership(mcStack, False)
    ROOT.SetOwnership(legend, False)
    canvas.GetListOfPrimitives().SetOwner(True)
    return canvas


