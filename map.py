import percentage_rank_functions as prf
import plotly.graph_objects as go
import US_state_abv
import pandas as pd

# prepare df for mapping
# case dict for mapping
def get_case_map_df(date):
    case_map_dict = {}
    for s in prf.total_pop_dict.keys():
        case_map_dict.update({s: prf.covid_pct(s, date, 'cases')})
    case_map_dict_abv = {US_state_abv.state_abv[state]: value for state, value in case_map_dict.items()}
    df = pd.DataFrame(case_map_dict_abv.items(), columns=['State', 'Case Percentage'])
    return df
# print(case_map_data('2022-01-23'))

def get_death_map_df(date):
    death_map_dict = {}
    for s in prf.total_pop_dict.keys():
        death_map_dict.update({s: prf.covid_pct(s, date, 'deaths')})
    death_map_dict_abv = {US_state_abv.state_abv[state]: value for state, value in death_map_dict.items()}
    df = pd.DataFrame(death_map_dict_abv.items(), columns=['State', 'Death Percentage'])
    return df
# print(death_map_data('2022-01-23'))

def get_vax_map_df(date):
    vax_map_dict = {}
    for s in prf.vaccinations_dict.keys():
        vax_map_dict.update({s: prf.vax_pct(s, date, 'people fully vaccinated')})
    vax_map_dict_abv = {US_state_abv.state_abv[state]: value for state, value in vax_map_dict.items()}
    df = pd.DataFrame(vax_map_dict_abv.items(), columns=['State', 'Fully Vaccinated Percentage'])
    return df


# Sample data as dictionary
# data = death_map_data('2022-01-23')
# #{'AL': 22.61, 'AK': 26.46, 'AZ': 23.81, 'AR': 24.25, 'CA': 19.7, 'CO': 20.32, 'CT': 18.52, 'DE': 23.58, 'DC': 18.93, 'FL': 23.84, 'GA': 19.9, 'HI': 13.72, 'ID': 18.47, 'IL': 22.07, 'IN': 22.37, 'IA': 21.32, 'KS': 23.21, 'KY': 23.75, 'LA': 23.09, 'ME': 12.05, 'MD': 15.18, 'MA': 22.0, 'MI': 21.11, 'MN': 21.28, 'MS': 23.18, 'MO': 20.74, 'MT': 19.83, 'NE': 20.99, 'NV': 19.34, 'NH': 18.48, 'NJ': 22.33, 'NM': 20.72, 'NY': 23.82, 'NC': 20.6, 'ND': 27.09, 'OH': 21.32, 'OK': 22.24, 'OR': 13.46, 'PA': 19.83, 'PR': 14.76, 'RI': 29.91, 'SC': 23.96, 'SD': 23.81, 'TN': 24.03, 'TX': 19.76, 'UT': 24.44, 'VT': 15.32, 'VA': 16.72, 'WA': 14.87, 'WV': 23.6, 'WI': 24.54, 'WY': 23.28}
# # Convert dictionary to Pandas dataframe
# df = pd.DataFrame(data.items(), columns=['State', 'Percentage'])
# print(df)


def draw_map(df, feature):
    '''
    df (dict): use get_case_map_df() or get_case_map_df()
    feature (str): 'Case Percentage' or 'Death Percentage'
    '''
    fig = go.Figure(data=go.Choropleth(
        locations=df['State'],
        z=df[feature].astype(float),
        locationmode='USA-states',
        colorscale="Reds",
        colorbar_title=f"{feature}",
        text=f"{feature}:" +
        df[feature].astype(float).apply('{:,}'.format)
    ))

    fig.update_layout(
        geo_scope='usa',
        title={'text': f"{feature} in the United States", 'x': 0.5,
               'xanchor': 'center', 'font': {'size': 16}}
    )

    fig.show()

# draw_map(get_case_map_df('2022-01-23'), 'Case Percentage')
# draw_map(get_vax_map_df('2022-01-23'), 'Fully Vaccinated Percentage')


# fig = go.Figure(data=go.Choropleth(
#     locations=df['State'],
#     z=df['Percentage'].astype(float),
#     locationmode='USA-states',
#     colorscale="Blues",
#     colorbar_title=f"{'Percentage'}",
#     text=f"{'Percentage'}:" +
#     df['Percentage'].astype(float).apply('{:,}'.format)
#     ))

# fig.update_layout(
#     geo_scope='usa',
#     title={'text': f"{'Percentage'} in the United States", 'x': 0.5,
#             'xanchor': 'center', 'font': {'size': 16}}
#     )

# fig.show()
