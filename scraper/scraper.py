from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import pandas as pd
from datetime import datetime
import platform
import credsPASSWORDS as credsPASSWORDS
import re

from sqlalchemy import engine, types

def sqlEngineMaker(modeIn):
	mode = modeIn 

	if mode == 'mysql':
		credentials = credsPASSWORDS.mySql
		connection_type='pymysql'	
	elif mode == 'digitalOcean':
		credentials = credsPASSWORDS.digitalOcean
		connection_type='mysqlconnector'		
	else:
		raise Exception("Don't support database: " + mode)

	connection_string = "mysql+"+connection_type+"://" + credentials['user'] + ":" + credentials['password'] + "@" + credentials['host'] + ":" + credentials['port']
	return engine.create_engine(connection_string)  # mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

def runChrome():	
	# TODO make chrome Web Driver function
	chrome_options = Options()
	chrome_options.add_argument("--window-size=1920,1080")
	chrome_options.add_argument("--verbose")
	chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
	# chrome_options.add_argument("--headless")
	
	system = platform.system()
	if system == 'Windows':
		s = Service('./scraper/chromedriver.exe')
		wd = webdriver.Chrome(options=chrome_options, service=s)#  executable_path='./scraper/chromedriver.exe')
	elif system == 'Darwin':
		# s = Service('./chromedriver')
		wd = webdriver.Chrome(options=chrome_options, executable_path='./scraper/chromedriver')
	else:
		raise Exception("Don't have an executable for: " + system)
	return wd

def loadPage(wd,url):
	wd.get(url)
	no_of_jobs = int(wd.find_element(By.CSS_SELECTOR, 'h1>span').get_attribute('innerText'))

	# load the whole page with a combination of scrolling and clicking a "show more" button

	print(no_of_jobs)
	print(len(wd.find_element(By.CLASS_NAME, 'jobs-search__results-list').find_elements(By.TAG_NAME, 'li')))
	i = 2
	while len(wd.find_element(By.CLASS_NAME, 'jobs-search__results-list').find_elements(By.TAG_NAME,
																						'li')) < no_of_jobs and i < 4:  # i<4 for testing - faster
		print(len(wd.find_element(By.CLASS_NAME, 'jobs-search__results-list').find_elements(By.TAG_NAME, 'li')))
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		i = i + 1
		try:
			wd.find_element(By.XPATH, '//*[@id="main-content"]/section[2]/button').click()
			time.sleep(4)
		except WebDriverException:
			pass
			time.sleep(4)
	return

