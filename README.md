TCBuilder
=========

Test Case Builder
----
[general description]
TCBuilder is a python-based (with some javascript help) web application, intended to easily create test scenarios and steps for a standard software QA test case.

Input:
- scenarios/steps
- reordering scenarios/steps

Output:
- visual table
- jira/wiki markup

Physical layout:
- HTML tables of scenarios/steps
- multiline textbox for jira/wiki markup

----
[objects used]
- Test Case, collection of Scenarios
- Scenario, collection of Test Steps
- Test Step, containing:
	- step description
	- results
	- notes

----
[Actions]
- add scenario
- change scenario title
- add step
- change step data
- reorder scenarios (backlog)
- reorder steps (backlog)
- convert TO markup
- convert FROM markup (backlog)

----
[example data structure layout for app]

allScenarios = []
allScenarios.append({"scen_desc":"first scenario", "steps":[]})
allScenarios[0]["steps"].append({"step_desc":"first step description", "results":"first results", "notes":"any notes"})
allScenarios[0]["steps"].append({"notes": "some other notes", "results": "second results", "step_desc": "second step"})

----
[features]
- bulk import of scenario names
- import of jira/wiki format
- conversion of jira/wiki to TCBuilder