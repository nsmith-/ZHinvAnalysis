import ROOT
from meta.plotgroups import plotgroups, stack_order
import meta

def stackUp(**kwargs) :
    ''' Parameters:
        name
        bins
        xmin
        xmax
        trees
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
        if dataname not in kwargs['trees'] :
            continue
        plotgroup = info['plotgroup']
        h = findGroupHist(plotgroup)
        hname = h.GetName()
        kwargs['trees'][dataname].Draw(kwargs['variable']+">>+"+hname, cut)
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
    mcStack.GetXaxis().SetTitle(kwargs['xtitle'])
    mcStack.GetYaxis().SetTitle(kwargs['ytitle'])

    hstackErrors.Draw("E2 same")

    for h, style in todraw.iteritems() :
        h.SetDirectory(0)
        h.Draw(style+"same")

    if kwargs.get('logY', False) :
        canvas.SetLogy()

    legend = ROOT.TLegend(.55, .75, .92, .88)
    for h in tostack.itervalues() :
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
    legend.Draw()

    # Transfer object ownership to canvas
    for h in todraw.iterkeys() :
        ROOT.SetOwnership(h, False)
    ROOT.SetOwnership(hstackErrors, False)
    ROOT.SetOwnership(mcStack, False)
    ROOT.SetOwnership(legend, False)
    canvas.GetListOfPrimitives().SetOwner(True)
    return canvas


