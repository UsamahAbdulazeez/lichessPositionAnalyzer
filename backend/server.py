import os
from flask import Flask, request, jsonify
import openai
import chess
import chess.engine
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

STOCKFISH_PATH = os.getenv('STOCKFISH_PATH')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

@app.route('/stockfish', methods=['POST'])
def stockfish_analysis():
    data = request.get_json()
    fen = data.get('fen')

    board = chess.Board(fen)
    result = engine.analyse(board, chess.engine.Limit(time=0.1))
    best_move = result['pv'][0]

    return jsonify({'best_move': best_move.uci(), 'fen': fen})

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
