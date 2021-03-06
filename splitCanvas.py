import ROOT

def recursePrimitives(tobject, function, *fargs) :
    function(tobject, *fargs)
    if hasattr(tobject, 'GetListOfPrimitives') :
        primitives = tobject.GetListOfPrimitives()
        if primitives :
            for item in primitives :
                recursePrimitives(item, function, *fargs)
    other_children = ['Xaxis', 'Yaxis', 'Zaxis']
    for child in other_children :
        if hasattr(tobject, 'Get'+child) :
            childCall = getattr(tobject, 'Get'+child)
            recursePrimitives(childCall(), function, *fargs)

def fixFontSize(item, scale) :
    if 'TH' in item.ClassName() :
        return
    if item.GetName() == 'yaxis' :
        item.SetTitleOffset(item.GetTitleOffset()/scale)
    sizeFunctions = ['LabelSize', 'TextSize', 'TitleSize']
    for fun in sizeFunctions :
        if hasattr(item, 'Set'+fun) :
            getattr(item, 'Set'+fun)(getattr(item, 'Get'+fun)()*scale)

def readStyle(canvas) :
    style = ROOT.TStyle(canvas.GetName()+"_style", "Read style")
    style.cd()
    style.SetIsReading()
    canvas.UseCurrentStyle()
    style.SetIsReading(False)
    return style

def splitCanvas(oldcanvas) :
    name = oldcanvas.GetName()

    canvas = ROOT.TCanvas(name+'__new', name)
    ratioPad = ROOT.TPad(name+'_ratioPad', 'ratioPad', 0., 0., 1., .3)
    ratioPad.Draw()
    stackPad = ROOT.TPad(name+'_stackPad', 'stackPad', 0., 0.3, 1., 1.)
    stackPad.Draw()

    stackPad.cd()
    oldcanvas.DrawClonePad()
    del oldcanvas
    oldBottomMargin = stackPad.GetBottomMargin()
    stackPad.SetBottomMargin(0.)
    canvas.SetName(name)

    ratioPad.cd()
    ratioPad.SetBottomMargin(oldBottomMargin/.3)
    ratioPad.SetTopMargin(0.)
    sumMC = stackPad.GetPrimitive(name+'_hstackErrors')
    data = stackPad.GetPrimitive(name+'_data_hist')
    stack = stackPad.GetPrimitive(name+'_hmcstack')
    dataOverSumMC = data.Clone(name+'_dataOverSumMC_hist')
    sumMCErrors = sumMC.Clone(name+'_sumMCErrors_hist')
    dataOverSumMC.Divide(sumMC)
    for i in range(data.GetNbinsX()) :
        dataOverSumMC.SetBinError(i, data.GetBinError(i)/max(data.GetBinContent(i),1))
        sumMCErrors.SetBinError(i, sumMCErrors.GetBinError(i)/max(sumMCErrors.GetBinContent(i),1))
        sumMCErrors.SetBinContent(i, 1.)
    dataOverSumMC.GetXaxis().SetTitle(stack.GetXaxis().GetTitle())
    dataOverSumMC.GetYaxis().SetTitle('Data / #Sigma MC')
    dataOverSumMC.GetYaxis().CenterTitle()
    dataOverSumMC.GetYaxis().SetRangeUser(.4, 1.6)
    dataOverSumMC.GetYaxis().SetNdivisions(305)
    dataOverSumMC.GetYaxis().SetTitleSize(dataOverSumMC.GetYaxis().GetTitleSize()*0.6)
    if 'cutflow' in name :
        for i in range(dataOverSumMC.GetXaxis().GetNbins()) :
            dataOverSumMC.GetXaxis().SetBinLabel(i+1, stack.GetXaxis().GetBinLabel(i+1))
        dataOverSumMC.GetXaxis().SetLabelOffset(0.02)
    dataOverSumMC.Draw()
    sumMCErrors.Draw("E2 same")
    line = ROOT.TLine(dataOverSumMC.GetBinLowEdge(1), 1, dataOverSumMC.GetBinLowEdge(dataOverSumMC.GetNbinsX()+1), 1)
    line.SetLineStyle(ROOT.kDotted)
    line.Draw()

    recursePrimitives(stackPad, fixFontSize, 1/0.7)
    stackPad.Modified()
    recursePrimitives(ratioPad, fixFontSize, 1/0.3)
    ratioPad.Modified()
    canvas.Update()

    for item in [stackPad, ratioPad, dataOverSumMC, sumMCErrors, line] :
        ROOT.SetOwnership(item, False)
    return canvas

