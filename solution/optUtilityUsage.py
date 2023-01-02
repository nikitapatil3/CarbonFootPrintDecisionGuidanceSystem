#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import copy
# replace path below with a path to aaa_dgalPy
sys.path.append("/Users/nikitapatil/Desktop/cs787_carbon_footprint_project")

import lib.dgalPy as dgal
import utilization

dgal.startDebug()

def optimizeUtility(input):

    optAnswer = dgal.min({
        "model": utilization.carbonFootPrints,
        "input": input,
        "obj": lambda o: o["totalCo2EmissionPerPerson"],
        "constraints": lambda o: o["constraints"],
        "options": {"problemType": "mip", "solver":"glpk","debug": True}
    })
    optOutput = 'none'
    if(optAnswer["solution"] != 'none'):
        optOutput = utilization.carbonFootPrints(optAnswer["solution"])
    
    output = {
        "optAnswer": optAnswer,
        "optOutput": optOutput
    }
    
    return output
