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
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    try:
        # Effectuer la requête GET pour récupérer les données des commits
        response = requests.get(url)
        
        # Log pour vérifier l'URL et la réponse
        app.logger.info(f"Réponse de l'API GitHub: {response.status_code}")
        
        # Vérifier le code de réponse de l'API
        if response.status_code != 200:
            app.logger.error(f"Erreur lors de l'appel API : {response.status_code}, {response.text}")
            return jsonify({"error": f"Erreur API GitHub: {response.status_code}"}), 500

        commits_data = response.json()

        # Vérifier si la structure des données est correcte
        if not isinstance(commits_data, list) or len(commits_data) == 0:
            app.logger.error(f"Aucun commit trouvé dans la réponse de l'API : {commits_data}")
            return jsonify({"error": "Aucun commit trouvé dans la réponse de l'API"}), 500

        minutes = []
        commit_counts = []

        # Compter les commits par minute
        for commit in commits_data:
            try:
                commit_date_str = commit['commit']['author']['date']
                commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')

                minute = commit_date.minute

                if minute not in minutes:
                    minutes.append(minute)
                    commit_counts.append(1)
                else:
                    index = minutes.index(minute)
                    commit_counts[index] += 1
            except KeyError as e:
                app.logger.error(f"Clé manquante dans les données du commit: {str(e)}")
                return jsonify({"error": f"Clé manquante dans les données du commit: {str(e)}"}), 500

        # Retourner les données des commits sous forme de JSON
        return jsonify({"minutes": minutes, "commit_counts": commit_counts})

    except requests.exceptions.RequestException as e:
        # Si une erreur se produit lors de la requête HTTP
        app.logger.error(f"Erreur lors de la requête HTTP vers l'API GitHub: {str(e)}")
        return jsonify({"error": f"Erreur lors de la requête HTTP vers l'API GitHub: {str(e)}"}), 500

if __name__ == "__main__":
  app.run(debug=True)
