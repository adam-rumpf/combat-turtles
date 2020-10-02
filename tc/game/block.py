"""Defines the block class."""

### Use Tkinter to draw the blocks.

class Block:
    """Block class.

    Defines rectangular obstacles in the arena. Turtles cannot pass through
    blocks, and missile explode on contact with blocks.
    """

    #=========================================================================

    def __init__(self, left, right, bottom, top, col="black"):
        """_Block(left, right, bottom, top) -> _Block
        Block constructor.

        Requires the following positional arguments:
            left (float) -- leftmost x-coordinate (px)
            right (float) -- rightmost x-coordinate (px)
            bottom (float) -- lowermost y-coordinate (px)
            top (float) -- uppermost y-coordinate (px)

        Accepts the following optional keyword arguments:
            col (str or color tuple) ["black"] -- color of block
        """

        # Assign given attributes
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

        # Create a turtle to draw the block
        ###self.t = turtle.Turtle() # turtle object
        ###self._draw_block(col=col)

    #-------------------------------------------------------------------------

    def __del__(self):
        """~Block() -> None
        Block destructor destroys graphics turtle.
        """

        del self.t

    #-------------------------------------------------------------------------

    def contains(self, coords, closed=True):
        """Block.contains(coords[, closed]) -> bool
        Determines whether the block contains a given coordinate.

        Requires the following positional arguments:
            coords (tuple (float, float)) -- coordinate to test

        Accepts the following optional keyword arguments:
            closed (bool [True]) -- whether to include the boundaries

        Returns True if coords is within the block, and False otherwise.
        """

        # Determine output depending on whether boundaries are included
        if closed == True:
            # Closed boundaries
            if (coords[0] >= self.left and coords[0] <= self.right and
                coords[1] >= self.bottom and coords[1] <= self.top):
                return True
        else:
            # Open boundaries
            if (coords[0] > self.left and coords[0] < self.right and
                coords[1] > self.bottom and coords[1] < self.top):
                return True

        # If nothing has been returned yet, the tests failed
        return False

    #-------------------------------------------------------------------------

    def _draw_block(self, col="black"):
        """Block._draw_block() -> None
        Uses a turtle to draw the block.

        Accepts the following optional keyword arguments:
            col (str or color tuple) ["black"] -- color of block
        """

        pass

        # # Calculate dimensions
        # w = self.right - self.left # width
        # h = self.top - self.bottom # height

        # # Use turtle to draw block
        # self.t.hideturtle()
        # self.t.speed(0)
        # self.t.color(col)
        # self.t.penup()
        # self.t.goto(self.left, self.bottom)
        # self.t.setheading(0)
        # self.t.pendown()
        # self.t.begin_fill()
        # self.t.forward(w)
        # self.t.left(90)
        # self.t.forward(h)
        # self.t.left(90)
        # self.t.forward(w)
        # self.t.left(90)
        # self.t.forward(h)
        # self.t.end_fill()
