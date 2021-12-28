from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import datetime
import platform
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import mysql.connector
import credsPASSWORDS
import pymysql
import re

from sqlalchemy import engine, types

#TODO clean up imports

#TODO create main function

#TODO make connector function
mode='mysql'#pass this in somehow
creds={
	'host':"",
	'user':"",
	'password':"",
	'port':""
}

if mode=='mysql':
	creds=credsPASSWORDS.mySql
elif mode=='digitalOcean':
	creds=credsPASSWORDS.digitalOcean
else:
	raise Exception("Don't support database: "+mode)

host=creds['host']
user=creds['user']
password=creds['password']
port=creds['port']

mysql_engine=''

if mode=='mysql':
	#mysql_engine=mysql.connector.connect(user=user, password=password,host=host,database='scraper')
	connectionString = "mysql+pymysql://" + user + ":" + password + "@" + host + ":" + port
	mysql_engine = engine.create_engine(connectionString)
elif mode=='digitalOcean':
	connectionString="mysql+mysqlconnector://"+user+":"+password+"@"+host+":"+port
	mysql_engine = engine.create_engine(connectionString) #mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
else:
	raise Exception("Don't support database: "+mode)

#TODO make chrome webdriver function
chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--verbose")
#chrome_options.add_argument("--headless")

urls = ['https://www.linkedin.com/jobs/search?keywords=cyber%20security&location=Nashville%2C%20Tennessee%2C%20United%20States&geoId=105573479&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
	,'file:///C:/Users/acook/Downloads/614%20Cyber%20Security%20jobs%20in%20Nashville,%20Tennessee,%20United%20States%20(19%20new).html'
		,'file:///Users/andrewcook/Documents/GitHub/linkedin-scraper-selenium/job_page2.html']
url=urls[0]
# wd = webdriver.get("file://" + path)
system=platform.system()
wd=[]
if system=='Windows' :
	s = Service('./chromedriver.exe')
	wd = webdriver.Chrome(service=s, options=chrome_options)
elif  system=='Darwin' :
	#s = Service('./chromedriver')
	wd=webdriver.Chrome(options=chrome_options, executable_path='./chromedriver')
else:
	raise Exception("Don't have an executable for: "+system)

#TODO make job loader function to load full page
wd.get(url)
no_of_jobs = int(wd.find_element(By.CSS_SELECTOR,'h1>span').get_attribute('innerText'))

#load the whole page with a combination of scrolling and clicking a "show more" button
#speed up. sleep(1)
#change to while (you aren't at the bottom) instead of trying to count cause it might miss one and throw it off

print(no_of_jobs)
print(len(wd.find_element(By.CLASS_NAME,'jobs-search__results-list').find_elements(By.TAG_NAME,'li')))
i = 2
while len(wd.find_element(By.CLASS_NAME,'jobs-search__results-list').find_elements(By.TAG_NAME,'li'))<no_of_jobs and i<4: #i<4 for testing - faster
	print(len(wd.find_element(By.CLASS_NAME,'jobs-search__results-list').find_elements(By.TAG_NAME,'li')))
	wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	i = i + 1	
	try:
		wd.find_element(By.XPATH,'//*[@id="main-content"]/section[2]/button').click()
		time.sleep(4)
	except:
		pass
		time.sleep(4)

#now that everything is loaded, get info about the page

#TODO make get job info function
job_lists = wd.find_element(By.CLASS_NAME,'jobs-search__results-list')
jobs = job_lists.find_elements(By.TAG_NAME,'li') # return a list

print(no_of_jobs)


job_id= []
job_urn = []
job_title = []
company_name = []
location = []
date = []
job_link = []
jar=[]
k=0
for job in jobs:

	if k>1:
		break

	# job_id0 = job.get_attribute('data-id') # don't think job id is a thing anymore
	job_id0=k
	job_id.append(job_id0)
	#jar[k]=job_id0
	

	k = k + 1

	job_urn0 = job.find_element(By.CSS_SELECTOR,'div').get_attribute('data-entity-urn')
	job_urn_id = job_urn0.split(":")[3]
	job_urn.append(job_urn_id)
	# main-content > section.two-pane-serp-page__results-list > ul > li:nth-child(2) > div

	job_title0 = job.find_element(By.CSS_SELECTOR,'div > div.base-search-card__info > h3').get_attribute('innerText')
	job_title.append(job_title0)
	
	company_name0 = job.find_element(By.CSS_SELECTOR,'div > div.base-search-card__info > h4 > a').get_attribute('innerText')
	company_name.append(company_name0)
	
	location0 = job.find_element(By.CSS_SELECTOR,'div > div.base-search-card__info > div > span').get_attribute('innerText')
	location.append(location0)
	
	date0 = job.find_element(By.CSS_SELECTOR,'div > div.base-search-card__info > div > time').get_attribute('datetime')
	date.append(date0)
	
	job_link0 = job.find_element(By.CSS_SELECTOR,'div > a').get_attribute('href')
	job_link.append(job_link0)

