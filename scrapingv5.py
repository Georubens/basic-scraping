from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

def google_search(query):
    query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve search results. Error: {e}"

def parse_results(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for g in soup.find_all('div', class_='yuRUbf'):
        link = g.find('a')['href']
        results.append(link)
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target_name = request.form['target_name']
        query = f'intext:"{target_name}"'
        html = google_search(query)
        if html:
            results = parse_results(html)
            return render_template('index.html', results=results, target_name=target_name)
        else:
            error = "Gagal mendapatkan hasil pencarian"
            return render_template('index.html', error=error)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
