
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time,json, os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



driver = webdriver.Chrome(ChromeDriverManager().install())

#driver.get('https://id.indeed.com')

# Enter to the site
driver.get('https://www.linkedin.com/login');
time.sleep(2)
# Accept cookies
#driver.find_element("xpath","/html/body/div/main/div[1]/div/section/div/div[2]/button[2]").click()
# User Credentials
# Reading txt file where we have our user credentials

user_name = "naeem.mhedhbi@yahoo.com" # First line
password =  "goonnaim123"
driver.find_element("xpath",'//*[@id="username"]').send_keys(user_name)
driver.find_element("xpath",'//*[@id="password"]').send_keys(password)
time.sleep(1)

# Login button
driver.find_element("xpath",'//*[@id="organic-div"]/form/div[3]/button').click()
driver.implicitly_wait(30)

# Access to the Jobs button and click it
driver.find_element("xpath",'//*[@id="global-nav"]/div/nav/ul/li[3]/a').click()
time.sleep(3)

# Go to search results directly via link
driver.get("https://www.linkedin.com/jobs/search/?geoId=105646813&keywords=Controller&location=Spain")
time.sleep(1)

#jobs_block = driver.find_element("xpath",'//*[@id="main"]/div/section[1]/div')
#jobs_list = driver.find_element("xpath",'//*[@id="main"]/div/section[1]/div/ul')


# Get all links for these offers
links = []
all_links = []
# Navigate 13 pages
print('Links are being collected now.')
try:
    
    for page in range(1,3):
        time.sleep(2)
        #jobs_block = driver.find_element("xpath",'//*[@id="main"]/div/section[1]/div')
        jobs_block = driver.find_element(By.CLASS_NAME,'scaffold-layout__list')
        jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.scaffold-layout__list-item')
        #jobs_list  = driver.find_element("xpath",'//*[@id="main"]/div/section[1]/div/ul')
        #print(jobs_list)
        #type(jobs_list)
        print("job_block : " +str(jobs_block))
        print("job_list : " +str(jobs_block))
        for job in jobs_list:
            all_links = job.find_elements(By.TAG_NAME,'a')
            for a in all_links:
                if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links: 
                    links.append(a.get_attribute('href'))
                else:
                    pass
            # scroll down for each job element
            driver.execute_script("arguments[0].scrollIntoView();", job)
        
        print(f'Collecting the links in the page: {page-1}')
        # go to next page:
        driver.find_element("xpath",f"//button[@aria-label='Page {page}']").click()
        time.sleep(3)
except:
    pass
print('Found ' + str(len(links)) + ' links for job offers')


# Create empty lists to store information
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = [] 
job_desc = []
job_url=[]

i = 0
j = 1

# Visit each link one by one to scrape the information
print('Visiting the links and collecting information just started.')
for i in range(len(links)):
    try:
        job_url.append(links[i])
        driver.get(links[i])
        i=i+1
        time.sleep(2)
        # Click See more.
        driver.find_element(By.CLASS_NAME,"artdeco-card__actions").click()
        time.sleep(2)
    except:
        pass
    
    # Find the general information of the job offers
    contents = driver.find_elements(By.CLASS_NAME,'p5')
    for content in contents:
        try:
            job_titles.append(content.find_element(By.TAG_NAME,"h1").text)
            company_names.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__company-name").text)
            company_locations.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__bullet").text)
            work_methods.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__workplace-type").text)
            post_dates.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__posted-date").text)
            work_times.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__job-insight").text)
            print(f'Scraping the Job Offer {j} DONE.')
            j+= 1
        except:
            pass
        time.sleep(2)
        
        # Scraping the job description
    job_description = driver.find_elements(By.CLASS_NAME,'jobs-description__content')
    for description in job_description:
        job_text = description.find_element(By.CLASS_NAME,"jobs-box__html-content").text
        job_desc.append(job_text)
        print(f'Scraping the Job Offer {j}')
        time.sleep(2)  
            
# Creating the dataframe 
df = pd.DataFrame(list(zip(job_titles,company_names,
                    company_locations,work_methods,
                    post_dates,work_times,job_desc,job_url)),
                    columns =['job_title', 'company_name',
                           'company_location','work_method',
                           'post_date','work_time','job_summary','job_url'])

# Storing the data to csv file
df.to_csv('job_offers_controller_spain.csv', index=False)

# Output job descriptions to txt file
with open(r'C:\Users\121\Documents\vscode\job_descriptions.txt', 'w',encoding="utf-8") as f:
    for line in job_desc:
        f.write(line)
        f.write('\n')
