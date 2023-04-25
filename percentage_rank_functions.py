import US_state_abv
import pandas as pd
import json



covid_case_death = pd.read_csv('us-states.csv')
grouped = covid_case_death.groupby('state')

covid_dict = {}
for state, data in grouped:
    covid_dict[state] = {}
    for index, row in data.iterrows():
        date = row['date']
        cases = row['cases']
        deaths = row['deaths']
        covid_dict[state][date] = {'cases': cases, 'deaths': deaths}
# print(covid_dict['Alabama'])
# covid_dict = {'Alabama': {'2020-03-13': {'cases': 6, 'deaths': 0},}}

# for k, v in covid_dict.items():
#     print(v.keys())
# print(covid_dict)



total_pop = pd.read_csv('US_pop.csv')
grouped = total_pop.groupby('NAME')

total_pop_dict = {}
for state, data in grouped:
    if state in US_state_abv.states.values():
        total_pop_dict[state] = {}
        for index, row in data.iterrows():
            pop_2020 = row['POPESTIMATE2020']
            pop_2021 = row['POPESTIMATE2021']
            pop_2022 = row['POPESTIMATE2022']
            total_pop_dict[state] = {'2020': pop_2020, '2021': pop_2021, '2022': pop_2022}
# total_pop_dict = {'Alabama': {'2020': 5031362, '2021': 5049846, '2022': 5074296}, 'Alaska': {'2020': 732923, '2021': 734182, '2022': 733583}}


vaccinations = pd.read_csv('us_state_vaccinations.csv')
grouped = vaccinations.groupby('location')

vaccinations_dict = {}
for state, data in grouped:
    if state in US_state_abv.states.values():
        vaccinations_dict[state] = {}
        for index, row in data.iterrows():
            date = row['date']
            total_vax = row['total_vaccinations']
            ppl_vax =  row['people_vaccinated']
            ppl_full_vax = row['people_fully_vaccinated']
            ppl_full_vax_100 = row['people_fully_vaccinated_per_hundred']
            vaccinations_dict[state][date] = {'total_vax': total_vax,
                                              'ppl_vax': ppl_vax,
                                              'ppl_full_vax': ppl_full_vax,
                                              'ppl_full_vax_100': ppl_full_vax_100}

# print(vaccinations_dict['Alabama']['2023-04-05'])
# print(vaccinations_dict)
# vaccinations_dict = {'Alabama': {'2023-03-22': {'total_vax': 851096.0, 'ppl_vax': 353073.0, 'ppl_full_vax': 307218.0, 'ppl_full_vax_100': 30.7}}}

healthIT_adoption_dict = {}
with open('healthIT_adoption.json', 'r') as f:
    data = json.load(f)
for d in data:
    state = list(d.keys())[0]
    if state in US_state_abv.states.values():
        state_value = list(d.values())[0]
        period = state_value['period']
        ehr_pct = state_value['pct_phys_any_ehr']
        if state not in healthIT_adoption_dict:
            healthIT_adoption_dict[state] = {}
            healthIT_adoption_dict[state][period] = ehr_pct
        elif state in healthIT_adoption_dict:
            healthIT_adoption_dict[state].update({period: ehr_pct})
# print(healthIT_adoption_dict['Montana']['2017'])



def covid_pct(state, date, type):
    '''
    calculate case or death percentage by state and date

    Arg:
    state (str): state full name (e.g., Alabama)
    date (str): yyyy-mm-dd (e.g., 2020-01-23)
    type (str): case (case, cases, positive) or death (death, deaths, mortality)

    Return:
    percentage (float or str): return case/death percentage (rounded to two decimal places) or "No available data"
    '''
    if state in US_state_abv.states.values():
        if type in ['case', 'cases', 'positive']:
            case_pct = round(((covid_dict[state][date]['cases'] / total_pop_dict[state][date[0:4]]) *100), 2)
            return case_pct
        elif type in ['death', 'deaths', 'mortality']:
            death_pct = round(((covid_dict[state][date]['deaths'] / total_pop_dict[state][date[0:4]]) *100), 2)
            return death_pct
    else:
        return "No available data"

# print(type(covid_pct('Washington', '2022-01-23', 'case')))

