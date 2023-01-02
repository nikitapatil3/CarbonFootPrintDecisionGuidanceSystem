from re import S
from unittest import result
import sys
sys.path.append(r'//Users/nikitapatil/Documents/Carbon-Footprint-DGS-main')
sys.path.append(r'/lib')
import copy
import pyomo.environ as pyo
from pyomo.environ import *
import json
import utilization
import optUtilityUsage
import importlib.util
spec = importlib.util.spec_from_file_location("dgal", "/Users/nikitapatil/Documents/Carbon-Footprint-DGS-main/lib/dgalPy.py")
dgal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dgal)


def checkOptions(optionsToUser, percentageImprovedRequired, utility_itr):
    best_option = -1
    currentPercentageImprovement = 100
    for option_itr in optionsToUser[utility_itr]:
        if optionsToUser[utility_itr][option_itr] <= currentPercentageImprovement and optionsToUser[utility_itr][option_itr] >= percentageImprovedRequired :
            best_option = option_itr
            currentPercentageImprovement = optionsToUser[utility_itr][option_itr]

    return best_option


def displayOptionToUser(best_option, optionsToUser, currentUsage, optimizedUsage, utility_itr, percentageImprovedRequired): 

    if (best_option == -1):
        result = {
            "Component": utility_itr,
            "CurrentUsage": currentUsage,
            "RequiredUsage": optimizedUsage,
            "Percentage Reduction required": percentageImprovedRequired,
            "options": [
                {
                    "option": itr, 
                    "Percentage reduced by using this option": optionsToUser[utility_itr][itr]} 
                    for itr in optionsToUser[utility_itr]
                    ]
                }    
    else:
        result = {
        "Component": utility_itr,
        "CurrentUsage": currentUsage,
        "RequiredUsage": optimizedUsage,
        "Percentage Reduction required": percentageImprovedRequired,
        "options": [
            {
            "option": best_option, 
            "Percentage reduced by using this option": optionsToUser[utility_itr][best_option]
            }
            ]
        }  
    
    return result

def suggestOptionsToUser(optimized_anwer, input, carChange):
    options_file = open("example_input_output/alternatives_to_reduce_carbon_footprints.json","r")
    optionsToUser = json.loads(options_file.read())
    utilityUsage = input["utilityUsage"]
    optimizedUtilityUsage = optimized_anwer["utilityCo2Emission"]
    display_answer = []
    for utility_itr in utilityUsage:
        currentUsage = utilityUsage[utility_itr]["usage"]
        optimizedUsage = optimizedUtilityUsage[utility_itr]["usage"]
        percentageImprovedRequired = ((currentUsage - optimizedUsage) * 100)/currentUsage
        best_option = checkOptions(optionsToUser, percentageImprovedRequired, utility_itr)
       
        if (optimizedUsage < currentUsage):
            display_answer.append(displayOptionToUser(best_option, optionsToUser, currentUsage, optimizedUsage, utility_itr, percentageImprovedRequired))
        else:
            return "Your Carbon Footprint is in correct range"

    if carChange:
        display_answer.append({
            "Component": "carType",
            "options": [{
                "option": "Use Electric or Hybrid car type"}
            ]
        })
    return str(display_answer)

def model1(Electricity, NaturalGas, Propane, Miles, totalFamilyMembers, carType):
    minUsagePercentage = 0
    template_file = open("example_input_output/impact_of_car_and_utility.json","r")
    input = json.loads(template_file.read())
    input["carType"] = carType
    input["utilityUsage"]["Electricity"]["usage"] = int(Electricity)
    input["utilityUsage"]["NaturalGas"]["usage"] = int(NaturalGas)
    input["utilityUsage"]["Propane"]["usage"] = int(Propane)
    input["utilityUsage"]["Fuel"]["usage"] = int(Miles) / 40
    input["totalFamilyMembers"] = int(totalFamilyMembers)
    optimization_file = open("example_input_output/impact_of_car_and_utility_in_var.json","r")
    optimization_input = json.loads(optimization_file.read())
    optimization_input["totalFamilyMembers"] = int(totalFamilyMembers)
    optimization_input["carType"] = carType
    optimized_anwer = None
    while (optimized_anwer is None or optimized_anwer["optOutput"] == 'none') and minUsagePercentage < 80:
        for utility_itr in input["utilityUsage"]:
            input["utilityUsage"][utility_itr]["minUsage"] = input["utilityUsage"][utility_itr]["usage"] - ((input["utilityUsage"][utility_itr]["usage"] * minUsagePercentage)/100)
        
        for utility_itr in optimization_input["utilityUsage"]:
            optimization_input["utilityUsage"][utility_itr]["minUsage"] = input["utilityUsage"][utility_itr]["usage"] - ((input["utilityUsage"][utility_itr]["usage"] * minUsagePercentage)/100)

        answer = utilization.carbonFootPrints(input)
        answer_file = open("answers/out.json","w")
        answer_file.write(json.dumps(answer))
        if(answer["totalCo2EmissionPerPerson"] <= 6000):
            return "Your Carbon Footprint is in correct range"
        optimized_anwer = optUtilityUsage.optimizeUtility(optimization_input)
        minUsagePercentage = minUsagePercentage + 10

    carChange = False

    if (optimized_anwer is None or optimized_anwer["optOutput"] == 'none'):
        optimization_input["carType"] = "hybrid"
        input["carType"] = "hybrid"
        minUsagePercentage = 0
        carChange = True
        while (optimized_anwer is None or optimized_anwer["optOutput"] == 'none') and minUsagePercentage < 80:
            for utility_itr in input["utilityUsage"]:
                input["utilityUsage"][utility_itr]["minUsage"] = input["utilityUsage"][utility_itr]["usage"] - ((input["utilityUsage"][utility_itr]["usage"] * minUsagePercentage)/100)
        
            for utility_itr in optimization_input["utilityUsage"]:
                optimization_input["utilityUsage"][utility_itr]["minUsage"] = input["utilityUsage"][utility_itr]["usage"] - ((input["utilityUsage"][utility_itr]["usage"] * minUsagePercentage)/100)

            answer = utilization.carbonFootPrints(input)
            answer_file = open("answers/out.json","w")
            answer_file.write(json.dumps(answer))
            if(answer["totalCo2EmissionPerPerson"] <= 6000):
                return "Your Carbon Footprint is in correct range"
            optimized_anwer = optUtilityUsage.optimizeUtility(optimization_input)
            minUsagePercentage = minUsagePercentage + 10

        if (optimized_anwer is None or optimized_anwer["optOutput"] == 'none'):
            message = "Your current usage of utilities is too much, Even if you reduced your utilities by 80 percentage and switched car type to electric or hybrid it does not fit in the correct range of carbon footprints"
            return message
    
    optimized_answer_file = open("answers/optUtilityUsage.json","w")
    optimized_answer_file.write(json.dumps(optimized_anwer))
    return suggestOptionsToUser(optimized_anwer["optOutput"], input, carChange)
