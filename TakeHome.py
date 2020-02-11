import random
import string
from datetime import datetime
from datetime import date
import os
from nltk.corpus import names
from prettytable import PrettyTable


class Claim:
	#An event (such as a doctor's appointment) claimed from our policyholders
	def __init__(self, lossDate, claimBilled,claimCovered, uID, age):
		self.lossDate = datetime.strptime(lossDate, "%m/%d/%Y")
		self.lossYear = self.lossDate.year
		self.claimBilled = claimBilled
		self.claimantAge = age
		self.claimantName = uID
		self.claimCovered = claimCovered

class PolicyHolder:
	#An individual's insurance information 
	def __init__(self, firstName,lastName, DOB, SSN, gender, smokingStatus, medicalConditions):
		self.firstName = firstName
		self.lastName = lastName
		self.fullName = firstName +  ' ' + lastName
		self.DOB = datetime.strptime(DOB, "%m/%d/%Y")
		self.birthYear = self.DOB.year
		self.SSN = "###-##-"+SSN[-5:-1]
		self.gender = gender
		self.age = int(date.today().year) - int(self.birthYear)
		self.smokingStatus = smokingStatus
		self.medicalConditions = medicalConditions
		self.claimHistory = []
		self.uniqueIdentifier = ''
		self.assignUniqueIdentifier()
	def reportLoss(self,lossDate,claimBilled,claimCovered):
		self.claimHistory.append(Claim(lossDate,claimBilled,claimCovered, self.uniqueIdentifier, self.age))
	def assignUniqueIdentifier(self):
		self.uniqueIdentifier =  ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
		
class Dashboard:
	#A basic dashboard object used to pull aggregations from our policyholders info
	def __init__(self,claims):
		self.totalPaid = sum([claim.claimCovered for claim in claims])
		self.averageAge = sum([claim.claimantAge for claim in claims])/len(claims)
		self.yearsWithclaims = {claim.lossYear for claim in claims}
		self.yearClaimCounts = {}
		self.getClaimCounts(claims)
		self.claims = claims
	def getClaimCounts(self,claims):
		for year in self.yearsWithclaims:
			self.yearClaimCounts[year] = sum(claim.lossYear == year for claim in claims)
	def printDashboard(self):
		aggTable = PrettyTable()
		aggTable.field_names = ["Description","Value"]
		aggTable.add_row(["Total Paid",convertToMoney(self.totalPaid)])
		aggTable.add_row(["Average Age",round(self.averageAge,3)])
		yearTable = PrettyTable()
		yearTable.field_names= ["Year","Claim Count"]
		for year in self.yearClaimCounts:
			yearTable.add_row([year,self.yearClaimCounts[year]])
		print(yearTable)
		print(aggTable)
			
			

def convertToMoney(value):
	return '${:,.2f}'.format(value)

def randomDate(beginYear,endYear):
	return str(random.randint(1,12))+"/"+str(random.randint(1,28))+"/"+str(random.randint(beginYear,endYear))

def simulateData(insuredCount):
	insuredList = []
	firstNames = names.words('male.txt')+names.words('female.txt')
	for insured in range(insuredCount):
		insuredList.append(PolicyHolder(random.choice(firstNames),"Smith",randomDate(1970,2000),str(random.randint(100000000,999999999)),random.choice(["Male","Female"]),random.choice(["Y","N"]),[]))
	for insured in insuredList:
		claimCount = random.randint(0,10)
		for claim in range(claimCount):
			bill = random.randint(10,99999)
			insured.reportLoss(randomDate(1990,2019), bill,bill*random.randint(50,100)/100)
	return insuredList
		

def addInsured(data):
	firstName, lastName = str(input("Please enter the insured's full name:\n")).split(" ")
	#  DOB, SSN, gender, smokingStatus, medicalConditions
	DOB = str(input("Please enter the DOB of the insured: \n"))
	SSN = str(input("Please enter the SSN of the insured: \n"))
	Gender = str(input("What is the insured's gender? \n"))
	smokingStatus = str(input("do they smoke? (Y/N)"))
	medicalConditions = str(input("Please input any medical conditions, separated by commas below: \n")).split(",")
	newInsured = PolicyHolder(firstName,lastName,DOB,SSN,Gender,smokingStatus,medicalConditions)
	data.append(newInsured)
	os.system('cls')
	print("The new Insured's unique ID is: %s" % newInsured.uniqueIdentifier)
	return data


def reportClaim(data):
	#lossDate,claimBilled,claimCovered
	findID = str(input("Please enter the ID of the insured you are looking up: \n"))
	for insured in data:
		if insured.uniqueIdentifier == findID:
			lossDate = str(input("please enter the date of loss in MM/DD/YYYY format below: \n"))
			claimBilled = int(input("Please enter the amount billed (numbers only): \n"))
			claimCovered = int(input("Please enter the amount that the bill was covered (numbers only): \n"))
			insured.reportLoss(lossDate,claimBilled,claimCovered)
	return data

def listInsured(data):
	insuredTable = PrettyTable()
	insuredTable.field_names = ["ID","Insured Name","DOB","Gender","Smoking Status","SSN","Claim Count"]
	for insured in data:
		insuredTable.add_row([insured.uniqueIdentifier,insured.fullName,insured.DOB,insured.gender,insured.smokingStatus,insured.SSN,len(insured.claimHistory)])
	return insuredTable
		
def listClaims(data):
	while True:
		findID = str(input("Please enter the ID of the insured you are looking up: \n"))
		for insured in data:
			if insured.uniqueIdentifier == findID:
				claimTable = PrettyTable()
				claimTable.field_names = ["Event Date","Billed Amount","Covered Amount"]
				for claim in insured.claimHistory:
					claimTable.add_row([claim.lossDate,claim.claimBilled,claim.claimCovered])		
		return claimTable
			


def mainMenu(data):
	while True:
		print("Welcome to Health-Connect, please choose from the following options:")
		print("1 - Add an insured name")
		print("2 - Report a Claim")
		print("3 - List all insured individuals")
		print("4 - Display all claims by uniqueIdentifier")
		print("5 - Basic Aggregate Data")
		Option = str(input()).lower()
		if "add" in Option or Option == "1":
			os.system('cls')
			data = addInsured(data)
			continue
		elif ("report" or "claim") in Option or Option == "2":
			os.system('cls')
			data = reportClaim(data)
			continue
		elif "list" in Option or Option == "3":
			os.system('cls')
			print(listInsured(data))
			continue
		elif "display" in Option or Option == "4":
			os.system('cls')
			print(listClaims(data))
			continue
		elif ("aggregate" or "data") in Option or Option == "5":
			os.system('cls')
			claims = []
			for insured in data:
				claims += insured.claimHistory
			Dashboard(claims).printDashboard()
		else:
			os.system('cls')
			print("It seems we did not recognize your input, please try again")
			continue

def startMenu():
	os.system('cls')
	while True:
		simulate = str(input(" Would you like to simulate some random data to sample the program? (Y/N)\n"))
		if simulate.lower().startswith("y"):
			mainMenu(simulateData(20))
		elif simulate.lower().startswith("n"):
			mainMenu([])
		else:
			print("Sorry, please enter 'Y' or 'N'")
			continue

startMenu()