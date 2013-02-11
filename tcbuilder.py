#!/usr/bin/env python

import os
import re
#import logging
#import time
#from cgi import escape
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
#from google.appengine.ext import db
#from google.appengine.ext.db import Key
#from google.appengine.api import users
#from django.utils import simplejson as json
#from datetime import date
#from datetime import datetime
#from datetime import timedelta
import jinja2

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

PROJECT_NAME = "tcbuilder"

#

allScenarios = []
allScenarios.append({"scen_desc":"Edit - Unlocked configuration", "steps":[]})
allScenarios.append({"scen_desc":"Edit - Locked configuration", "steps":[]})

allScenarios[0]["steps"].append({
	"step_desc":"Navigate to Device Browser,",
	"results":"Device Browser is displayed",
	"notes":""
	})
allScenarios[0]["steps"].append({
	"step_desc":"Select a device that has been fully provisioned in Centcom",
	"results":"",
	"notes":""
	})
allScenarios[0]["steps"].append({
	"step_desc":"Click Open Configuration button",
	"results":"Configuration window is displayed",
	"notes":""
	})
allScenarios[0]["steps"].append({
	"step_desc":"Click Edit button",
	"results":"Configuration window will be in edit mode, Edit button will be disabled",
	"notes":"This change is not instantaneous"
	})


allScenarios[1]["steps"].append({
	"step_desc":"This scenario requires multiple sessions (A and B), and a privelged user",
	"results":"",
	"notes":""
	})
allScenarios[1]["steps"].append({
	"step_desc":"Session A: Follow the directions above in Edit - Unlocked configuration",
	"results":"Device will be in a locked state",
	"notes":""
	})
allScenarios[1]["steps"].append({
	"step_desc":"Session B: Follow the directions above using the same device record",
	"results":"Confirmation dialog requesting user to unlock configuration is displayed",
	"notes":""
	})
allScenarios[1]["steps"].append({
	"step_desc":"Click Yes",
	"results":"Configuration window will be in edit mode, Edit button will be disabled",
	"notes":""
	})

def ReturnScenarioStrings(scenarios) :
	# ReturnScenarioString(scenarios) takes a 'scenarios' variable and returns a dictionary with two keys:
	#	- scenario_html: 1 html table per scenario
	#	- markup_string: full wiki/jira markup of combined tables
	scenario_html = ""
	markup_string = "||Scenario||Steps||Results||Notes||\n"

	for i in range(len(scenarios)) :
		scenario = scenarios[i]
		scenario_html += "<p>" + scenario["scen_desc"] + "</p>"
		scenario_html += "<table id='table-6'>"
		scenario_html += "<tr><th><b>Steps</b></th><th><b>Results</b></th><th><b>Notes</b></th></tr>"

		#for step in scenario["steps"] :
		for j in range(len(scenario["steps"])) :
			step = scenario["steps"][j]

			if j == 0 :
				markup_string += "|" + scenario["scen_desc"] + " "
			else :
				markup_string += "| "

			scenario_html += "<tr>"
			scenario_html += "<td>" + step["step_desc"] + "</td>"
			scenario_html += "<td>" + step["results"] + "</td>"
			scenario_html += "<td>" + step["notes"] + "</td>"
			scenario_html += "</tr>"

			markup_string += "|" + step["step_desc"] + " "
			markup_string += "|" + step["results"] + " "
			markup_string += "|" + step["notes"] + " |\n"

		scenario_html += "</table>"

	# add nbsp to empty cells
	scenario_html = re.sub('\<td\>\<\/td\>', '<td>&nbsp;</td>', scenario_html)

	# return scenario_html, markup_string
	return { "scenario_html": scenario_html, "markup_string": markup_string }

def MarkupToData(markup) :
	#scenarios = allScenarios
	scenarios = []
	# MarkupToData(markup) takes a 'markup' string and returns a complex nested 'scenarios' variable:
	# - scenarios[]
	# - scenarios[i] = {"scen_desc":"SCENARIO TITLE", "steps":[]}
	# - scenarios[i]["steps"] = {
	#		"step_desc":"STEP DESCRIPTION,",
	#		"results":"STEP RESULTS",
	#		"notes":"STEP NOTES"
	#	}

	markup_lines = markup.split("\n|") # split on "\n|" ??
	if re.match("^\|\|", markup_lines[0]) :
		markup_lines.pop(0) # kill header row

	for i in range(len(markup_lines)) :
		cells = markup_lines[i].split("|")
		cells.pop()
		
		# cells[0] is the scenario title (or blank)
		if len(cells[0].strip()) > 0 :	# new scenario!
			throwaway = ""
			scenarios.append({"scen_desc": cells[0].strip(), "steps": []})

		scenarios[len(scenarios) - 1]["steps"].append({
			"step_desc": cells[1].strip(),
			"results": cells[2].strip(),
			"notes": cells[3].strip()
			})
	
	#scenarios = markup_lines[0].split("|")

	#scenarios = markup_lines
	return scenarios

#allScenarios = []
#allScenarios.append({"scen_desc":"Edit - Unlocked configuration", "steps":[]})
#allScenarios.append({"scen_desc":"Edit - Locked configuration", "steps":[]})
#
#allScenarios[0]["steps"].append({
#	"step_desc":"Navigate to Device Browser,",
#	"results":"Device Browser is displayed",
#	"notes":""
#	})
#allScenarios[0]["steps"].append({
#	"step_desc":"Select a device that has been fully provisioned in Centcom",
#	"results":"",
#	"notes":""
#	})

class MainPage(webapp.RequestHandler) :
	def get(self) :
		# allScenarios should be populated

		# Calculate strScenarioHTML/strMarkup from allScenarios
		#strScenarioHTML = "<p>Scenarios!</p>"
		scenarioDict = ReturnScenarioStrings(allScenarios)
		strScenarioHTML = scenarioDict["scenario_html"]
		strMarkup = scenarioDict["markup_string"]

		template_values = {
			'strScenarioHTML': strScenarioHTML,
			'strMarkup': strMarkup
			}

		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))

	def post(self) :
		# we have 3 buttons that can be handled by this post:
		# new_scenario
		# convert2markup
		# convert2tables
		# ...handled by
		# is_delete = request.POST.get('delete_item', None)
		is_new_scenario = self.request.POST.get('new_scenario', None)
		is_convert2markup = self.request.POST.get('convert2markup', None)
		is_convert2tables = self.request.POST.get('convert2tables', None)

		if is_new_scenario :
			strMarkup = "new scenario"
		elif is_convert2markup :
			strMarkup = "convert >>"
		elif is_convert2tables :
			#strMarkup = "<< convert"
			markup = self.request.POST.get('markup')
			allScenarios = MarkupToData(markup)

			strMarkup = ""
			#for i in range(len(allScenarios)) :
			#	strMarkup += "[" + str(i) + "]: " + allScenarios[i] + "\n"

		else :
			raise Exception("no form action given")

		scenarioDict = ReturnScenarioStrings(allScenarios)
		strScenarioHTML = scenarioDict["scenario_html"]
		#strScenarioHTML = ""
		strMarkup = scenarioDict["markup_string"]

		template_values = {
			'strScenarioHTML': strScenarioHTML,
			'strMarkup': strMarkup
			}

		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))

class AnotherPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write("<p>user info</p>")
		#self.response.out.write('</body></html>')

application = \
	webapp.WSGIApplication([('/', MainPage),
							('/anotherpage', AnotherPage)
							],
							debug=True)

						  
def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()
