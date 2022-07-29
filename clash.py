import pandas as pd
import numpy as np
from itertools import product
import re


class Time:
	def __init__(self):
		self.slots = []

	def checkIfClashSlot(self,st,et):
		for slot in self.slots:
			if (st <= slot[0] and et >= slot[1]) or (st >= slot[0] and st <= slot[1]) or (et >= slot[0] and et <= slot[1]):
				return True
			else:
				continue

		return False

	def addSlot(self,st,et,course):
		if not self.checkIfClashSlot(st,et):
			self.slots.append((st,et,course))
			return True
		else:
			return False

	def __repr__(self):
		return str(self.slots)

	def __str__(self):
		return str(self.slots)

def sepDays(dayStr):
	days_types = ["Th","M","T","W","F"]

	days = []

	dayString = dayStr[:]

	for day in days_types:
		if day in dayString:
			days.append(day)
			dayString = dayString.replace(day,"")

	return days

def read_csv(file):
	df = pd.read_csv(file)

	return df


def process_df(df):
	courses = list(df["Course"])

	full_courses_dict = {}

	for course in courses:
		sections = {}

		for index, row in df.iterrows():
			if row["Course"] == course:
				section = row["Section"]

				if full_courses_dict.get(course) != None:
					if full_courses_dict.get(course).get(section) != None:
						days = full_courses_dict.get(course).get(section)
				else:
					days = {"M":set([]),"T":set([]),"W":set([]),"Th":set([]),"F":set([])}

				section_days = sepDays(row["Day"])

				for day in section_days:
					days[day].add((row["StartTimeNum"],row["EndTimeNum"]))

				sections[section] = days
		full_courses_dict[course] = sections


	return full_courses_dict

def genCombos(timeTableWithSections):
	combos = [dict(zip(timeTableWithSections, v)) for v in product(*timeTableWithSections.values())]

	return combos



def processCombo(combo, full_courses_dict):
	schedule = {"M":Time(),"T":Time(),"W":Time(),"Th":Time(),"F":Time()}

	for course, section in combo.items():
		course_days = [k for k,v in full_courses_dict[course][section].items() if len(v) > 0]

		for week_day in course_days:
			times = full_courses_dict[course][section][week_day]


			for time in times:
				add = schedule[week_day].addSlot(time[0], time[1], course+" "+str(section))
				if not add:
					return False

	return schedule

def createTimeTable(wantedCourses, full_courses_dict):
	timeTable = {}

	combos = []

	workingCombos = []

	for course in wantedCourses:
		timeTable[course] = full_courses_dict[course]

	timeTableWithSections = {}

	for course in timeTable:
		sections = [k for k,v in timeTable[course].items()]

		timeTableWithSections[course] = sections

	combos = genCombos(timeTableWithSections)

	for combo in combos:
		res = processCombo(combo, full_courses_dict)

		if res:
			workingCombos.append(res)

	return workingCombos

def getAllCourseSectionFromCombo(combo):
	allSlots = [v for k,v in combo.items()]

	sections = []

	for slot in allSlots:
		for section in slot.slots:
			sections.append(section[2])

	sections = set(sections)

	sectionDict = {}

	for section in sections:
		course = section[:-2]
		section_num = section[-2:]

		sectionDict[course] = int(section_num)

	return sectionDict



def exportToCSV(timeTable, wantedCourses, fileName):
	allSections = {}

	for course in wantedCourses:
		allSections[course] = []

	for combo in timeTable:
		sections = getAllCourseSectionFromCombo(combo)

		for k,v in sections.items():
			allSections[k].append(v)

	final_df = pd.DataFrame.from_dict(allSections)

	final_df.to_csv(fileName)

	print("Exported")

	

	

df = read_csv("Fall Semester 2022 Class Schedule - final.csv")

courses = process_df(df)

wantedCourses = ["MATH 102", "CS 210", "SS 102", "CS 200", "CS 225"]

timeTable = createTimeTable(wantedCourses, courses)

exportToCSV(timeTable, wantedCourses, "working.csv")