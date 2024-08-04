import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app, resources={r"/analysis": {"origins": "*"}})

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set.")

openai.api_key = OPENAI_API_KEY

STOCKFISH_API_URL = "https://stockfish.online/api/s/v2.php"
STOCKFISH_DEPTH = 15  # You can adjust the depth as needed

ANALYSIS_PROMPTS = {
    'tactical': "Briefly analyze the chess position. Focus on the most critical: 1) Check or capture. 2) Immediate threat. Consider recent moves. Be very concise. FEN: {fen}. PGN: {pgn}. Engine Analysis: {engine_analysis}",
    'positional': "Briefly analyze the chess position. Identify the most significant: 1) Strong or weak piece. 2) Pawn structure issue. Consider recent moves. Be very concise. FEN: {fen}. PGN: {pgn}. Engine Analysis: {engine_analysis}",
    'material': "Briefly analyze the chess position. Note: 1) Material count. 2) Most important imbalance. Consider recent exchanges. Be very concise. FEN: {fen}. PGN: {pgn}. Engine Analysis: {engine_analysis}",
    'strategic': "Briefly analyze the chess position. Suggest: 1) Key idea for each side. 2) One potential plan. Consider the game progression. Be very concise. FEN: {fen}. PGN: {pgn}. Engine Analysis: {engine_analysis}",
    'dynamic': "Briefly analyze the chess position. Comment on: 1) Who has the initiative. 2) Most uncoordinated piece. Consider recent tempo gains/losses. Be very concise. FEN: {fen}. PGN: {pgn}. Engine Analysis: {engine_analysis}",
    'summary': "Provide a brief summary of the chess position. Include: 1) Overall assessment. 2) Most critical move or plan. Consider the game context. Be very concise. FEN: {fen}. PGN: {pgn}. Engine Analysis: {engine_analysis}"
}

@app.route('/')
def home():
    return "Chess Analysis Server is running!", 200

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

def fetch_stockfish_analysis(fen):
    try:
        response = requests.get(STOCKFISH_API_URL, params={'fen': fen, 'depth': STOCKFISH_DEPTH})
        if response.status_code == 200 and response.json().get('success', False):
            data = response.json()
            eval_score = data.get('evaluation', 'N/A')
            best_move = data.get('bestmove', 'N/A')
            continuation = data.get('continuation', 'N/A')
            return f"Evaluation: {eval_score}, Best Move: {best_move}, Continuation: {continuation}"
        else:
            return "Engine analysis failed or returned incomplete data."
    except requests.exceptions.RequestException as e:
        return f"Stockfish API error: {str(e)}"

@app.route('/analysis', methods=['POST'])
def analysis():
    try:
        data = request.get_json()
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
            return jsonify({"error": f"Invalid analysis type: {analysis_type}. Valid types are: {', '.join(ANALYSIS_PROMPTS.keys())}"}), 400

        # Fetch Stockfish analysis
        engine_analysis = fetch_stockfish_analysis(fen)
        
        # Generate prompt for LLM
        prompt = ANALYSIS_PROMPTS[analysis_type].format(fen=fen, pgn=pgn, engine_analysis=engine_analysis)

        response = openai.ChatCompletion.create(
            model="gpt-4",  # Switching to GPT-4 for more advanced analysis
            messages=[
                {"role": "system", "content": "You are a chess analyst providing extremely brief, focused analyses. Use at most two short sentences per point. Refer to specific moves from the PGN only if critically relevant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        explanation = response['choices'][0]['message']['content'].strip()
        return jsonify({'explanation': explanation})
    except openai.error.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
