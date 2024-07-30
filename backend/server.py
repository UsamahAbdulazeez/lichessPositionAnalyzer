import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    app.logger.error("OPENAI_API_KEY environment variable is not set.")
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

openai.api_key = OPENAI_API_KEY

def get_analysis_prompt(fen, analysis_type):
    base_prompt = f"Analyze this FEN position: {fen} briefly and concisely. "
    if analysis_type == 'threats':
        return base_prompt + "Provide details on checks, captures, and threats."
    elif analysis_type == 'pieces':
        return base_prompt + "Provide details on weak and strong pieces."
    elif analysis_type == 'ideas':
        return base_prompt + "Provide key ideas and strategies."
    elif analysis_type == 'overview':
        return base_prompt + "Provide a general overview."
    else:
        return base_prompt

@app.route('/analysis', methods=['POST'])
def analysis():
    try:
        data = request.get_json()
        app.logger.info(f"Received data: {data}")
        fen = data.get('fen')
        analysis_type = data.get('analysis')

        if not fen or not analysis_type:
            app.logger.error("Missing FEN or analysis type")
            return jsonify({"error": "Missing FEN or analysis type"}), 400

        prompt = get_analysis_prompt(fen, analysis_type)
        app.logger.info(f"Generated prompt: {prompt}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful chess assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        
        app.logger.info(f"OpenAI response: {response}")
        explanation = response['choices'][0]['message']['content'].strip()
        app.logger.info(f"Received explanation: {explanation}")
        return jsonify({'explanation': explanation})
    except Exception as e:
        app.logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/')
def health_check():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=10000)
