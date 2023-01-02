from re import S
from unittest import result
from flask import Flask,render_template,request
import sys
sys.path.append(r'//Users/Mumtaz/Desktop/Important Folders/Wasef/GMU/Courses/Fall 2022/CS 787/Final Project/Carbon-Footprint-DGS/Carbon-Footprint-DGS')
sys.path.append(r'/lib')
import copy
import pyomo.environ as pyo
from pyomo.environ import *
import model1
import model2
import importlib.util
spec = importlib.util.spec_from_file_location("dgal", "/Users/Mumtaz/Desktop/Important Folders/Wasef/GMU/Courses/Fall 2022/CS 787/Final Project/Carbon-Footprint-DGS/Carbon-Footprint-DGS/lib/dgalPy.py")
dgal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dgal)

app = Flask(__name__)
 
@app.route('/')
def form():
    return render_template('formChoice.html')

@app.route('/selectOption', methods = ['POST', 'GET'])
def data():
    if request.method == 'POST':
        selectedOption = request.form.get("way")
        if selectedOption == 'model1':
            return render_template('utilityForm.html')
        else:
            return render_template('pointsForm.html')

@app.route('/model1', methods = ['POST', 'GET'])
def model1Choice():
    if request.method == 'POST':
        Electricity = request.form.get("electricityUsage")
        NaturalGas = request.form.get("naturalgasUsage")
        Propane = request.form.get("propaneUsage")
        Miles = request.form.get("totalMiles")
        totalFamilyMembers = request.form.get("totalFamilyMembers")
        carType = request.form.get("carType")
        answer_model1 = model1.model1(Electricity, NaturalGas, Propane, Miles, totalFamilyMembers, carType)
        return render_template('results.html', results= answer_model1)

@app.route('/model2', methods = ['POST', 'GET'])
def model2Choice():
    if request.method == 'POST':
        NumberOfFamilyMembers = str(request.form.get("householdFamilyShare"))
        SizeOfHouse = str(request.form.get("homeSize"))
        FoodChoice = str(request.form.get("foodIntake"))
        WaterConsumption = str(request.form.get("waterConsumption"))
        HouseholdPurchases = str(request.form.get("householdPurchases"))
        WasteConsumption = str(request.form.get("wasteConsumption"))
        RecycleCheck = str(request.form.get("recycleCheck"))
        answer_model2= model2.model2(NumberOfFamilyMembers, SizeOfHouse, FoodChoice, WaterConsumption, HouseholdPurchases, WasteConsumption, RecycleCheck)
        return render_template('results.html', results= answer_model2)

app.run(host='localhost', port=5000)
