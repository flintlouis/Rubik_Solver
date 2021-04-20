# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    main.py                                            :+:    :+:             #
#                                                      +:+                     #
#    By: flintlouis <flintlouis@student.codam.nl      +#+                      #
#                                                    +#+                       #
#    Created: 2021/03/17 18:54:23 by flintlouis    #+#    #+#                  #
#    Updated: 2021/04/08 22:02:23 by flintlouis    ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

from src.Rubik import Rubik
from src.solver import solve
from src.defines import VALID_MOVES

cube = Rubik()
value = ''
while (True):
	cube.draw(-150, 50, 50)
	print()
	print("[enter valid move or: scramble, solve, exit]")
	value = input("Enter move: ")
	if value == "solve":
		solve(cube)
	elif value == "scramble":
		cube.scramble(25, verbose=True)
	elif value == "exit":
		break
	elif value == "eval":
		solve(cube, eval=True)
	else:
		for move in value.split():
			if move in VALID_MOVES:
				cube.move(move)
			else:
				print("Incorrect move:", move)
