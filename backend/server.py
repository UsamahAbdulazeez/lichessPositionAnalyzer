from flask import Flask, request, jsonify
from transformers import pipeline
import chess
import chess.engine

app = Flask(__name__)
generator = pipeline('text-generation', model='gpt-2')

# Path to Stockfish executable
stockfish_path = "./stockfish-windows-x86-64/stockfish-windows-x86-64.exe"

def get_stockfish_analysis(fen):
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        board = chess.Board(fen)
        result = engine.analyse(board, chess.engine.Limit(time=2.0))
        best_move = result['pv'][0]
        analysis = engine.analyse(board, chess.engine.Limit(depth=20))
        return str(best_move), analysis

@app.route('/stockfish', methods=['POST'])
def stockfish():
    data = request.json
    fen = data['fen']
    best_move, analysis = get_stockfish_analysis(fen)
    return jsonify({'best_move': best_move, 'analysis': str(analysis)})

@app.route('/explanation', methods=['POST'])
def explanation():
    data = request.json
    fen = data['fen']
    stockfish_analysis = data['analysis']
    prompt = f"Given the chess position FEN {fen} and the analysis {stockfish_analysis}, provide a detailed explanation of the position."
    explanation = generator(prompt, max_length=150)[0]['generated_text']
    return jsonify({'explanation': explanation})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
