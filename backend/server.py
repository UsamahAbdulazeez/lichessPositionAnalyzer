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
    'tactical': "Briefly analyze the chess position. Focus on the most critical: 1) Check or capture. 2) Immediate threat. Consider recent moves. Be very concise. FEN: {fen}. PGN: {pgn}",
    'positional': "Briefly analyze the chess position. Identify the most significant: 1) Strong or weak piece. 2) Pawn structure issue. Consider recent moves. Be very concise. FEN: {fen}. PGN: {pgn}",
    'material': "Briefly analyze the chess position. Note: 1) Material count. 2) Most important imbalance. Consider recent exchanges. Be very concise. FEN: {fen}. PGN: {pgn}",
    'strategic': "Briefly analyze the chess position. Suggest: 1) Key idea for each side. 2) One potential plan. Consider the game progression. Be very concise. FEN: {fen}. PGN: {pgn}",
    'dynamic': "Briefly analyze the chess position. Comment on: 1) Who has the initiative. 2) Most uncoordinated piece. Consider recent tempo gains/losses. Be very concise. FEN: {fen}. PGN: {pgn}",
    'summary': "Provide a brief summary of the chess position. Include: 1) Overall assessment. 2) Most critical move or plan. Consider the game context. Be very concise. FEN: {fen}. PGN: {pgn}"
}

@app.route('/')
def home():
    return "Chess Analysis Server is running!", 200

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/analysis', methods=['POST'])
def analysis():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Log received data
        fen = data.get('fen')
        pgn = data.get('pgn')
        analysis_type = data.get('analysis')

        if not fen:
            return jsonify({"error": "Missing FEN"}), 400
        if not pgn:
            return jsonify({"error": "Missing PGN"}), 400
        if not analysis_type:
            return jsonify({"error": "Missing analysis type"}), 400

        if analysis_type not in ANALYSIS_PROMPTS:
            return jsonify({"error": f"Invalid analysis type: {analysis_type}"}), 400

        prompt = ANALYSIS_PROMPTS[analysis_type].format(fen=fen, pgn=pgn)
        print(f"Generated prompt: {prompt}")  # Log the generated prompt

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chess analyst providing extremely brief, focused analyses. Use at most two short sentences per point. Refer to specific moves from the PGN only if critically relevant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        explanation = response['choices'][0]['message']['content'].strip()
        return jsonify({'explanation': explanation})
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {str(e)}")  # Log OpenAI errors
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Log unexpected errors
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)