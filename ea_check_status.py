import requests
from lxml import html

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
	session_request.post(login_url, data = payload, headers = dict(referer = login_url))
	# The referer in the GET call was earlier the 'status_page'. This returned wrong
	# results and since has been replaced with 'login_url'.
	result = session_request.get(status_page, headers = dict(referer = login_url))
	tree = html.fromstring(result.content)
	# Xpath function to get current status.
	status = list(tree.xpath("//table[@class='progress-table']/tbody/tr/td[3]/text()"))[0]
	return status

if __name__ == '__main__':
	ea_username = 'vinayak1986@gmail.com'
	ea_pwd = 'H312@blr'
	ea_login_url = 'https://portal.engineersaustralia.org.au/user/login?destination=estage1/applicant'
	ea_status_page = 'https://portal.engineersaustralia.org.au/estage1/applicant'
	status = get_app_status(ea_username, ea_pwd, ea_login_url, ea_status_page)
	print(status)

