import pandas as pd
import requests
import os
import json
import csv


def get_csv(url, filename):
    if os.path.exists(filename):
    # If the file already exists, read from it
        with open(filename, 'r') as f:
            data = f.read()
    else:
    # If the file doesn't exist, download it and save it locally
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        data = response.content
    return data

# COVID-19 status
covid_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
get_csv(covid_url, 'us-states.csv')

# if os.path.exists(covid_filename):
#     # If the file already exists, read from it
#     with open(covid_filename, 'r') as f:
#         data = f.read()
# else:
#     # If the file doesn't exist, download it and save it locally
#     response = requests.get(covid_url)
#     with open(covid_filename, 'wb') as f:
#         f.write(response.content)
#     data = response.content

covid_csv = pd.read_csv('us-states.csv')
covid_csv = covid_csv.drop('fips', axis=1)
# print(covid_csv)


# covid_status = {}
# with open('us-states.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         covid_status[row['state']] = [row['date'], row['cases'], row['deaths']]

# print(covid_status)



# Vaccination status
vax_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv'
get_csv(vax_url, 'us_state_vaccinations.csv')
vax_csv = pd.read_csv('us_state_vaccinations.csv')
vax_csv = vax_csv.drop(['total_distributed', 'people_fully_vaccinated_per_hundred', 'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred', 'distributed_per_hundred', 'daily_vaccinations_raw', 'daily_vaccinations', 'daily_vaccinations_per_million', 'share_doses_used', 'total_boosters', 'total_boosters_per_hundred'], axis=1)
# print(vax_csv)

# vaccination = {}
# with open('us_state_vaccinations.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         value = [row['date'], row['total_vaccinations'], row['people_vaccinated'], row['people_fully_vaccinated']]
#         if row['location'] not in vaccination:
#             vaccination[row['location']] = [value]
#         else:
#             vaccination[row['location']].append(value)
# print(vaccination['Alabama'])
# print(len(vaccination))
#date, total_vaccinations, people_vaccinated, people_fully_vaccinated





# Physician health IT adoption and use
healthIT_url = 'https://www.healthit.gov/data/open-api?source=nehrs.csv' # json API?

resp = requests.get(healthIT_url)
resp_json = resp.json()
# print(len(resp_json))

healthIT_list = []
for data in resp_json[0:-1]:
    # print(data)
    healthIT_list.append({data['region']:
                          {'period': data['period'],
                           'pct_phys_any_ehr': data['pct_phys_any_ehr']}})
# print(healthIT_list)
json_string = json.dumps(healthIT_list)
with open('healthIT_adoption.json', 'w') as f:
    f.write(json_string)
f.close()