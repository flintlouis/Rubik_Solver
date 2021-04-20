# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    Rubik.py                                           :+:    :+:             #
#                                                      +:+                     #
#    By: flintlouis <flintlouis@student.codam.nl      +#+                      #
#                                                    +#+                       #
#    Created: 2021/03/18 13:27:12 by flintlouis    #+#    #+#                  #
#    Updated: 2021/04/08 21:40:12 by flintlouis    ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import numpy as np
import random
from src.Side import Side
from src.draw import init_turtle, turtle
from src.defines import *

class Rubik:

	def __init__(self):
		self.f = 0
		self.g = 0
		self.sides = []
		self.snapshot = []
		self.moves_taken = []
		for colour in COLOURS:
			self.sides.append(Side(colour))
		self[FRONT].set_adjacent(
			self[TOP].cubies[2],
			self[RIGHT].cubies[:,0],
			np.flip(self[BOTTOM].cubies[0]),
			np.flip(self[LEFT].cubies[:,2])
		)
		self[RIGHT].set_adjacent(
			np.flip(self[TOP].cubies[:,2]),
			self[BACK].cubies[:,0],
			np.flip(self[BOTTOM].cubies[:,2]),
			np.flip(self[FRONT].cubies[:,2])
		)
		self[BACK].set_adjacent(
			np.flip(self[TOP].cubies[0]),
			self[LEFT].cubies[:,0],
			self[BOTTOM].cubies[2],
			np.flip(self[RIGHT].cubies[:,2])
		)
		self[LEFT].set_adjacent(
			self[TOP].cubies[:,0],
			self[FRONT].cubies[:,0],
			self[BOTTOM].cubies[:,0],
			np.flip(self[BACK].cubies[:,2])
		)
		self[TOP].set_adjacent(
			np.flip(self[BACK].cubies[0]),
			np.flip(self[RIGHT].cubies[0]),
			np.flip(self[FRONT].cubies[0]),
			np.flip(self[LEFT].cubies[0])
		)
		self[BOTTOM].set_adjacent(
			self[FRONT].cubies[2],
			self[RIGHT].cubies[2],
			self[BACK].cubies[2],
			self[LEFT].cubies[2]
		)

	def __getitem__(self, side):
		return self.sides[side]

	def __lt__(self, other):
		if self.f < other.f:
			return True
		return False

	def draw(self, x, y, size):
		init_turtle()
		side_size = size * 3
		for side in range(6):
			if side in [FRONT, RIGHT, BACK]:
				self[side].draw(x+(side*side_size), y, size)
			elif side == LEFT:
				self[side].draw(x-side_size, y, size)
			elif side == TOP:
				self[side].draw(x, y+side_size, size)
			elif side == BOTTOM:
				self[side].draw(x, y-side_size, size)
		turtle.update()

	def turn(self, move):
		if '\'' in move:
			amount = 1
		elif '2' in move:
			amount = 2
		else:
			amount = 3
		side = MOVES[move[0]]
		self[side].turn(amount)

	def get_snapshot(self):
		state = []
		for side in self.sides:
			for cubie in side.cubies.flatten():
				state.append(cubie)
		return state

	def take_snapshot(self):
		self.snapshot = []
		for side in self.sides:
			for cubie in side.cubies.flatten():
				self.snapshot.append(cubie)

	def restore_snapshot(self, custom_snapshot=None):
		if custom_snapshot:
			self.snapshot = custom_snapshot
		if len(self.snapshot) != AMOUNT_OF_CUBIES:
			raise Exception("Invalid snapshot")
		i = 0
		for side in range(6):
			for cubie in range(9):
				row = int(cubie / 3)
				col = int(cubie % 3)
				self[side].cubies[row, col] = self.snapshot[i]
				i += 1

	def move(self, moves, verbose=False, remember=True):
		for move in moves.split():
			if move in VALID_MOVES:
				if verbose:
					print(move, end=' ')
				if remember:
					self.moves_taken.append(move)
				self.turn(move)
			else:
				raise Exception("Invalid move")

	def scramble(self, amount, seed=None, verbose=False, remember=True):
		if seed != None:
			random.seed(seed)
		for _ in range(amount):
			move = random.randint(0, 17)
			if verbose:
				print(VALID_MOVES[move], end=' ')
			if remember:
				self.moves_taken.append(VALID_MOVES[move])
			self.turn(VALID_MOVES[move])
		if verbose:
			print()
