import copy
import json
import importlib.util
import sys
import numbers

sys.path.append('/Users/Mumtaz/Desktop/Important Folders/Wasef/GMU/Courses/Fall 2022/CS 787/Final Project/Carbon-Footprint-DGS/Carbon-Footprint-DGS')
sys.path.append(r'/lib')
import lib.dgalPy as dgal

# import aaa_dgalPy.lib.dgalPy as dgal

def minUtilityConstraints(utilityUsage, utilityCo2Emission):
    return dgal.all([utilityCo2Emission[utility_co2_itr]["usage"] >= utilityUsage[utility_co2_itr]["minUsage"]
    for utility_co2_itr in utilityCo2Emission])

def carbonFootPrint(totalCo2EmissionPerPerson):
    return dgal.all([totalCo2EmissionPerPerson >= 0, totalCo2EmissionPerPerson <= 60])

def carbonFootPrints(input):
    type = input["type"]
    householdFamilyShare = input["householdFamilyShare"]
    utilityUsage = input["pointsUsage"]
    co2Emission = input["co2Emission"]
    totalCo2EmissionForUtilities = sum(
        (utilityUsage[utility_usage_itr]["usage"])
        for utility_usage_itr in utilityUsage
        for co2Emission_itr in co2Emission
        if utility_usage_itr == co2Emission_itr
    )
    totalCo2Emission = totalCo2EmissionForUtilities
    totalCo2EmissionPerPerson = totalCo2Emission

    utilityCo2Emission = dict()
    for utility_usage_itr in utilityUsage:
            utilityCo2Emission.update({utility_usage_itr: {"usage": utilityUsage[utility_usage_itr]["usage"], 
            "co2Emission": utilityUsage[utility_usage_itr]["usage"],
            "avgCo2Emission": utilityUsage[utility_usage_itr]["minUsage"]}})

    minUtilityCheck = minUtilityConstraints(utilityUsage, utilityCo2Emission)
    carbonFootPrintCheck = carbonFootPrint(totalCo2EmissionPerPerson)

    constraints = dgal.all([minUtilityCheck, carbonFootPrintCheck])

    return {
        "type": type,
        "householdFamilyShare": householdFamilyShare,
        "totalCo2Emission": totalCo2Emission,
        "totalCo2EmissionPerPerson": totalCo2EmissionPerPerson,
        "constraints": constraints,
        "utilityCo2Emission": utilityCo2Emission,
        "co2Emission": co2Emission
    }
