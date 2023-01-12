from bs4 import BeautifulSoup
from unidecode import unidecode
import requests
import re
import csv

url = "https://www.careerlink.vn/vieclam/list?page="

#function to find and return last page number
#get the last page number from pagination
def get_last_page():
    html = requests.get(url + str(1)).text
    soup = BeautifulSoup(html, 'html5lib')
    lis = soup("li","page-item")
    count = lis[4].find("a", "page-link").text
    return int(count)

#function to convert from USD to VND
def USD2VNDconvertor(amount):
    amount = int(amount)
    url_convert = 'https://api.exchangerate.host/convert?from=USD&to=VND&amount='+str(amount)+'&places=1'
    response = requests.get(url_convert)
    data = response.json()
    return data['result']

#function to extract number from salary string
def extract1(content):
    content = re.sub(r"\D", "", content)
    content = int(content)
    return content

#function to extract 2 numbers from salary string, and return its average value
def extract2(content):
    array = content.split("-")
    array[0] = extract1(array[0])
    array[1] = extract1(array[1])
    return (array[0] + array[1])/2

#create dataset, which will be stored in a csv file named 'dataset2'
with open('dataset2.csv', 'w') as csvfile:
    fieldnames = ['name', 'company', 'location', 'average_salary']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    #scrape data on all pages
    for x in range(1, get_last_page()):
        html = requests.get(url  + str(x)).text
        soup = BeautifulSoup(html, 'html5lib')
        divs = soup("div","media-body overflow-hidden")
        #scrape work information
        def work_info(div):
            #job name
            if div.find("h5", "job-name text-line-clamp-2 mb-1"):
                name = div.find("h5", "job-name text-line-clamp-2 mb-1").text.strip()
            #else if here because job labeled with "hot" has different div
            elif div.find("h5", "job-name text-line-clamp-2 mb-1 font-weight-bolder red"):
                name = div.find("h5", "job-name text-line-clamp-2 mb-1 font-weight-bolder red").text.strip()
            else:  
                name = ""
            #company name
            if div.find("a", "text-dark job-company mb-1 d-inline-block line-clamp-1"):
                company = div.find("a", "text-dark job-company mb-1 d-inline-block line-clamp-1").text.strip()
            else:
                company = "" 
            #salary range
            if div.find("span", "job-salary text-primary d-flex align-items-center"):
                salary = div.find("span", "job-salary text-primary d-flex align-items-center").text.strip()
            else:
                salary = ""
            #work location
            if div.find("a", "text-reset"):
                location = div.find("a", "text-reset").text.strip()
            else:
                location = "" 
            #handle salary field
            #check if salary range contains which type of salary (1 value or 2 values)
            if salary.count("VND") == 1:
                average_salary = extract1(salary)/1e6
            elif salary.count("USD") == 1:
                average_salary = round(USD2VNDconvertor(extract1(salary))/1e6, 1)
            elif "-" in salary:
                if "VND" in salary:
                    average_salary = extract2(salary)/1e6
                elif "USD" in salary:
                    average_salary = round(USD2VNDconvertor(extract2(salary))/1e6, 1)
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