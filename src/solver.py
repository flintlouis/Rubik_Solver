# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    solver.py                                          :+:    :+:             #
#                                                      +:+                     #
#    By: flintlouis <flintlouis@student.codam.nl      +#+                      #
#                                                    +#+                       #
#    Created: 2021/04/01 15:12:25 by flintlouis    #+#    #+#                  #
#    Updated: 2021/04/08 22:02:29 by flintlouis    ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import time
import numpy as np
from src.defines import *
from src.astar import get_opposite, create_bottom_cross
from src.misc import *

def optimize_moves(cube):
	i = 0
	size = len(cube.moves_taken)
	moves = cube.moves_taken
	while i < (size - 1):
		if moves[i][0] == moves[i+1][0]:
			if moves[i] == moves[i+1]:
				if '2' in moves[i]:
					i, size = delete_both_moves(moves, i, size)
				else:
					moves[i+1] = moves[i][0] + '2'
					moves.pop(i)
			elif '2' not in moves[i] and '2' not in moves[i+1]:
				i, size = delete_both_moves(moves, i, size)
			else:
				if '\'' in moves[i] or '\'' in moves[i+1]:
					moves[i+1] = moves[i][0]
				else:
					moves[i+1] = moves[i][0] + '\''
				moves.pop(i)
			size -= 1
		else:
			i += 1
	cube.moves_taken = moves
	return len(cube.moves_taken)

def rotate90_pattern(pattern):
	new_pattern = (16 & pattern)
	new_pattern |= (4 & pattern) >> 2
	new_pattern |= (32 & pattern) >> 4
	new_pattern |= (256 & pattern) >> 6
	new_pattern |= (128 & pattern) >> 2
	new_pattern |= (64 & pattern) << 2
	new_pattern |= (8 & pattern) << 4
	new_pattern |= (1 & pattern) << 6
	new_pattern |= (2 & pattern) << 2
	return new_pattern

def	pattern_on_side(side, pattern, equal=False):
	side_pattern = side.get_pattern()
	for rot in range(1, 5):
		pattern = rotate90_pattern(pattern)
		if side.is_pattern(pattern, equal):
			return rot
	return 0

def check_state(patterns, btm_pattern, top_pattern, side_pattern):
	if (patterns[BOTTOM] & btm_pattern) != btm_pattern:
		return False
	if (patterns[TOP] & top_pattern) != top_pattern:
		return False
	for side in range(4):
		if (patterns[side] & side_pattern) != side_pattern:
			return False
	return True

def get_state(cube):
	patterns = [pattern.get_pattern() for pattern in cube.sides]
	if (check_state(patterns, SIDE_SOLVED, SIDE_SOLVED, SIDE_SOLVED)):
		return SOLVED
	if (check_state(patterns, SIDE_SOLVED, SIDE_SOLVED, TWO_ROWS)):
		return TOP_SOLVED
	if (check_state(patterns, SIDE_SOLVED, 0, TWO_ROWS)):
		return TWO_LAYERS
	if (check_state(patterns, SIDE_SOLVED, 0, MID_SIDE)):
		return BOTTOM_SOLVED
	if (check_state(patterns, CROSS, 0, 0)):
		return BOTTOM_CROSS
	return SCRAMBLED

def sequence(front_side, moves):
	new_moves = ""
	for move in moves.split():
		move_index = MOVES[move[0]]
		if move_index < 4:
			new_move = (move_index + front_side) % 4
		else:
			new_move = move_index
		rest = move[1:]
		new_moves = new_moves + MOVES_INDEX[new_move] + rest + ' '
	return new_moves

