"""Main Turtle Combat script."""

import turtle
from tc import ct

def play_game():
    """Main driver for the Turtle Combat game."""

    wn = turtle.Screen()
    p1 = ct.CombatTurtle()
    print(p1)
    wn.mainloop()
    turtle.bye()

play_game()
