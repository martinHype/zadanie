import requests
from bs4 import BeautifulSoup
import json


class JobOffer():
    #creating the constructor
    def __init__(self,title):
        self.title = title
    #method to set email variable
    def setEmail(self,contact_email):
        self.contact_email = contact_email

    #method to separate information regarding their label
    def setVariables(self,full_text):
        label = full_text.find("strong").text
        text = full_text.text[len(label):]
        if "Miesto výkonu práce:" in label:
            self.place = text
        elif "Platové ohodnotenie" in label:
            self.salary = text
        else:
            self.contract_type = text
    
#set up base url of the website we want to webscrape
BASE_URL ="https://www.hyperia.sk/"
#accessing the endpoint kariera of the base url
page = requests.get(BASE_URL+"kariera/")

#declaring the new list for storing objects of the job offers
list_of_jobs = []


soup = BeautifulSoup(page.content,"html.parser")


results = soup.find(id = "positions")
job_elements = results.find_all("div",class_ = "offset-lg-1 col-md-10")

#list throught the all elements and finding required informations
for job in job_elements:
    
    #geting the title of the job
    job_title = job.find("h3").text

    #creating instance of the job offer object
    job_offer = JobOffer(job_title)

    #getting link for the more information about the job offer
    link_element = job.find('a',href = True)
    ACCESS_LINK = BASE_URL + link_element['href']

    #accessing the subpage
    subpage = requests.get(ACCESS_LINK)
    soup = BeautifulSoup(subpage.content,"html.parser")
    results = soup.find(id ="__layout")

    elements = results.find_all("div",class_ = "col-md-4 icon")
    #nesting throught the elements to get place, salary and contract_type
    for element in elements:

        #sending text to analyze which information regards to which required data
        job_offer.setVariables(element.find('p'))

    #accasing the email for contact_email
    contact_email = results.find("div",class_ = "container position-contact").find('p').find('strong').text
    job_offer.setEmail(contact_email)

    #adding filled up instance to the list
    list_of_jobs.append(job_offer.__dict__)

#creating or writing the data to he json file
with open("json_output.json","w",encoding="utf8") as file:
    json.dump(list_of_jobs,file,indent=5,ensure_ascii=False)
        
    