import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set.")

openai.api_key = OPENAI_API_KEY

ANALYSIS_PROMPTS = {
    'checks_captures_threats': "Analyze the following chess position in FEN notation. Focus only on immediate checks, captures, and threats. Be very concise and to the point. FEN: ",
    'weak_strong_pieces': "Analyze the following chess position in FEN notation. Identify weak and strong pieces for both sides. Be very concise and to the point. FEN: ",
    'key_ideas_strategies': "Analyze the following chess position in FEN notation. Suggest key ideas and strategies for both sides. Be very concise and to the point. FEN: "
}

@app.route('/analysis', methods=['POST'])
def analysis():
    try:
        data = request.get_json()
        fen = data.get('fen')
        analysis_type = data.get('analysis')

        if not fen or not analysis_type:
            return jsonify({"error": "Missing FEN or analysis type"}), 400

        prompt = ANALYSIS_PROMPTS.get(analysis_type, "Analyze this chess position. Be concise. FEN: ") + fen

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chess analyst providing brief, focused analyses."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        explanation = response['choices'][0]['message']['content'].strip()
        return jsonify({'explanation': explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    return "", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))