from selenium import webdriver
from pprint import pprint

# create a webdriver object for PhantomJS
driver = webdriver.PhantomJS(executable_path='/usr/local/lib/node_modules/phantomjs/lib/phantom/bin/phantomjs')
driver.implicitly_wait(10)

# navigate to the login page
driver.get("https://goldcoast.cs.adventist.edu.au/#?page=/timetable")

password = "asdfghjkl;'"

# find the form element and fill in the login form
email_field = driver.find_element_by_css_selector(".username")
password_field = driver.find_element_by_name(".password")
email_field.send_keys("gc021217@goldcoastcc.qld.edu.au")
password_field.send_keys(password)

# submit the form
driver.find_element_by_css_selector("button[type='submit']").click()

# navigate to the desired page
driver.get("https://goldcoast.cs.adventist.edu.au/seqta/student/load/timetable")

# scrape the data you need
# element = driver.find_element_by_css_selector(".timetable")
data = driver.page_source
pprint(data)

# close the browser
driver.quit()
