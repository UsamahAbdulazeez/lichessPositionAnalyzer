from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
import chess
import chess.engine

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
stockfish_path = "./stockfish-windows-x86-64/stockfish-windows-x86-64.exe"

def get_stockfish_analysis(fen):
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        board = chess.Board(fen)
        result = engine.analyse(board, chess.engine.Limit(time=2.0))
        best_move = result['pv'][0]
        analysis = engine.analyse(board, chess.engine.Limit(time=2.0))
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
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text

@app.route('/stockfish', methods=['POST'])
def stockfish():
    data = request.json
    fen = data['fen']
    best_move, analysis = get_stockfish_analysis(fen)
    return jsonify({"best_move": best_move, "analysis": analysis})

@app.route('/explanation', methods=['POST'])
def explanation():
    data = request.json
    fen = data['fen']
    stockfish_analysis = data['analysis']
    response = generate_explanation(fen, stockfish_analysis)
    return jsonify({"explanation": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
