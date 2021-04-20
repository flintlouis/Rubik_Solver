# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    astar.py                                           :+:    :+:             #
#                                                      +:+                     #
#    By: flintlouis <flintlouis@student.codam.nl      +#+                      #
#                                                    +#+                       #
#    Created: 2021/04/05 12:50:59 by flintlouis    #+#    #+#                  #
#    Updated: 2021/04/08 21:38:02 by flintlouis    ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import numpy as np
from heapq import heappush, heappop
from src.defines import *
from src.Rubik import Rubik
from src.misc import get_opposite

def calculate_heuristic(cube):
	heuristic = 0
	for side in range(6):
		for cubie in range(9):
			row = int(cubie / 3)
			col = int(cubie % 3)
			if cube[side][(row, col)]:
				colour = cube[side][(row, col)] - 1
				if side == colour:
					h = 2 - row
				elif side == TOP or side == BOTTOM:
					array = np.rot90(np.array(cube[side].cubies), colour)
					if np.where(array == cube[side][(row, col)])[1] == 1:
						h = 3
					else:
						h = 2
				else:
					if row == 2:
						if get_opposite(side) == colour:
							h = 2
						else:
							h = 1
					elif row == 0:
						if get_opposite(side) == colour:
							h = 4
						else:
							h = 3
					else:
						if get_opposite(side) == colour:
							h = 3
						else:
							h = 2
				heuristic += h
	return heuristic

def get_edge_colour(side, pos):
	if pos == TOPEDGE:
		return side.top[MID]
	elif pos == LFTEDGE:
		return side.left[MID]
	elif pos == RGHTEDGE:
		return side.right[MID]
	else:
		return side.bottom[MID]

def create_state(cube):
	state = []
	for side in range(6):
		for cubie in range(9):
				row = int(cubie / 3)
				col = int(cubie % 3)
				if (cubie % 2 == 1) and  get_edge_colour(cube[side], (row, col)) == BOTTOM:
					state.append(cube[side][(row, col)] + 1)
				else:
					state.append(0)
	return state

def get_neighbours(current):
	neighbours = []
	for move in VALID_MOVES:
		if "2" in move:
			continue
		neighbour = Rubik()
		neighbour.restore_snapshot(current.get_snapshot())
		neighbour.moves_taken = [move for move in current.moves_taken]
		neighbour.move(move)
		if current.get_snapshot() == neighbour.get_snapshot():
			continue
		neighbour.g += 1
		neighbour.f = neighbour.g + calculate_heuristic(neighbour)
		neighbours.append(neighbour)
	return neighbours

def in_closed_set(neighbour, closedset):
	for cube in range(len(closedset)):
		if closedset[cube].get_snapshot() == neighbour.get_snapshot():
			if neighbour.f < closedset[cube].f:
				closedset.pop(cube)
				return False
			return True
	return False

def create_bottom_cross(cube):
	openset = []
	closedset = []
	current = Rubik()
	current.restore_snapshot(create_state(cube))
	current.f = calculate_heuristic(current) + current.g
	heappush(openset, current)
	while len(openset):
		current = heappop(openset)
		closedset.append(current)
		if BOTTOM_CROSS_STATE == current.get_snapshot():
			cube.moves_taken = current.moves_taken
			for move in cube.moves_taken:
				cube.move(move, remember=False)
			return
		neighbours = get_neighbours(current)
		for neighbour in neighbours:
			if in_closed_set(neighbour, closedset):
				pass
			else:
				heappush(openset, neighbour)
