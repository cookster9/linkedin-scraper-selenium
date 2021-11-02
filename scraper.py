from selenium import webdriver
import time
import pandas as pd

urls = ['https://www.linkedin.com/jobs/search?keywords=cyber%20security&location=Nashville%2C%20Tennessee%2C%20United%20States&geoId=105573479&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0']
url=urls[0]
wd = webdriver.Chrome(executable_path='./chromedriver.exe')
wd.get(url)

no_of_jobs = int(wd.find_element_by_css_selector('h1>span').get_attribute('innerText'))

#load the whole page with a combination of scrolling and clicking a "show more" button
i = 2
while i <= int(no_of_jobs/25)+1: 
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1
    try:
        wd.find_element_by_xpath('//*[@id="main-content"]/section[2]/button').click()
        time.sleep(5)
    except:
        pass
        time.sleep(5)

#now that everything is loaded, get info about the page
job_lists = wd.find_element_by_class_name('jobs-search__results-list')
jobs = job_lists.find_elements_by_tag_name('li') # return a list

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
	
	job_title0 = job.find_element_by_css_selector('h3').get_attribute('innerText')
	job_title.append(job_title0)
	
	company_name0 = job.find_element_by_css_selector('h4').get_attribute('innerText')
	company_name.append(company_name0)
	
	location0 = job.find_element_by_css_selector('[class=”job-result-card__location”]').get_attribute('innerText')
	location.append(location0)
	
	date0 = job.find_element_by_css_selector('div>div>time').get_attribute('datetime')
	date.append(date0)
	
	job_link0 = job.find_element_by_css_selector('a').get_attribute('href')
	job_link.append(job_link0)
	
jd = []
seniority = []
emp_type = []
job_func = []
industries = []
for item in range(len(jobs)):
	job_func0=[]
	industries0=[]
	# clicking job to view job details
	job_click_path = f'/html/body/main/div/section[2]/ul/li[{item+1}]/img'
	job_click = job.find_element_by_xpath(job_click_path).click()
	time.sleep(5)
	
	jd_path = '/html/body/main/section/div[2]/section[2]/div'
	jd0 = job.find_element_by_xpath(jd_path).get_attribute('innerText')
	jd.append(jd0)
	
	seniority_path = '/html/body/main/section/div[2]/section[2]/ul/li[1]/span'
	seniority0 = job.find_element_by_xpath(seniority_path).get_attribute('innerText')
	seniority.append(seniority0)
	
	emp_type_path = '/html/body/main/section/div[2]/section[2]/ul/li[2]/span'
	emp_type0 = job.find_element_by_xpath(emp_type_path).get_attribute('innerText')
	emp_type.append(emp_type0)
 
	job_func_path = '/html/body/main/section/div[2]/section[2]/ul/li[3]/span'
	job_func_elements = job.find_elements_by_xpath(job_func_path)
	for element in job_func_elements:
         job_func0.append(element.get_attribute('innerText'))
         job_func_final = ', '.join(job_func0)
         job_func.append(job_func_final)
	
	industries_path = '/html/body/main/section/div[2]/section[2]/ul/li[4]/span'
	industries_elements = job.find_elements_by_xpath(industries_path)
	for element in industries_elements:
         industries0.append(element.get_attribute('innerText'))
         industries_final = ', '.join(industries0)
         industries.append(industries_final)
 
job_data = pd.DataFrame({'ID': job_id,
'Date': date,
'Company': company_name,
'Title': job_title,
'Location': location,
'Description': jd,
'Level': seniority,
'Type': emp_type,
'Function': job_func,
'Industry': industries,
'Link': job_link
})
# cleaning description column
job_data['Description'] = job_data['Description'].str.replace('\n',' ')
job_data.to_excel('LinkedIn Job Data_Data Scientist.xlsx', index = False)