#!/usr/bin/env python
import ROOT

# Matched to AN2012_123 colors using
# mac 'Digital Color Meter' with sRGB color coordinates
plotgroups = {
    'WToLNu': {
        'title' : "W#rightarrowl#nu",
        'histOptions' : {
            'FillColor': ROOT.TColor.GetColor('#FFFF02')
        }
    },
    'ZToLL': {
        'title' : "Z#rightarrowll",
        'histOptions' : {
            'FillColor': ROOT.TColor.GetColor('#01FFFF')
        }
    },
    'ZToLL_fsr': {
        'title' : "Z#rightarrowll#gamma",
        'histOptions' : {
            'FillColor': ROOT.kMagenta-6
        }
    },
    'WW': {
        'title' : "WW#rightarrow2l2#nu",
        'histOptions' : {
            'FillColor': ROOT.kYellow-7
        }
    },
    'WZ': {
        'title' : "WZ#rightarrow3l#nu",
        'histOptions' : {
             'FillColor': ROOT.kBlue-7
        }
    },
    'ZZ': {
        'title' : "ZZ#rightarrow2l2#nu",
        'histOptions' : {
             'FillColor': ROOT.kGreen+1
        }
    },
    'data': {
        'title' : "Data",
        'histOptions' : {
             'MarkerColor': ROOT.kBlack
        }
    },
    'signal': {
        'title' : "Z(ll)H(inv)",
        'histOptions' : {
             'LineColor' : ROOT.kRed,
             'LineWidth' : 2,
             'MarkerColor' : ROOT.kRed,
             'MarkerSize' : 0
        }
    },
    'singleTop': {
        'title' : "Single top",
        'histOptions' : {
             'FillColor': ROOT.kViolet-4
        }
    },
    'ttbar': {
        'title' : "t#bar{t}",
        'histOptions' : {
             'FillColor': ROOT.kViolet+5
        }
    }
}

stack_order = [
    'ZZ',
    'WW',
    'WZ',
    'ttbar',
    'singleTop',
    'WToLNu',
    'ZToLL_fsr',
    'ZToLL'
]
