# **************************************************************************** #
#                                                                              #
#                                                         ::::::::             #
#    draw.py                                            :+:    :+:             #
#                                                      +:+                     #
#    By: flintlouis <flintlouis@student.codam.nl      +#+                      #
#                                                    +#+                       #
#    Created: 2021/03/18 13:28:50 by flintlouis    #+#    #+#                  #
#    Updated: 2021/04/08 21:38:09 by flintlouis    ########   odam.nl          #
#                                                                              #
# **************************************************************************** #

import turtle
from src.defines import COLOURS

WIDTH, HEIGHT = 1200, 800
PEN_SIZE = 2

def move_turtle(x, y):
	turtle.penup()
	turtle.goto(x, y)
	turtle.pendown()

def draw_square(x, y, colour, size):
	move_turtle(x, y)
	turtle.begin_fill()
	turtle.color("black", COLOURS[colour])
	for i in range(4):
		turtle.forward(size)
		turtle.right(90)
	turtle.end_fill()

def draw_outline(x, y, size):
	move_turtle(x, y)
	turtle.pensize(PEN_SIZE+2)
	for i in range(4):
		turtle.forward(size*3)
		turtle.right(90)
	turtle.pensize(PEN_SIZE)

def draw_side(x, y, cubies, size):
	for i in range(3):
		for j in range(3):
			draw_square(x+(j*size), y-(i*size), cubies[i,j], size)
	draw_outline(x, y, size)

def init_turtle():
	window = turtle.Screen()
	window.setup(WIDTH, HEIGHT)
	turtle.speed(0)
	turtle.pensize(PEN_SIZE)
	turtle.tracer(0, 0)
	turtle.hideturtle()
