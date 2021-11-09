from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import datetime

urls = ['https://www.linkedin.com/jobs/search?keywords=cyber%20security&location=Nashville%2C%20Tennessee%2C%20United%20States&geoId=105573479&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
	,'file:///C:/Users/acook/Downloads/614%20Cyber%20Security%20jobs%20in%20Nashville,%20Tennessee,%20United%20States%20(19%20new).html']
url=urls[0]
wd = webdriver.Chrome(executable_path='./chromedriver.exe')
wd.get(url)

no_of_jobs = int(wd.find_element(By.CSS_SELECTOR,'h1>span').get_attribute('innerText'))

#load the whole page with a combination of scrolling and clicking a "show more" button
#speed up. sleep(1)
#change to while (you aren't at the bottom) instead of trying to count cause it might miss one and throw it off

print(no_of_jobs)
print(len(wd.find_element(By.CLASS_NAME,'jobs-search__results-list').find_elements(By.TAG_NAME,'li')))
i = 2
while len(wd.find_element(By.CLASS_NAME,'jobs-search__results-list').find_elements(By.TAG_NAME,'li'))<no_of_jobs and i<3: #i<4 for testing - faster
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
job_lists = wd.find_element(By.CLASS_NAME,'jobs-search__results-list')
jobs = job_lists.find_elements(By.TAG_NAME,'li') # return a list

print(no_of_jobs)


job_id= []
job_title = []
company_name = []
location = []
date = []
job_link = []
for job in jobs:
	job_id0 = job.get_attribute('data-id')
	job_id.append(job_id0)
	
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
	
jd = []
seniority = []
emp_type = []
job_func = []
industries = []
descriptions = []
for item in range(len(jobs)):
	if 1==1:
		try:
			print(item)
			job_func0=[]
			industries0=[]
			descriptions0=[]
			# clicking job to view job details
			job_click_path = f'//*[@id="main-content"]/section[2]/ul/li[{item+1}]/div/a'#//*[@id="main-content"]/section[2]/ul/li[1]/div/a
			job_click = job.find_element(By.XPATH,job_click_path).click()
			time.sleep(5)

			detail_path='/html/body/div[1]/div/section'
			detail_section=wd.find_element(By.XPATH,detail_path)

			showmore_click_path = 'div.decorated-job-posting__details > section.core-section-container.description > div > div > section > button.show-more-less-html__button.show-more-less-html__button--more'
			showmore_click = 	detail_section.find_element(By.CSS_SELECTOR,showmore_click_path).click()

			jd_path = 'show-more-less-html__markup'
			jd0 = wd.find_element(By.CLASS_NAME,jd_path).get_attribute('innerText')
			jd.append(jd0)

			#maybe just get the list of attributes: description__job-criteria-list

			description_class='description__job-criteria-list'
			description_element= wd.find_element(By.CLASS_NAME,description_class)
			item_class='description__job-criteria-item'
			description_items=description_element.find_elements(By.CLASS_NAME,item_class)
			item_description_class = 'description__job-criteria-text'
			for item in description_items:
				item0=item.find_element(By.CLASS_NAME,item_description_class).get_attribute('innerText')
				descriptions0.append(item0)
			
			#descriptions_final = ', '.join(descriptions0)
			descriptions.append(descriptions0)
		except:
			jd0='error'
			jd.append(jd0)
			descriptions0=['error']
			descriptions.append(descriptions0)


	# for element in description_elements:
	# 	descriptions0.append(element.get_attribute())
	
	# seniority_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span'
	# seniority0 = wd.find_element(By.XPATH,seniority_path).get_attribute('innerText')
	# seniority.append(seniority0)
	
	# emp_type_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span'
	# emp_type0 = wd.find_element(By.XPATH,emp_type_path).get_attribute('innerText')
	# emp_type.append(emp_type0)
 
	# job_func_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[3]/span'
	# job_func_elements = wd.find_elements(By.XPATH,job_func_path)
	# for element in job_func_elements:
    #      job_func0.append(element.get_attribute('innerText'))
    #      job_func_final = ', '.join(job_func0)
    #      job_func.append(job_func_final)
	
	# industries_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[4]/span'
	# industries_elements = wd.find_elements(By.XPATH,industries_path)
	# for element in industries_elements:
    #      industries0.append(element.get_attribute('innerText'))
    #      industries_final = ', '.join(industries0)
    #      industries.append(industries_final)
 
job_data = pd.DataFrame({'ID': job_id,
	'Date': date,
	'Company': company_name,
	'Title': job_title,
	'Location': location,
	'Description': jd,
	'Sub descriptions': descriptions,
	'Link': job_link
	})

# cleaning description column
job_data['Description'] = job_data['Description'].str.replace('\n',' ')
filename='LinkedIn Job Data_Data Scientist'+datetime.now().strftime("%m%d%Y%H%M%S")+'.csv'
job_data.to_csv(filename, index = False, sep='|')
#job_data.to_excel('LinkedIn Job Data_Data Scientist.xlsx', index = False)