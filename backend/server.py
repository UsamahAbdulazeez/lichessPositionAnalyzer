import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

ANALYSIS_PROMPTS = {
    'checks_captures_threats': "Analyze the following chess position in FEN notation. Focus only on immediate checks, captures, and threats. Be very concise and to the point. FEN: ",
    'weak_strong_pieces': "Analyze the following chess position in FEN notation. Identify weak and strong pieces for both sides. Be very concise and to the point. FEN: ",
    'key_ideas_strategies': "Analyze the following chess position in FEN notation. Suggest key ideas and strategies for both sides. Be very concise and to the point. FEN: "
}

@app.route('/analysis', methods=['POST'])
def analyze_fen():
    data = request.json
    fen = data.get('fen')
    analysis_type = data.get('analysis')

    if not fen:
        return jsonify({'error': 'FEN not provided'}), 400
    if not analysis_type or analysis_type not in ANALYSIS_PROMPTS:
        return jsonify({'error': 'Invalid analysis type'}), 400

    prompt = ANALYSIS_PROMPTS[analysis_type] + fen
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chess analysis assistant. Provide brief, concise analyses focusing only on the requested aspect of the position."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.5
        )
        explanation = response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        return jsonify({'error': f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': f"Unexpected error: {str(e)}"}), 500

    return jsonify({'explanation': explanation})

if __name__ == '__main__':
    app.run(debug=True)