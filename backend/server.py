import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

@app.route('/analysis', methods=['POST'])
def analyze_fen():
    data = request.json
    fen = data.get('fen')
    analysis_type = data.get('analysis')

    if not fen:
        return jsonify({'error': 'FEN not provided'}), 400
    if not analysis_type:
        return jsonify({'error': 'Analysis type not provided'}), 400

    prompt = f"Analyze the following FEN ({analysis_type}): {fen}"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.5
        )
        explanation = response.choices[0].text.strip()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'explanation': explanation})

if __name__ == '__main__':
    app.run(debug=True)
