from flask import Flask, request, jsonify
import re
import base64
import requests

app = Flask(__name__)

@app.route('/boost.ink?url=', methods=['GET'])
def extract():
    # Get the URL from query parameters
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        # Fetch the webpage content
        response = requests.get(url)
        html_content = response.text

        # Regex pattern to match the Base64 value inside bufpsvdhmjybvgfncqfa attribute
        pattern = r'bufpsvdhmjybvgfncqfa="([^"]+)"'

        # Find all matches
        matches = re.findall(pattern, html_content)

        if matches:
            # Extract the first match
            base64_value = matches[0]

            # Decode the Base64 value
            decoded_value = base64.b64decode(base64_value).decode("utf-8")
            
            return jsonify({"decoded_value": decoded_value})
        else:
            return jsonify({"error": "No matches found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
