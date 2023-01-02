import copy
import json
import importlib.util
import sys
import numbers

import lib.dgalPy as dgal

# import aaa_dgalPy.lib.dgalPy as dgal

def minUtilityConstraints(utilityUsage, utilityCo2Emission):
    return dgal.all([utilityCo2Emission[utility_co2_itr]["usage"] >= utilityUsage[utility_co2_itr]["minUsage"]
    for utility_co2_itr in utilityCo2Emission])

def carbonFootPrint(totalCo2EmissionPerPerson):
    return dgal.all([totalCo2EmissionPerPerson >= 6000, totalCo2EmissionPerPerson <= 15999])

def carbonFootPrints(input):
    type = input["type"]
    totalFamilyMembers = input["totalFamilyMembers"]
    utilityUsage = input["utilityUsage"]
    co2Emission = input["co2Emission"]
    carType = input["carType"]
    totalCo2EmissionForUtilities = sum(
        utilityUsage[utility_usage_itr]["usage"] * co2Emission[co2Emission_itr]
        for utility_usage_itr in utilityUsage
        for co2Emission_itr in co2Emission
        if utility_usage_itr == co2Emission_itr
    )
    totalCo2EmissionForCar = sum(co2Emission["car"][co2Emission_itr]
        for co2Emission_itr in co2Emission["car"]
        if  carType == co2Emission_itr
    )
    totalCo2Emission = totalCo2EmissionForUtilities + totalCo2EmissionForCar
    totalCo2EmissionPerPerson = totalCo2Emission / totalFamilyMembers

    utilityCo2Emission = dict()
    for utility_usage_itr in utilityUsage:
        utilityCo2Emission.update({utility_usage_itr: {"usage": utilityUsage[utility_usage_itr]["usage"], 
        "co2Emission": utilityUsage[utility_usage_itr]["usage"] * co2Emission[utility_usage_itr],
        "avgCo2Emission": utilityUsage[utility_usage_itr]["minUsage"] * co2Emission[utility_usage_itr]}})

    minUtilityCheck = minUtilityConstraints(utilityUsage, utilityCo2Emission)
    carbonFootPrintCheck = carbonFootPrint(totalCo2EmissionPerPerson)

    constraints = dgal.all([minUtilityCheck, carbonFootPrintCheck])

    return {
        "type": type,
        "totalFamilyMembers": totalFamilyMembers,
        "totalCo2Emission": totalCo2Emission,
        "totalCo2EmissionPerPerson": totalCo2EmissionPerPerson,
        "constraints": constraints,
        "utilityCo2Emission": utilityCo2Emission,
        "co2Emission": co2Emission
    }
