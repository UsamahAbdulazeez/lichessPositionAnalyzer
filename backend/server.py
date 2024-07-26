from flask import Flask, request, jsonify
from flask_cors import CORS
import chess.engine
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

stockfish_path = "./stockfish-windows-x86-64/stockfish-windows-x86-64.exe"

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_stockfish_analysis(fen):
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        board = chess.Board(fen)
        result = engine.analyse(board, chess.engine.Limit(time=2.0))
        best_move = result['pv'][0]
        analysis = result
    return str(best_move), analysis

def generate_explanation(fen, stockfish_analysis):
    prompt = f"The current position in FEN notation is: {fen}. The analysis is: {stockfish_analysis}. Provide detailed insights including:"
    prompt += "Immediate Threats, Captures, and Checks\n"
    prompt += "Threats:\n"
    prompt += "Captures:\n"
    prompt += "Checks:\n"
    prompt += "Key Ideas and Strategies\n"
    prompt += "Weaknesses and Strengths\n"
    prompt += "Strong and Weak Pieces\n"
    prompt += "Strategic Guidance\n"
    prompt += "Tactical Considerations\n"
    prompt += "Overview\n"

    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=1500
    )
    return response.choices[0].text.strip()

@app.route('/stockfish', methods=['POST'])
def stockfish():
    data = request.get_json()
    fen = data.get('fen')
    if not fen:
        return jsonify({"error": "FEN not provided"}), 400

    try:
        best_move, analysis = get_stockfish_analysis(fen)
        return jsonify({"best_move": best_move, "analysis": analysis}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/explanation', methods=['POST'])
def explanation():
    data = request.get_json()
    fen = data.get('fen')
    analysis = data.get('analysis')
    if not fen or not analysis:
        return jsonify({"error": "FEN or analysis not provided"}), 400

    try:
        explanation = generate_explanation(fen, analysis)
        return jsonify({"explanation": explanation}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
