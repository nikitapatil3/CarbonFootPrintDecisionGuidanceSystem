from re import S
from unittest import result
import sys
sys.path.append(r'//Users/Mumtaz/Desktop/Important Folders/Wasef/GMU/Courses/Fall 2022/CS 787/Final Project/Carbon-Footprint-DGS/Carbon-Footprint-DGS')
sys.path.append(r'/lib')
import copy
import pyomo.environ as pyo
from pyomo.environ import *
import json
import utilization_points
import optPointsUsage
import importlib.util
spec = importlib.util.spec_from_file_location("dgal", "/Users/Mumtaz/Desktop/Important Folders/Wasef/GMU/Courses/Fall 2022/CS 787/Final Project/Carbon-Footprint-DGS/Carbon-Footprint-DGS/lib/dgalPy.py")
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

def suggestOptionsToUser(optimized_anwer, input):
    options_file = open("example_input_output/alternatives_to_reduce_carbon_footprints_points.json","r")
    optionsToUser = json.loads(options_file.read())
    utilityUsage = input["pointsUsage"]
    optimizedUtilityUsage = optimized_anwer["utilityCo2Emission"]
    display_answer = []
    for utility_itr in utilityUsage:
        currentUsage = utilityUsage[utility_itr]["usage"]
        optimizedUsage = optimizedUtilityUsage[utility_itr]["usage"]
        if(currentUsage > 0):
            percentageImprovedRequired = ((currentUsage - optimizedUsage) * 100)/currentUsage
        else:
            percentageImprovedRequired = 0
        best_option = checkOptions(optionsToUser, percentageImprovedRequired, utility_itr)
       
        if (optimizedUsage < currentUsage):
            display_answer.append(displayOptionToUser(best_option, optionsToUser, currentUsage, optimizedUsage, utility_itr, percentageImprovedRequired))

    if(display_answer == []):
        return "Your Carbon Footprint is in correct range"
    return str(display_answer)

def model2(NumberOfFamilyMembers, SizeOfHouse, FoodChoice, WaterConsumption, HouseholdPurchases, WasteConsumption, RecycleCheck):
    minUsagePercentage = 30
    
    template_file = open("example_input_output/impact_of_points.json","r")
    input = json.loads(template_file.read())
    input["householdFamilyShare"] = NumberOfFamilyMembers
    input["homeSize"] = SizeOfHouse
    input["foodIntake"] = FoodChoice
    input["waterConsumption"] = WaterConsumption
    input["householdPurchases"] = HouseholdPurchases
    input["wasteConsumption"] = WasteConsumption
    input["recycleCheck"] = RecycleCheck

    for iterator in input["co2Emission"]:
        if(input[iterator] in input["co2Emission"][iterator]): 
            input["pointsUsage"][iterator]["usage"] = input["co2Emission"][iterator][input[iterator]]
        else:
            input["pointsUsage"][iterator]["usage"] = input["co2Emission"][iterator]["limit"]

    optimization_file = open("example_input_output/impact_of_points_var.json","r")
    optimization_input = json.loads(optimization_file.read())
    optimization_input["householdFamilyShare"] = NumberOfFamilyMembers
    optimization_input["homeSize"] = SizeOfHouse
    optimization_input["foodIntake"] = FoodChoice
    optimization_input["waterConsumption"] = WaterConsumption
    optimization_input["householdPurchases"] = HouseholdPurchases
    optimization_input["wasteConsumption"] = WasteConsumption
    optimization_input["recycleCheck"] = RecycleCheck

    optimized_anwer = None
    while optimized_anwer is None and minUsagePercentage < 80:

        answer = utilization_points.carbonFootPrints(input)
        answer_file = open("answers/out.json","w")
        answer_file.write(json.dumps(answer))
        optimized_anwer = optPointsUsage.optimizeUtility(optimization_input)
        minUsagePercentage = minUsagePercentage + 10
    
    optimized_answer_file = open("answers/optPointsUsage.json","w")
    optimized_answer_file.write(json.dumps(optimized_anwer))
    return suggestOptionsToUser(optimized_anwer["optOutput"], input)