def match_corners(cube):
	while (True):
		patterns_matched = 0
		for side in range(4):
			if cube[side][TOPLFT] == cube[side][TOPRGHT]:
				side_matched, colour = side, cube[side][TOPLFT]
				patterns_matched += 1
		if patterns_matched == 0:
			cube.move(POSITION_CORNERS)
		else:
			if side_matched != colour:
				if is_oppisite(colour, side_matched):
					cube.move("U2")
				elif is_right(colour, cube[side_matched]):
					cube.move("U'")
				else:
					cube.move("U")
			if patterns_matched == 1:
				cube.move(sequence(get_opposite(colour), POSITION_CORNERS))
			else:
				break

def match_edges(cube):
	while (True):
		patterns_matched = 0
		side_matched = 0
		for side in range(4):
			if cube[side].is_pattern(SIDE_SOLVED):
				side_matched = side
				patterns_matched += 1
		if patterns_matched == 4:
			return
		side = get_opposite(side_matched)
		if is_left(cube[side][0,1], cube[side]):
			cube.move(sequence(side, CYCLE_MID_CLOCKWISE))
		else:
			cube.move(sequence(side, CYCLE_MID_COUNTER_CLOCKWISE))

def solve_final_layer(cube):
	match_corners(cube)
	match_edges(cube)

def create_top_cross(cube):
	while not cube[TOP].is_pattern(CROSS):
		for pattern in [U, LINE, DOT]:
			rot = pattern_on_side(cube[TOP], pattern)
			if rot:
				if pattern == U:
					cube.move(sequence(rot, TOP_CROSS_U))
				elif pattern == LINE:
					cube.move(sequence(rot, TOP_CROSS_LINE))
				else:
					cube.move(TOP_CROSS_U)
				break

def create_top_side(cube):
	while cube[TOP].get_pattern() != SIDE_SOLVED:
		if cube[TOP].get_pattern() == CROSS:
			for side in range(4):
				left_side = (side + 3) % 4
				if cube[left_side][TOPRGHT] == TOP:
					cube.move(sequence(side, TOP_SIDE_SEQ))
					break
		else:
			rot = pattern_on_side(cube[TOP], FISH, equal=True)
			if rot:
				cube.move(sequence(rot, TOP_SIDE_SEQ))
			else:
				for side in range(4):
					if cube[side][TOPLFT] == TOP:
						cube.move(sequence(side, TOP_SIDE_SEQ))
						break

def solve_top_side(cube):
	create_top_cross(cube)
	create_top_side(cube)

def fit_edge(cube):
	side = 0
	while side < 4:
		if cube[side][TOPEDGE] != TOP and cube[side].top[MID] != TOP:
			if cube[side].top[MID] == get_opposite(side):
				if is_right(cube[side][TOPEDGE], cube[side]):
					cube.move(sequence(get_right(side), FIT_EDGE_RIGHT))
				else:
					cube.move(sequence(get_left(side), FIT_EDGE_LEFT))
			elif cube[side][TOPEDGE] == side:
				if is_right(cube[side].top[MID], cube[side]):
					cube.move(sequence(side, "U " + FIT_EDGE_RIGHT))
				else:
					cube.move(sequence(side, "U' " + FIT_EDGE_LEFT))
			elif cube[side].top[MID] == side:
				if is_left(cube[side][TOPEDGE], cube[side]):
					cube.move(sequence(get_left(side), "U2 " + FIT_EDGE_RIGHT))
				else:
					cube.move(sequence(get_right(side), "U2 " + FIT_EDGE_LEFT))
			else:
				if is_right(cube[side].top[MID], cube[side]):
					cube.move(sequence(get_opposite(side), "U " + FIT_EDGE_LEFT))
				else:
					cube.move(sequence(get_opposite(side), "U' " + FIT_EDGE_RIGHT))
			side = 0
		side += 1

def take_out_edge(cube):
	side = 0
	while side < 4:
		if cube[side][LFTEDGE] == side and cube[side][RGHTEDGE] == side:
			side += 1
			continue
		elif cube[side][RGHTEDGE] != side:
			cube.move(sequence(side, FIT_EDGE_RIGHT))
		else:
			cube.move(sequence(side, FIT_EDGE_LEFT))
		fit_edge(cube)
		side = 0

