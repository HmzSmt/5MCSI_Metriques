from flask import Flask, render_template, jsonify
from urllib.request import urlopen
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    url = 'https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx'

    response = urlopen(url)
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')  
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  
        results.append({'Jour': dt_value, 'temp': temp_day_value})

    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/commits/")
def commits():
    # URL de l'API GitHub
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = urlopen(url)
    raw_content = response.read()
    commits_data = json.loads(raw_content.decode('utf-8'))

    commits_per_minute = {}
    for commit in commits_data:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute

        if minute not in commits_per_minute:
            commits_per_minute[minute] = 0
        commits_per_minute[minute] += 1

    results = [{'minute': minute, 'commits': count} for minute, count in commits_per_minute.items()]
    return jsonify(results=results)

@app.route("/commit/")
def commits_chart():
    return render_template("commit.html")

if __name__ == "__main__":
    app.run(debug=True)
