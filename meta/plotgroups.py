#!/bin/env python
import ROOT

plotgroups = {
    'WToLNu': {
        'title' : "W#to#ell#nu",
        'histOptions' : {
            'FillColor': ROOT.kYellow
        }
    },
    'ZToLL': {
        'title' : "Z#to#ell#ell",
        'histOptions' : {
            'FillColor': ROOT.kCyan
        }
    },
    'WW': {
        'title' : "WW#to2#ell2#nu",
        'histOptions' : {
            'FillColor': ROOT.kYellow-2
        }
    },
    'WZ': {
        'title' : "WZ#to3#ell#nu",
        'histOptions' : {
             'FillColor': ROOT.kBlue
        }
    },
    'ZZ': {
        'title' : "ZZ#to2#ell2#nu",
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
        'title' : "Z(#ell#ell)H(inv)",
        'histOptions' : {
             'LineColor' : ROOT.kRed
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

