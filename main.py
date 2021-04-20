# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    main.py                                            :+:    :+:             #
#                                                      +:+                     #
#    By: flintlouis <flintlouis@student.codam.nl      +#+                      #
#                                                    +#+                       #
#    Created: 2021/03/17 18:54:23 by flintlouis    #+#    #+#                  #
#    Updated: 2021/04/20 13:37:23 by flintlouis    ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

from src.Rubik import Rubik
from src.solver import solve
from src.defines import VALID_MOVES

error_snapshot = [5, 5, 5, 2, 0, 5, 4, 1, 4, 0, 4, 2, 0, 1, 3, 3, 0, 3, 4, 3, 1, 0, 2, 5, 2, 1, 1, 0, 0, 0, 3, 3, 1, 5, 4, 2, 1, 4, 0, 2, 4, 4, 2, 5, 5, 4, 2, 3, 1, 5, 3, 3, 2, 1]
cube = Rubik()
cube.restore_snapshot(error_snapshot)
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
