import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

openai.api_key = OPENAI_API_KEY

@app.route('/explanation', methods=['POST'])
def explanation():
    data = request.get_json()
    fen = data.get('fen')
    analysis = data.get('analysis')

    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Analyze this FEN position: {fen} and provide a detailed explanation for the following analysis: {analysis}",
        max_tokens=150
    )
    
    explanation = response.choices[0].text.strip()
    return jsonify({'explanation': explanation})

if __name__ == '__main__':
    app.run(debug=True)
