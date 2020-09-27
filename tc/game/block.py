class _Block:
    """Block class.

    Defines rectangular obstacles in the arena. Turtles cannot pass through
    blocks, and missile explode on contact with blocks.
    """

    #=========================================================================

    def __init__(self, left, right, top, bottom):
        """_Block(left, right, top, bottom) -> _Block
        Block constructor.

        Requires the following positional arguments:
            left (float) -- leftmost x-coordinate (px)
            right (float) -- rightmost x-coordinate (px)
            top (float) -- uppermost y-coordinate (px)
            bottom (float) -- lowermost y-coordinate (px)
        """

        # Assign given attributes
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        ###
        # Use a turtle to draw the block.

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
        if (closed == True):
            # Closed boundaries
            if ((coords[0] >= self.left) and (coords[0] <= self.right) and
                (coords[1] >= self.bottom) and (coords[1] <= self.top)):
                return True
        else:
            # Open boundaries
            if ((coords[0] > self.left) and (coords[0] < self.right) and
                (coords[1] > self.bottom) and (coords[1] < self.top)):
                return True

        # If nothing has been returned yet, the tests failed
        return False
