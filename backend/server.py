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

def get_analysis_prompt(fen, analysis_type):
    if analysis_type == 'threats':
        return f"Analyze this FEN position: {fen} and provide details on checks, captures, and threats."
    elif analysis_type == 'pieces':
        return f"Analyze this FEN position: {fen} and provide details on weak and strong pieces."
    elif analysis_type == 'ideas':
        return f"Analyze this FEN position: {fen} and provide key ideas and strategies."
    elif analysis_type == 'overview':
        return f"Analyze this FEN position: {fen} and provide a general overview."
    else:
        return f"Analyze this FEN position: {fen}."

@app.route('/analysis', methods=['POST'])
def analysis():
    try:
        data = request.get_json()
        fen = data.get('fen')
        analysis_type = data.get('analysis')

        if not fen or not analysis_type:
            return jsonify({"error": "Missing FEN or analysis type"}), 400

        prompt = get_analysis_prompt(fen, analysis_type)

        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=prompt,
            max_tokens=150
        )
        
        explanation = response.choices[0].text.strip()
        return jsonify({'explanation': explanation})
    except Exception as e:
        app.logger.error(f"Error during analysis: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
