from flask import Flask, request, jsonify, render_template
from recipe_scrapers import scrape_me

def safe_scrape(callable_func, default_value):
    try:
        return callable_func()
    except Exception as e:
        if "No ratings data in SchemaOrg." in str(e):
            return default_value
        raise e

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    url = request.form.get('url') if request.method == 'POST' else None

    if url:
        try:
            scraper = scrape_me(url, wild_mode=True)
            result = {
                'success': True,
                'title': safe_scrape(scraper.title, "N/A"),
                'host': safe_scrape(scraper.host, "N/A"),
                'total_time': safe_scrape(scraper.total_time, "N/A"),
                'image': safe_scrape(scraper.image, "N/A"),
                'ingredients': safe_scrape(scraper.ingredients, []),
                'instructions': safe_scrape(scraper.instructions, "N/A"),
                'instructions_list': safe_scrape(scraper.instructions_list, []),
                'yields': safe_scrape(scraper.yields, "N/A"),
                'nutrients': safe_scrape(scraper.nutrients, {}),
                'category': safe_scrape(scraper.category, "N/A"),
                'cuisine': safe_scrape(scraper.cuisine, "N/A"),
                'ratings': safe_scrape(scraper.ratings, {}),
                'description': safe_scrape(scraper.description, "N/A"),
                'author': safe_scrape(scraper.author, "N/A"),
            }
        except Exception as e:
            result = {'success': False, 'error_message': str(e)}
    else:
        result = {'success': False, 'error_message': 'Please provide a valid URL.'}

    if request.method == 'POST':
        return jsonify(result)
    else:
        return render_template('index.html')

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'success': False, 'error_message': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()
