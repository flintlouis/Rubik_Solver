# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    defines.py                                         :+:    :+:             #
#                                                      +:+                     #
#    By: flintlouis <flintlouis@student.codam.nl      +#+                      #
#                                                    +#+                       #
#    Created: 2021/04/01 16:31:25 by flintlouis    #+#    #+#                  #
#    Updated: 2021/04/08 21:55:31 by flintlouis    ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

COLOURS = { 0:"red", 1:"green", 2:"orange", 3:"blue", 4:"white", 5:"yellow" }
FRONT, RIGHT, BACK, LEFT, BOTTOM, TOP = 0, 1, 2, 3, 4, 5
VALID_MOVES = ["F", "F'", "F2", "R", "R'", "R2",
			   "B", "B'", "B2", "L", "L'", "L2",
			   "D", "D'", "D2", "U", "U'", "U2"]
MOVES = {"F":FRONT, "R":RIGHT, "U":TOP, "B":BACK, "L":LEFT, "D":BOTTOM}
MOVES_INDEX = {FRONT:"F", RIGHT:"R", TOP:"U", BACK:"B", LEFT:"L", BOTTOM:"D"}

TOPLFT = (0,0)
TOPEDGE = (0,1)
TOPRGHT = (0,2)
LFTEDGE = (1,0)
RGHTEDGE = (1,2)
BTMLFT = (2,0)
BTMEDGE = (2,1)
BTMRGHT = (2,2)
LFT = 0
MID = 1
RGHT = 2

AMOUNT_OF_CUBIES = 54

SIDE_SOLVED = 511
TWO_ROWS = 504
MID_SIDE = 144
CROSS = 186
TOP_ROW = 7
TOP_CORNERS = 5
LINE = 56
U = 26
FISH = 250
DOT = 16

SOLVED = 31
TOP_SOLVED = 15
TWO_LAYERS = 7
BOTTOM_SOLVED = 3
BOTTOM_CROSS = 1
SCRAMBLED = 0

STATES = {SOLVED:"solved", TOP_SOLVED:"top solved", TWO_LAYERS:"two layers solved", BOTTOM_SOLVED:"bottom solved", BOTTOM_CROSS:"bottom cross", SCRAMBLED:"scrambled"}

POSITION_CORNERS = "R' F R' B2 R F' R' B2 R2"
CYCLE_MID_CLOCKWISE = "F2 U L R' F2 L' R U F2"
CYCLE_MID_COUNTER_CLOCKWISE = "F2 U' L R' F2 L' R U' F2"
TOP_CROSS_U = "F U R U' R' F'"
TOP_CROSS_LINE = "F R U R' U' F'"
TOP_SIDE_SEQ = "R U R' U R U2 R'"
FIT_EDGE_RIGHT = "R U' R' U' F' U F"
FIT_EDGE_LEFT = "L' U L U F U' F'"
FIT_RIGHT_CORNER = "F' U' F"
FIT_RIGHT_CORNER_RIGHT = "R U' R'"
FIT_RIGHT_CORNER_OPP = "R U2 R'"
FIT_RIGHT_CORNER_LEFT = "U L' U' L"
FIT_LEFT_CORNER = "F U F'"
FIT_LEFT_CORNER_LEFT = "L' U L"
FIT_LEFT_CORNER_OPP = "L' U2 L"
FIT_LEFT_CORNER_RIGHT = "U' R U R'"
TAKE_OUT_CORNER_COUNTER_CLOCKWISE = "R U' R'"
TAKE_OUT_CORNER_CLOCKWISE = "R U R'"
ROTATE_TOP_CORNER = "R U2 R'"

BOTTOM_CROSS_STATE = [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
