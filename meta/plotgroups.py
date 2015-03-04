#!/bin/env python
import ROOT

plotgroups = {
    'WToLNu': {
        'title' : "W#rightarrowl#nu",
        'histOptions' : {
            'FillColor': ROOT.kYellow
        }
    },
    'ZToLL': {
        'title' : "Z#rightarrowll",
        'histOptions' : {
            'FillColor': ROOT.kCyan
        }
    },
    'WW': {
        'title' : "WW#rightarrow2l2#nu",
        'histOptions' : {
            'FillColor': ROOT.kYellow-2
        }
    },
    'WZ': {
        'title' : "WZ#rightarrow3l#nu",
        'histOptions' : {
             'FillColor': ROOT.kBlue
        }
    },
    'ZZ': {
        'title' : "ZZ#rightarrow2l2#nu",
        'histOptions' : {
             'FillColor': ROOT.kGreen
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
             'LineWidth' : 2
        }
    },
    'singleTop': {
        'title' : "Single top",
        'histOptions' : {
             'FillColor': ROOT.kViolet
        }
    },
    'ttbar': {
        'title' : "t#bar{t}",
        'histOptions' : {
             'FillColor': ROOT.kBlue+2
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
    'ZToLL'
]
