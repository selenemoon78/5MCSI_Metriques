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




@app.route("/commits/")
def mescommits():
    return render_template("commits.html")

# Route pour récupérer les commits via l'API GitHub
@app.route("/api/commits/")
def api_commits():
    # URL de l'API GitHub pour récupérer les commits
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    # Effectuer une requête GET pour récupérer les données des commits
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Erreur lors de la récupération des données depuis GitHub"}), 500

    # Extraire les données JSON de la réponse
    commits_data = response.json()
    
    # Extraire les minutes de chaque commit
    minutes = []
    commit_counts = []

    # Compter les commits par minute
    for commit in commits_data:
        # Récupérer la date du commit
        commit_date_str = commit['commit']['author']['date']
        commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')

        # Extraire la minute du commit
        minute = commit_date.minute

        if minute not in minutes:
            minutes.append(minute)
            commit_counts.append(1)
        else:
            # Si la minute existe déjà, on incrémente le nombre de commits
            index = minutes.index(minute)
            commit_counts[index] += 1

    # Retourner les données des commits sous forme de JSON
    return jsonify({"minutes": minutes, "commit_counts": commit_counts})
if __name__ == "__main__":
  app.run(debug=True)
