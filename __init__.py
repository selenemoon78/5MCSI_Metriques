from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
from collections import defaultdict
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')#
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

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

@app.route("/commits/")
def mescommits():
    return render_template("commits.html")
  

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

@app.route('/commits/')
def show_commits_graph():
    # Appel API GitHub pour obtenir les commits du repo
    commits_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(commits_url)
    commits = response.json()

    # Dictionnaire pour compter les commits par minute
    commits_by_minute = defaultdict(int)

    # Extraction des minutes des commits
    for commit in commits:
        date_string = commit['commit']['author']['date']  # Format: "2024-02-11T11:57:27Z"
        minute = extract_commit_minute(date_string)
        commits_by_minute[minute] += 1

    # Préparer les données pour le graphique
    minutes = sorted(commits_by_minute.keys())
    commit_counts = [commits_by_minute[minute] for minute in minutes]

    # Créer le graphique en utilisant Google Charts
    return render_template('commits_graph.html', minutes=minutes, commit_counts=commit_counts)

# Fonction pour extraire la minute d'un commit
def extract_commit_minute(date_string):
    # Nous utilisons le code de la route extract-minutes
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date_object.minute


if __name__ == "__main__":
  app.run(debug=True)