def solve_side_edges(cube):
	fit_edge(cube)
	take_out_edge(cube)

def check_corner(side, corner):
	if corner == BTMLFT:
		a, b, = side.bottom[RGHT], side.left[LFT]
	else:
		a, b, = side.bottom[LFT], side.right[RGHT]
	return (side[corner] == BOTTOM or a == BOTTOM or b == BOTTOM)

def fit_corner(cube):
	side = 0
	while side < 4:
		if cube[side][TOPLFT] == BOTTOM:
			if cube[side].top[LFT] == side:
				cube.move(sequence(side, FIT_LEFT_CORNER))
			elif cube[side].top[LFT] == get_left(side):
				cube.move(sequence(get_left(side), FIT_LEFT_CORNER_LEFT))
			elif cube[side].top[LFT] == get_opposite(side):
				cube.move(sequence(get_opposite(side), FIT_LEFT_CORNER_OPP))
			else:
				cube.move(sequence(side, FIT_LEFT_CORNER_RIGHT))
			side = 0
		elif cube[side][TOPRGHT] == BOTTOM:
			if cube[side].top[RGHT] == side:
				cube.move(sequence(side, FIT_RIGHT_CORNER))
			elif cube[side].top[RGHT] == get_right(side):
				cube.move(sequence(get_right(side), FIT_RIGHT_CORNER_RIGHT))
			elif cube[side].top[RGHT] == get_opposite(side):
				cube.move(sequence(get_opposite(side), FIT_RIGHT_CORNER_OPP))
			else:
				cube.move(sequence(side, FIT_RIGHT_CORNER_LEFT))
			side = 0
		else:
			side += 1

def take_out_corner(cube):
	for side in range(4):
		if (check_corner(cube[side], BTMRGHT) and cube[side][BTMRGHT] != side):
			if cube[side][BTMRGHT] == BOTTOM:
				cube.move(sequence(side, TAKE_OUT_CORNER_COUNTER_CLOCKWISE))
			else:
				cube.move(sequence(side, TAKE_OUT_CORNER_CLOCKWISE))
			return False
	return True
	
def corner_on_top(cube):
	for side in range(4):
		if cube[side].top[RGHT] == BOTTOM:
			for free_side in range(4):
				free_side = (free_side + side) % 4
				if (not check_corner(cube[free_side], BTMRGHT)) or not (cube[free_side][BTMRGHT] == free_side):
					if free_side == side:
						cube.move(sequence(side, ROTATE_TOP_CORNER))
					elif get_opposite(side) == free_side:
						cube.move(sequence(free_side, "U2 " + ROTATE_TOP_CORNER))
					elif get_right(side) == free_side:
						cube.move(sequence(free_side, "U' " + ROTATE_TOP_CORNER))
					else:
						cube.move(sequence(free_side, "U " + ROTATE_TOP_CORNER))
			return

def create_bottom_layer(cube):
	while (get_state(cube) & BOTTOM_SOLVED) != BOTTOM_SOLVED:
		fit_corner(cube)
		if take_out_corner(cube):
			corner_on_top(cube)

def solve(cube, eval=False):
	start = round(time.time() * 1000)
	cube.moves_taken = []
	state = get_state(cube)
	while state != SOLVED:
		if eval:
			cube.draw(-150, 50, 50)
			input(STATES[state])
		if state == TOP_SOLVED:
			solve_final_layer(cube)
		elif state == TWO_LAYERS:
			solve_top_side(cube)
		elif state == BOTTOM_SOLVED:
			solve_side_edges(cube)
		elif state == BOTTOM_CROSS:
			create_bottom_layer(cube)
		else:
			create_bottom_cross(cube)
		state = get_state(cube)
	if eval:
		print(STATES[state])
	optimize_moves(cube)
	end = round(time.time() * 1000)
	print_info(cube, start, end)
