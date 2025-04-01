from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')#
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhisto():
    return render_template("histogramme.html")




YOUR_NAME = "selenemoon78"
YOUR_EMAIL = "asmaa.bahammou@edu.esiee-it.fr"

@app.route('/commits/')
def commits():
    url = "https://api.github.com/repos/selenemoon/5MCSI_Metriques/commits"
    
    with urlopen(url) as response:
        data = json.load(response)

    minute_counts = [0] * 60

    for commit in data:
        try:
            author = commit['commit']['author']
            author_name = author['name']
            author_email = author['email']
            date_str = author['date']

            if author_name == YOUR_NAME or author_email == YOUR_EMAIL:
                dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                minute = dt.minute
                minute_counts[minute] += 1
        except KeyError:
            continue

    minutes = list(range(60))

    return render_template("commits.html", minutes=minutes, counts=minute_counts)

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


if __name__ == "__main__":
  app.run(debug=True)
