# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    Side.py                                            :+:    :+:             #
#                                                      +:+                     #
#    By: flintlouis <flintlouis@student.codam.nl      +#+                      #
#                                                    +#+                       #
#    Created: 2021/03/18 13:27:15 by flintlouis    #+#    #+#                  #
#    Updated: 2021/04/08 21:38:18 by flintlouis    ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import numpy as np
from src.draw import draw_side

class Side:

	def __init__(self, side):
		self.side = side
		self.cubies = np.full((3,3), side)

	def set_adjacent(self, top, right, bottom, left):
		self.top = top
		self.right = right
		self.bottom = bottom
		self.left = left
		
		self.top_side = top[0]
		self.right_side = right[0]
		self.bottom_side = bottom[0]
		self.left_side = left[0]

	def draw(self, x, y, size):
		draw_side(x, y, self.cubies, size)

	def rotate_face(self):
		tmp_top_row = np.array(self.cubies[0])
		self.cubies[0,0] = self.cubies[0,2]
		self.cubies[0,1] = self.cubies[1,2]
		self.cubies[0,2] = self.cubies[2,2]
		self.cubies[1,2] = self.cubies[2,1]
		self.cubies[2,2] = self.cubies[2,0]
		self.cubies[2,1] = self.cubies[1,0]
		self.cubies[2,0] = tmp_top_row[0]
		self.cubies[1,0] = tmp_top_row[1]

	def turn(self, amount):
		for n in range(amount):
			self.rotate_face()
			sides = [self.top, self.right, self.bottom, self.left]
			tmp_top = np.array(self.top)
			for side in range(4):
				for block in range(3):
					if side != 3:
						sides[side][block] = int(sides[side + 1][block])
					else:
						sides[side][block] = int(tmp_top[block])

	def get_pattern(self):
		array = self.cubies.flatten()
		pattern = 0
		for i in range(9):
			if array[i] == self.side:
				pattern |= (1 << i)
		return pattern

	def is_pattern(self, pattern, equal=False):
		if equal:
			return self.get_pattern() == pattern
		else:
			return (self.get_pattern() & pattern) == pattern

	def __getitem__(self, pos):
		x, y = pos
		return self.cubies[x, y]