def vax_pct(state, date, type):
    '''
    calculate percentages for vaccination data by date (people vax or people fully vaccinated)

    Arg:
    state (str): state full name (e.g., Alabama)
    date (str): yyyy-mm-dd (e.g., 2020-01-23)
    type (str): people vax or people fully vaccinated

    Return:
    percentage (float or str): return the requested percentage (rounded to two decimal places) or "No available data"
    '''
    if state in US_state_abv.states.values():
        # if type == "total vaccinations":
        #     total_vax_pct = round(((vaccinations_dict[state][date]['total_vax'] / total_pop_dict[state][date[0:4]]) *100), 2)
        #     return total_vax_pct
        if type == "people vaccinated":
            ppl_vax_pct = round(((vaccinations_dict[state][date]['ppl_vax'] / total_pop_dict[state][date[0:4]]) *100), 2)
            return ppl_vax_pct
        elif type == "people fully vaccinated":
            ppl_full_vax = float(vaccinations_dict[state][date]['ppl_full_vax_100'])
            return ppl_full_vax
    else:
        return "No available data"
# print(type(vax_pct('Washington', '2022-01-23', 'people fully vaccinated')))
# print(vaccinations_dict['Michigan'])



def get_ehr_pct(state, year):
    '''
    search the percentage of physicians adopted any EHR system in the state by year, rounded to two decimal places

    Arg:
    state (str)
    year (str): yyyy

    Return:
    percentage (float)
    '''
    pct = healthIT_adoption_dict[state][year]['any_ehr_pct']
    if pct != '':
        return round(float(pct), 2)
    else:
        return 0
# print(get_ehr_pct('Michigan', '2019'))
# print(healthIT_adoption_dict)

def case_rank(state, date):
    case_rank_list = []
    for s in total_pop_dict.keys():
        pct = covid_pct(s, date, 'cases')
        case_rank_list.append({s: pct})
    sorted_case_rank_list = sorted(case_rank_list, key=lambda x: list(x.values())[0])
    rank = sorted_case_rank_list.index({state: covid_pct(state, date, 'cases')}) +1
    return rank # number
# print(case_rank('Michigan', '2022-01-23'))

# print(covid_dict['American Samoa'])

def death_rank(state, date):
    death_rank_list = []
    for s in total_pop_dict.keys():
        pct = covid_pct(s, date, 'deaths')
        death_rank_list.append({s: pct})
    sorted_death_rank_list = sorted(death_rank_list, key=lambda x: list(x.values())[0])
    rank = sorted_death_rank_list.index({state: covid_pct(state, date, 'deaths')}) +1
    return rank # number
# print(death_rank('Michigan', '2022-01-24'))



def vax_rank(state, date): # only for people fully vaccinated
    vax_rank_list = []
    for s in vaccinations_dict.keys():
        pct = vax_pct(s, date, 'people fully vaccinated')
        vax_rank_list.append({s: pct})
    sorted_vax_rank_list = sorted(vax_rank_list, key=lambda x: list(x.values()), reverse=True)
    low = 0
    high = len(sorted_vax_rank_list) - 1
    target_pct = vax_pct(state, date, 'people fully vaccinated')
    while low <= high:
        mid = (low + high) // 2
        if list(sorted_vax_rank_list[mid].values())[0] >= target_pct:
            high = mid - 1
        else:
            low = mid + 1
    rank = sorted_vax_rank_list.index({state: target_pct}) + 1
    return rank
# print(vax_rank('Washington', '2022-01-23'))

def ehr_rank(state, year):
    ehr_rank_list = []
    for s in healthIT_adoption_dict.keys():
        try:
            pct = get_ehr_pct(s, year)
            ehr_rank_list.append({s: pct})
        except:
            continue
    sorted_ehr_rank_list = sorted(ehr_rank_list, key=lambda x: list(x.values()), reverse=True)
    rank = sorted_ehr_rank_list.index({state: get_ehr_pct(state, year)}) +1
    return rank
# print(ehr_rank('Michigan', '2019')) # 3 (reverse=True, smaller num better ehr adoption)


def get_state_name(state):
    if state.upper() in US_state_abv.states:
        return US_state_abv.states[state.upper()]
    elif state.title() in US_state_abv.states.values():
        return state.title()
    else:
        return None