def main():
	
	wd = runChrome()

	urls = [
		'https://www.linkedin.com/jobs/search?keywords=Cybersecurity&location=Nashville%2C%20Tennessee%2C%20United%20States&geoId=105573479&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
		,'https://www.google.com'
		]
	url = urls[0]	

	loadPage(wd,url)
	
	# now that everything is loaded, get info about the page

	# TODO make get job info function
	job_lists = wd.find_element(By.CLASS_NAME, 'jobs-search__results-list')
	jobs = job_lists.find_elements(By.TAG_NAME, 'li')  # return a list

	job_id = []
	job_urn = []
	job_title = []
	company_name = []
	location = []
	date = []
	job_link = []
	k = 0
	for job in jobs:

		if k > 1:
			break

		# job_id0 = job.get_attribute('data-id') # don't think job id is a thing anymore
		job_id0 = k
		job_id.append(job_id0)
		# jar[k]=job_id0

		k = k + 1

		job_urn0 = job.find_element(By.CSS_SELECTOR, 'div').get_attribute('data-entity-urn')
		job_urn_id = job_urn0.split(":")[3]
		job_urn.append(job_urn_id)
		# main-content > section.two-pane-serp-page__results-list > ul > li:nth-child(2) > div

		job_title0 = job.find_element(By.CSS_SELECTOR, 'div > div.base-search-card__info > h3').get_attribute(
			'innerText')
		job_title.append(job_title0)

		company_name0 = job.find_element(By.CSS_SELECTOR, 'div > div.base-search-card__info > h4 > a').get_attribute(
			'innerText')
		company_name.append(company_name0)

		location0 = job.find_element(By.CSS_SELECTOR, 'div > div.base-search-card__info > div > span').get_attribute(
			'innerText')
		location.append(location0)

		date0 = job.find_element(By.CSS_SELECTOR, 'div > div.base-search-card__info > div > time').get_attribute(
			'datetime')
		date.append(date0)

		job_link0 = job.find_element(By.CSS_SELECTOR, 'div > a').get_attribute('href')
		job_link.append(job_link0)

	# TODO make get descriptions function
	jd = []
	descriptions = []

	# len(jobs)
	for item in range(k):

		descriptions0 = {
			'ID': job_id[item],
			'URN': "",
			'Seniority level': "",
			'Employment type': "",
			'Job function': "",
			'Industries': "",
		}

		try:
			# clicking job to view job details
			job_click_path = F'//*[@id="main-content"]/section[2]/ul/li[{item + 1}]/div/a'
			job_click_element = wd.find_element(By.XPATH, job_click_path)
			desc_urn_match = re.search("\d*(?=\?refId)", job_click_element.get_attribute('href'))
			desc_urn = desc_urn_match.group(0)
			descriptions0['URN'] = desc_urn
			job_click_element.click()
			time.sleep(5)

			detail_path = '/html/body/div[1]/div/section'
			detail_section = wd.find_element(By.XPATH, detail_path)

			show_more_click_path = 'div.decorated-job-posting__details > section.core-section-container.description > div > div > section > button.show-more-less-html__button.show-more-less-html__button--more'
			detail_section.find_element(By.CSS_SELECTOR, show_more_click_path).click()

			jd_path = 'show-more-less-html__markup'
			jd0 = wd.find_element(By.CLASS_NAME, jd_path).get_attribute('innerText')
			jd.append(jd0)

			# descriptions exist in a series of <li> containers. it's easier to just loop through that list
			description_class = 'description__job-criteria-list'
			description_element = wd.find_element(By.CLASS_NAME, description_class)
			item_class = 'description__job-criteria-item'
			description_items = description_element.find_elements(By.CLASS_NAME, item_class)
			item_description_class = 'description__job-criteria-text'
			item_name = 'description__job-criteria-subheader'

			for d_item in description_items:
				item0 = d_item.find_element(By.CLASS_NAME, item_description_class).get_attribute('innerText')

				d_item_name = d_item.find_element(By.CLASS_NAME, item_name).get_attribute('innerText')
				descriptions0[d_item_name] = item0

			descriptions.append(descriptions0)
		except WebDriverException:
			jd0 = 'error'
			jd.append(jd0)
			descriptions0['Seniority level'] = 'error'
			descriptions0['Employment type'] = 'error'
			descriptions0['Job function'] = 'error'
			descriptions0['Industries'] = 'error'
			descriptions.append(descriptions0)

	wd.close()

	job_data = pd.DataFrame({'ID': job_id,
							 'URN': job_urn,
							 'Date': date,
							 'Company': company_name,
							 'Title': job_title,
							 'Location': location,
							 'Description': jd,
							 'Link': job_link,
							 })

	description_data = pd.DataFrame.from_dict(data=descriptions)

	print(job_data)
	print(description_data)

	full_data = job_data.join(description_data, how='inner', on='ID', lsuffix='_left', rsuffix='_right')

	# TODO make output function

	# cleaning description column
	full_data['Description'] = full_data['Description'].str.replace('\n', ' ')
	filename = 'LinkedIn Job Data_Data Scientist' + datetime.now().strftime("%m%d%Y%H%M%S") + '.csv'

	#TODO parameterize output - csv, sql, both, etc

	# full_data.to_csv(filename, index=False, sep='|')
	# job_data.to_excel('LinkedIn Job Data_Data Scientist.xlsx', index = False)

	print(full_data)

	test_types = dict(
		zip(full_data.columns.tolist(), (types.VARCHAR(length=20), types.VARCHAR(length=20), types.VARCHAR(length=200)
										 , types.VARCHAR(length=20), types.VARCHAR(length=200),
										 types.VARCHAR(length=400), types.VARCHAR(length=400), types.TEXT(length=20000)
										 , types.VARCHAR(length=400), types.VARCHAR(length=20),
										 types.VARCHAR(length=200), types.VARCHAR(length=400),
										 types.VARCHAR(length=400), types.VARCHAR(length=400),
										 types.VARCHAR(length=400))))

	full_data = full_data.astype(str)
	
	mode='mysql'	

	mysql_engine = sqlEngineMaker(mode)	
	full_data.to_sql('jobs', con=mysql_engine, schema='scraper', if_exists='append', index=False, chunksize=None,
					 dtype=test_types, method=None)

	quit()  # windows hangs? chromedriver issue

if __name__== "__main__" :
	main()
