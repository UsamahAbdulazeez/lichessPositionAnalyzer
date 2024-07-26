import os
import chess.engine
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Path to Stockfish executable
stockfish_path = "./backend/stockfish-windows-x86-64/stockfish-windows-x86-64.exe"

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_stockfish_analysis(fen):
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        board = chess.Board(fen)
        result = engine.analyse(board, chess.engine.Limit(time=2.0))
        best_move = result['pv'][0]
        analysis = engine.analyse(board, chess.engine.Limit(depth=20))
        return str(best_move), analysis

def generate_explanation(fen, stockfish_analysis):
    prompt = f"Analyze the chess position given the following FEN: {fen} and the analysis: {stockfish_analysis}. Provide detailed analysis and suggestions."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

@app.route('/stockfish', methods=['POST'])
def stockfish():
    data = request.get_json()
    fen = data['fen']
    best_move, analysis = get_stockfish_analysis(fen)
    return jsonify({"best_move": best_move, "analysis": analysis})

@app.route('/explanation', methods=['POST'])
def explanation():
    data = request.get_json()
    fen = data['fen']
    stockfish_analysis = data['analysis']
    explanation = generate_explanation(fen, stockfish_analysis)
    return jsonify({"explanation": explanation})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
