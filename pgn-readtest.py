from pgn_parser import parser, pgn
from stockfish import Stockfish
import chess
import chess.engine


def main():
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("/stockfish_10_x64")
    game = readFile(input("Enter file name: "))
    analyzeGame(game, board, engine)


# FUNCTION: Reads file and formats it into a game object
# RETURN: A game object 
def readFile(fileName): 
    try:
        with open(fileName, "r") as file:
            gametext = file.read()
        # print(gametext) # Debug gametext in string format
        game = parser.parse(gametext, actions=pgn.Actions())
        return game
    except IOError:
        print("File \"" + fileName + "\" could not be found")
        exit()

def analyzeGame(game, board, engine):
    m1 = game.move(1)
    board.push_san(m1.white.san)
    board.push_san("e5")
    # board.push_san("Ke2")
    print(board)
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    print("Score:", info["score"])
    engine.quit()

main()