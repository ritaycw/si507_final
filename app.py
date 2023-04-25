import percentage_rank_functions as prf
import map
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index', methods=['POST'])
def index():
    data_form = request.form['data_form']
    if data_form == 'map':
        return render_template('map_type.html')
    elif data_form == 'rank':  # rank
        return render_template('rank_date_state.html')
    else:
        return render_template('ehr_adoption.html')

@app.route('/handle_form', methods=['POST'])
def handle_form():
    data_type = request.form['data_type']
    if data_type == 'vaccination':
        return render_template('vax_date.html')
    elif data_type == 'positive_case':
        return render_template('case_date.html')
    else:
        return render_template('death_date.html')

@app.route('/case_date', methods=['POST'])
def case_date():
    input_date = request.form['date']
    map.draw_map(map.get_case_map_df(input_date), 'Case Percentage')
    return render_template('home.html')

@app.route('/death_date', methods=['POST'])
def death_date():
    input_date = request.form['date']
    map.draw_map(map.get_death_map_df(input_date), 'Death Percentage')
    return render_template('home.html')

@app.route('/vax_date', methods=['POST'])
def vax_date():
    input_date = request.form['date']
    map.draw_map(map.get_vax_map_df(input_date), 'Fully Vaccinated Percentage')
    return render_template('home.html')

@app.route('/rank_date_state', methods=['POST'])
def rank_date_state():
    input_state = request.form['state']
    state_name = prf.get_state_name(input_state)
    input_date = request.form['date']
    try:
        case_rank = prf.case_rank(state_name, input_date)
    except:
        case_rank = "No available data for this date"
    try:
        death_rank = prf.death_rank(state_name, input_date)
    except:
        death_rank = "No available data for this date"
    try:
        full_vax_rank = prf.vax_rank(state_name, input_date)
    except:
        full_vax_rank = "No available data for this date"
    try:
        ehr_rank = prf.ehr_rank(state_name, input_date[0:4])
    except:
        ehr_rank = "No available data for this year"
    return render_template('show_rank.html', state=state_name, date=input_date, show_case_rank=case_rank, show_death_rank=death_rank, show_full_vax_rank= full_vax_rank, show_ehr_rank=ehr_rank)

@app.route('/ehr_adoption', methods=['POST'])
def ehr_adoption():
    input_state = request.form['state']
    state_name = prf.get_state_name(input_state)
    show_ehr_dict = prf.healthIT_adoption_dict[state_name]
    results = {}
    for k, v in show_ehr_dict.items():
        if v == '':
            results[k] = "No available data"
        else:
            results[k] = v
    return render_template('show_ehr_adoption.html', show_ehr_dict=results)

@app.route('/back_home')
def back_home():
    return redirect(url_for('home'))

@app.route('/final')
def final():
    return render_template('final.html')







if __name__ == "__main__":
    app.run(debug=True)