#TODO make get descriptions function
jd = []
seniority = []
emp_type = []
job_func = []
industries = []
descriptions = []
desc_urns = []

#len(jobs)
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
		job_func0=[]
		industries0=[]
		# clicking job to view job details
		job_click_path=F'//*[@id="main-content"]/section[2]/ul/li[{item+1}]/div/a'
		job_click_element = job.find_element(By.XPATH,job_click_path)
		print(job_click_element)
		desc_urn_match = re.search("\d*(?=\?refId)",job_click_element.get_attribute('href'))
		print(desc_urn_match)
		desc_urn = desc_urn_match.group(0)
		print(desc_urn)
		#desc_urns.append(desc_urn)
		descriptions0['URN']=desc_urn
		clickWorked = job_click_element.click()
		time.sleep(5)

		detail_path='/html/body/div[1]/div/section'
		detail_section=wd.find_element(By.XPATH,detail_path)

		showmore_click_path = 'div.decorated-job-posting__details > section.core-section-container.description > div > div > section > button.show-more-less-html__button.show-more-less-html__button--more'
		showmore_click = 	detail_section.find_element(By.CSS_SELECTOR,showmore_click_path).click()

		jd_path = 'show-more-less-html__markup'
		jd0 = wd.find_element(By.CLASS_NAME,jd_path).get_attribute('innerText')
		jd.append(jd0)			

		#descriptions exist in a series of <li> containers. it's easier to just loop through that list
		description_class='description__job-criteria-list'
		description_element= wd.find_element(By.CLASS_NAME,description_class)
		item_class='description__job-criteria-item'
		description_items=description_element.find_elements(By.CLASS_NAME,item_class)
		item_description_class = 'description__job-criteria-text'
		item_name = 'description__job-criteria-subheader'
		
		for d_item in description_items:
			item0=d_item.find_element(By.CLASS_NAME,item_description_class).get_attribute('innerText')
			
			itemName=d_item.find_element(By.CLASS_NAME,item_name).get_attribute('innerText')
			descriptions0[itemName]=item0							
		
		descriptions.append(descriptions0)
	except:
		jd0='error'
		jd.append(jd0)
		descriptions0['Seniority level'] = 'error'
		descriptions0['Employment type'] = 'error'
		descriptions0['Job function'] = 'error'
		descriptions0['Industries'] = 'error'
		descriptions.append(descriptions0)
 
job_data = pd.DataFrame({'ID': job_id,
	'URN': job_urn,
	'Date': date,
	'Company': company_name,
	'Title': job_title,
	'Location': location,
	'Description': jd,	
	'Link': job_link,
	})

description_data=pd.DataFrame.from_dict(descriptions)

print(job_data)
print(description_data)

full_data=job_data.join(description_data, how='inner', on='ID', lsuffix='_left', rsuffix='_right')

#TODO make output function

#cleaning description column
full_data['Description'] = full_data['Description'].str.replace('\n',' ')
filename='LinkedIn Job Data_Data Scientist'+datetime.now().strftime("%m%d%Y%H%M%S")+'.csv'
full_data.to_csv(filename, index = False, sep='|')
#job_data.to_excel('LinkedIn Job Data_Data Scientist.xlsx', index = False)

print(full_data)

name='jobs'
#con=mydb
test_types=dict(zip(full_data.columns.tolist(),(types.VARCHAR(length=20), types.VARCHAR(length=20), types.VARCHAR(length=200)
, types.VARCHAR(length=20), types.VARCHAR(length=200), types.VARCHAR(length=400), types.VARCHAR(length=400), types.TEXT(length=20000)
, types.VARCHAR(length=400), types.VARCHAR(length=20), types.VARCHAR(length=200), types.VARCHAR(length=400), types.VARCHAR(length=400), types.VARCHAR(length=400), types.VARCHAR(length=400))))

full_data=full_data.astype(str)
full_data.to_sql('jobs', con=mysql_engine, schema='scraper', if_exists='append', index=False, chunksize=None, dtype=test_types, method=None)

quit() #windows hangs? chromedriver issue

#TODO add __main__ conditional