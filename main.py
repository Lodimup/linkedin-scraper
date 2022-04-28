from console import console
from rich import inspect
from selenium import webdriver
from bs4 import BeautifulSoup
# from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()


driver = webdriver.Chrome()
url = 'https://www.linkedin.com/jobs/search?keywords=developer&location=Bangkok%2C%20Bangkok%20City%2C%20Thailand&geoId=109988095&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&currentJobId=3038779681'
driver.get(url)

content = driver.find_elements_by_class_name('base-card__full-link')

class LJob:
    def __init__(self, job_title, org_name):
        self.job_title = job_title
        self.org_name = org_name
        self.job_description = job_description
    
    def __str__(self):
        return self.job_title
    
    def __repr__(self):
        return self.__str__()

l_ljobs = []
for i in content:
    link = i.get_attribute('href')
    driver = webdriver.Chrome()
    driver.get(link)
    job_title = driver.find_element_by_class_name('top-card-layout__title').get_attribute('innerHTML')
    org_name = driver.find_element_by_class_name('topcard__org-name-link').get_attribute('innerHTML')
    btn = driver.find_element_by_class_name('show-more-less-html__button')
    btn.click()
    job_description = driver.find_element_by_class_name('show-more-less-html__markup').get_attribute('innerHTML')
    job_description = BeautifulSoup(job_description, features='html.parser').get_text()
    job_title = job_title.strip()
    org_name = org_name.strip()
    
    ljob = LJob(job_title, org_name, job_description)
    l_ljobs.append(ljob)
    
    driver.close()

input('Press Enter to continue...')