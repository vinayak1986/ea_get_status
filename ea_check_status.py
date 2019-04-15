import requests
from lxml import html
import re
import time, datetime

# Function to get application status from EA portal.
def get_app_status(user_name, password, login_url, status_page):
	session_request = requests.session()
	# Get the hidden 'form_build_id' parameter from the login page.
	# This should be passed in to the POST call.
	result = session_request.get(login_url)
	tree = html.fromstring(result.text)
	site_token = list(tree.xpath("//input[@name = 'form_build_id']/@value"))[0]
	# The params for the POST call were determined from 'Network Monitor' in Firefox.
	payload = {'name' : user_name, 'pass' : password, 'op' : 'Login', 'form_build_id' : site_token, 'form_id' : 'user_login'}
	# Try the POST logic 5 times if an error code is returned.
	found = False
	n_tries = 1
	while (not found) and (n_tries <= 5):
		try:
			response = session_request.post(login_url, data = payload, headers = dict(referer = login_url))
			if response.status_code == '200':
				found = True
			n_tries += 1
		except:
			pass
	# The referer in the GET call was earlier the 'status_page'. This returned wrong
	# results and since has been replaced with 'login_url'.
	result = session_request.get(status_page, headers = dict(referer = login_url))
	tree = html.fromstring(result.content)
	# Xpath function to get current status.
	status = list(tree.xpath("//table[@class='progress-table']/tbody/tr/td[3]/text()"))[0]
	return status

def send_sms():
	url = "https://www.fast2sms.com/dev/bulk"
	payload = "sender_id=FSTSMS&language=english&route=qt&numbers=9739679174,9480373931&message=8923"
	headers = {'authorization': "Gs5QbmdjV9IEwKnXfBhRCPtL0paJ1Fviur7leA3ZzWU8HNTkq4SWupjCDAR74wTgtLX5Fl0qeUOkmodM",
    		   'cache-control': "no-cache",
    		   'content-type': "application/x-www-form-urlencoded"}
	requests.request("POST", url, data=payload, headers=headers)

if __name__ == '__main__':
	time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	ea_username = 'vinayak1986@gmail.com'
	ea_pwd = 'H312@blr'
	ea_login_url = 'https://portal.engineersaustralia.org.au/user/login?destination=estage1/applicant'
	ea_status_page = 'https://portal.engineersaustralia.org.au/estage1/applicant'
	status = get_app_status(ea_username, ea_pwd, ea_login_url, ea_status_page)
	print('{} : {}'.format(time_stamp, status))
    # Send SMS if the status changes from 'Queued for assessment'
	if (not re.match('Queued', status)) and status:
		send_sms()

