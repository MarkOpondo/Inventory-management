import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/product/<barcode>')
def get_food_facts(barcode):
    API_URL = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept" : "application/json",
        "From" : "mark.opondo@moringaschool.com"
    }

    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        # openfoodfacts returns 1 as the status if the product is found
        if data.get("status") == 1:
            product_info = data.get("product", {})

            filtered_data = {
                "success" : True,
                "barcode" : barcode,
                "name" : product_info.get("product_name", "Unknown Product"),
                "brands" : product_info.get("brands", "Unknown Brand"),
                # "image": product_info.get("image_front_url", ""),
                "nutriscore" : product_info.get("nutriscore_grade", "N/A").upper(),
                "ingredients" : product_info.get("ingredients_text", "No ingredients listed")
            }
            return jsonify(filtered_data), 200

        else:
            return jsonify({
                "success": False,
                "error": "Product not found in Open Food Facts database"
            }), 404
        
    except requests.exceptions.HTTPError as http_err:
        return jsonify({
            "success" : False,
            "error" : "External API error",
            "status_code": response.status_code
        }), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "success" : False, 
            "error": "Failed to fetch data", 
            "details" : str(e)
        }), 502
    
if __name__ == "__main__":
    app.run(debug=True)