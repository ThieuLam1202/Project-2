from bs4 import BeautifulSoup
from unidecode import unidecode
import numpy as np
import requests
import csv

url = "https://vieclam24h.vn/tim-kiem-viec-lam-nhanh?occupation_ids%5B%5D=7&occupation_ids%5B%5D=8&page="

#function to find and return last page number
#get the count of jobs then divide it with 30 (is number of jobs on a page)
def get_last_page():
    html = requests.get(url + str(1)).text
    soup = BeautifulSoup(html, 'html5lib')
    divs = soup("div","flex items-center")
    count = divs[0].find("span", "font-semibold").text
    return int(np.ceil(int(count)/30))

#create dataset, which will be stored in a csv file named 'dataset1'
with open('dataset1.csv', 'w') as csvfile:
    fieldnames = ['name', 'company', 'location', 'average_salary']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    #scrape data on all pages
    for x in range(1, get_last_page()):
        html = requests.get(url  + str(x)).text
        soup = BeautifulSoup(html, 'html5lib')
        divs = soup("div","relative lg:my-auto pl-2 lg:pl-2 leading-6 mb-4 flex-grow overflow-hidden mt-[14px]")
        #scrape work information
        def work_info(div):
            #job name
            if div.find("p", "text-se-neutral-100-n font-medium text-[18px] leading-6 tracking-tighter line-clamp-2 lg:line-clamp-none lg:truncate lg:block"):
                name = div.find("p", "text-se-neutral-100-n font-medium text-[18px] leading-6 tracking-tighter line-clamp-2 lg:line-clamp-none lg:truncate lg:block").text.strip()
            #else if here because job labeled with "hot" has different div
            elif div.find("p", "text-red-bright font-bold text-[18px] leading-6 tracking-tighter line-clamp-2 lg:line-clamp-none lg:truncate lg:block"):
                name = div.find("p", "text-red-bright font-bold text-[18px] leading-6 tracking-tighter line-clamp-2 lg:line-clamp-none lg:truncate lg:block").text.strip()
            else:  
                name = ""
            #company name
            if div.find("p", "block text-grey-48 text-[16px] leading-6 truncate pr-2 max-w-[240px] lg:max-w-full"):
                company = div.find("p", "block text-grey-48 text-[16px] leading-6 truncate pr-2 max-w-[240px] lg:max-w-full").text.strip()
            else:
                company = "" 
            #salary range
            if div.find("span", "text-se-neutral-80 text-14 whitespace-nowrap font-medium"):
                salary = div.find("span", "text-se-neutral-80 text-14 whitespace-nowrap font-medium").text.strip()
            else:
                salary = ""   
            #work location
            if div.find("span", "text-se-neutral-80 text-14 whitespace-nowrap truncate"):
                location = div.find("span", "text-se-neutral-80 text-14 whitespace-nowrap truncate").text.strip()
            else:
                location = "" 
            #if salary field is not null then convert to one average value only
            if (len(salary) > 0):
                array = salary.split()
                average_salary = (int(array[0]) + int(array[2]))/2
            else:
                average_salary = ""
            return {
                'name' : unidecode(name),
                'company' : unidecode(company),
                'location' : unidecode(location),
                'average_salary' : average_salary
        }

        for i in range(len(divs)):
            #print(work_info(divs[i]))
            writer.writerow(work_info(divs[i]))

#close file
csvfile.close()