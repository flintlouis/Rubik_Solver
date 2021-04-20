# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    misc.py                                            :+:    :+:             #
#                                                      +:+                     #
#    By: flintlouis <flintlouis@student.codam.nl      +#+                      #
#                                                    +#+                       #
#    Created: 2021/04/08 21:25:24 by flintlouis    #+#    #+#                  #
#    Updated: 2021/04/08 21:40:18 by flintlouis    ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

def print_moves(moves):
	for move in moves:
		print(move, end=' ')
	print()

def print_info(cube, start, end):
	print_moves(cube.moves_taken)
	print("Moves taken:", len(cube.moves_taken))
	print("Time taken in sec:", abs(start - end) / 1000)

def get_left(side):
	return ((side + 3) % 4)

def get_right(side):
	return ((side + 1) % 4)

def is_oppisite(colour, side):
	return (abs(colour - side) == 2)

def is_right(colour, side):
	return (side.right_side == colour)

def is_left(colour, side):
	return (side.left_side == colour)

def get_opposite(side):
	return ((side + 2) % 4)

def delete_both_moves(moves, i, size):
	moves.pop(i + 1)
	moves.pop(i)
	return i - 1, size - 1
