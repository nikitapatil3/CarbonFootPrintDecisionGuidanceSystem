#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import copy
# replace path below with a path to aaa_dgalPy
sys.path.append('/Users/Mumtaz/Downloads/Carbon-Footprint-DGS')
sys.path.append(r'/lib')
import lib.dgalPy as dgal
import utilization_points

dgal.startDebug()

def optimizeUtility(input):

    optAnswer = dgal.min({
        "model": utilization_points.carbonFootPrints,
        "input": input,
        "obj": lambda o: o["totalCo2EmissionPerPerson"],
        "constraints": lambda o: o["constraints"],
        "options": {"problemType": "mip", "solver":"glpk","debug": True}
    })
    optOutput = utilization_points.carbonFootPrints(optAnswer["solution"])
    dgal.debug("optOutput",optOutput)
    dgal.debug("constraints", optOutput["constraints"])

    output = {
        "optAnswer": optAnswer,
        "optOutput": optOutput
    }
    
    return output
