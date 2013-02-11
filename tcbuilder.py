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


class MainPage(webapp.RequestHandler):
	def get(self):
		#self.response.out.write("<p>content</p>")

		# Calculate strScenarioHTML from allScenarios
		#strScenarioHTML = "<p>Scenarios!</p>"
		strScenarioHTML = ""
		for scenario in allScenarios:
			strScenarioHTML += "<p>" + scenario["scen_desc"] + "</p>"
			strScenarioHTML += "<table id='table-6'>"
			strScenarioHTML += "<tr><th><b>Steps</b></th><th><b>Results</b></th><th><b>Notes</b></th></tr>"
			for step in scenario["steps"]:
				strScenarioHTML += "<tr>"
				strScenarioHTML += "<td>" + step["step_desc"] + "</td>"
				strScenarioHTML += "<td>" + step["results"] + "</td>"
				strScenarioHTML += "<td>" + step["notes"] + "</td>"
				strScenarioHTML += "</tr>"
			strScenarioHTML += "</table>"

		# add nbsp to empty cells
		strScenarioHTML = re.sub('\<td\>\<\/td\>', '<td>&nbsp;</td>', strScenarioHTML)

		# Calculate strMarkup from allScenarios
		strMarkup = "|| Scenario || Steps || Expected Results || Notes ||\n| Edit - Unlock configuration | Navigate to Device Browser | Device Browser is displayed |  |"

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
