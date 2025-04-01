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




@app.route('/commits/')
def commits():
    url = "https://api.github.com/repos/slngithh/5MCSI_Metriques/commits"
    
    # Récupération des données via urllib
    with urlopen(url) as response:
        data = json.load(response)

    # Initialisation du compteur des minutes
    minute_counts = [0] * 60

    # Traitement des commits
    for commit in data:
        try:
            author = commit['commit']['author']
            author_name = author['name']
            author_email = author['email']
            date_str = author['date']

            # Filtrage : on ne garde que les commits de l'utilisateur courant
            if author_name == YOUR_NAME or author_email == YOUR_EMAIL:
                dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                minute = dt.minute
                minute_counts[minute] += 1
        except:
            continue

    # Préparation des données pour le graphique
    minutes = list(range(60))

    # HTML avec Chart.js intégré
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Commits par minute</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h2>Commits par minute (vos commits uniquement)</h2>
        <canvas id="commitsChart" width="600" height="400"></canvas>
        <script>
            const minutes = {{ minutes | safe }};
            const counts = {{ counts | safe }};

            const ctx = document.getElementById('commitsChart').getContext('2d');
            const commitsChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: minutes,
                    datasets: [{
                        label: 'Commits par minute',
                        data: counts
                    }]
                },
                options: {
                    scales: {
                        x: {
                            title: { display: true, text: 'Minute (0-59)' }
                        },
                        y: {
                            beginAtZero: true,
                            title: { display: true, text: 'Nombre de commits' }
                        }
                    }
                }
            });
        </script>
    </body>
    </html>
    """

    return render_template_string(html_template, minutes=minutes, counts=minute_counts)

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


if __name__ == "__main__":
  app.run(debug=True)
