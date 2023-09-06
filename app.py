from flask import Flask, request, render_template
from recipe_scrapers import scrape_me
import urllib.request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        urls = request.form.get('url') or ''
        urls = urls.split(',')
        results = []
        for url in urls:
            try:
                url = url.strip()
                scraper = scrape_me(url)
                if scraper.title() and scraper.ingredients():
                    recipe_title = scraper.title()
                    ingredients = scraper.ingredients()
                    results.append({'title': recipe_title, 'ingredients': ingredients})
            except Exception as e:
                return render_template('error.html', error=str(e))
        if results:
            return render_template('results.html', results=results)
        else:
            return render_template('error.html', error="No valid results")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
