import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from console import console
from rich import inspect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

driver = webdriver.Chrome()
url = 'https://www.linkedin.com/jobs/search?keywords=developer&location=Bangkok%2C%20Bangkok%20City%2C%20Thailand&geoId=109988095&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&currentJobId=3038779681'
driver.get(url)

content = driver.find_elements_by_class_name('base-card__full-link')

class LJob:
    def __init__(self, job_title, org_name, job_description):
        self.job_title = job_title
        self.org_name = org_name
        self.job_description = job_description
    
    def __str__(self):
        return self.job_title
    
    def __repr__(self):
        return self.__str__()

l_ljobs = []
for i in content:
    try:
        options = Options()
        options.headless = True
        
        link = i.get_attribute('href')
        link = link.split('?')[0]
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        job_title = driver.find_element_by_class_name('top-card-layout__title').get_attribute('innerHTML')
        org_name = driver.find_element_by_class_name('topcard__org-name-link').get_attribute('innerHTML')
        btn = driver.find_element_by_class_name('show-more-less-html__button')
        btn.click()
        job_description = driver.find_element_by_class_name('show-more-less-html__markup').get_attribute('innerHTML')
        job_description = BeautifulSoup(job_description, features='html.parser').get_text()
        job_title.strip()
        org_name.strip()
        
        ljob = LJob(job_title, org_name, job_description)
        l_ljobs.append(ljob)
        
        console.log(job_title)
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        embed = DiscordEmbed(title=job_title, description=job_description[0:256], color='03b2f8')
        console.log(f'')
        embed.add_embed_field(name='Company name', value=org_name, inline=False)
        embed.add_embed_field(name='Apply', value=link, inline=False)
        webhook.add_embed(embed)
        response = webhook.execute()
        console.log(response.status_code)

        driver.close()
    except Exception as e:
        print(e)