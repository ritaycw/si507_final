# ritaycw_final_project
SI 507 Final Project, Winter 2023, University of Michigan

## Package
Installed the requirement packages by pip3
- pandas
- plotly
- Flask

## General info
The objective of this project is to enable users to visualize the distribution of COVID-19 cases, deaths, and fully vaccinated individuals in the United States on any date between 2020-2023. In addition, users can input a particular state and date to check the rankings of COVID-19 cases, deaths, fully vaccinated individuals, and EHR adoption rates compared to other states. Moreover, there is a section that focuses on physicians' Electronic Health Record (EHR) use rates in recent years, which enables users to observe the trend of EHR adoption and its potential impact on COVID-19 and vaccination rates.


### Data Sources
1. COVID-19 status quo (case and death) in all states by date.
(https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv)
2. COVID-19 vaccination data in all states by date.
(https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv)
3. Office-based Physician Health IT Adoption and Use data by year.
(https://www.healthit.gov/data/datasets/office-based-physician-health-it-adoption-and-use)
4. US total population by year (2020-2022).
(https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html)


### Data Structure
1. Cache the data in three dictionaries and connect the dictionaries with the key “state”
2. Map: use dataframe to sort the data and get the information.
3. Rank: use Binary Search to find the vaccination rank information.


### Interaction / Presentation
- Built the home page
  - Users can choose to return to the home page or end search after the results are presented.
- Prevent user error: use the dictionary of the full and abbreviated name of states in the US
  - It allows users to get the results no matter they enter a state's full name or abbreviation, upper or lower cases
- Plot the US choropleth map with the user input information (COVID case, death, fully vaccination rates by a chosen date).
- Display four different ranks for the state the user chooses.
- Display the EHR adoption rates over the years in a table by the user input state.

### Demo link
https://drive.google.com/file/d/1bqayGqkotNy1aalQky4R3vtVN0QrzTWm/view?usp=sharing

