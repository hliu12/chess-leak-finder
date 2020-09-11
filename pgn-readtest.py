"""
# Henry Liu
# September 2020
# pgn-readtest.py
#
# Reads in a pgn chess game file and outputs blunders
# along with the move they were made on
"""


from pgn_parser import parser, pgn
from stockfish import Stockfish
import chess
from chess.engine import Cp, Mate, MateGiven

BLUNDER_MARGIN = 75


def main():
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("/stockfish_10_x64")
    # game = readFile(input("Enter file name: "))
    game = readFile("testGame.pgn")
    analyzeGame(game, board, engine)



"""
# Name: readFile
# Purpose: Reads file and formats it into a game object
# Input: the file name
# Returns: game object
"""
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


"""
# Name: analyzeGame
# Purpose: Analyzes game against engine for blunders
# Input: game object, game board object, chess engine
# Returns: None
"""
def analyzeGame(game, board, engine):
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    evaluation = info["score"].white().score()
    # Checks first 20 moves for blunders
    for x in range(1, 20):
        # Evaluate position before the moves
        temp = evaluation
        # Make the move on the board and evaluate
        move = game.move(x)
        board.push_san(move.white.san)
        board.push_san(move.black.san)
        info = engine.analyse(board, chess.engine.Limit(time=0.1))
        evaluation = info["score"].white().score()
        # Prints score for debugging purposes
        # print("Score:", info["score"])
        # Check for blunder
        if evaluation + BLUNDER_MARGIN < temp :
            print("Blunder occured on move " + str(x))

    engine.quit()

main()