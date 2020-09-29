"""Defines the arena container class."""

from .block import Block

class Arena:
    """Arena class.

    Acts as a container to store the contents of the arena, including all of
    the blocks. The arrangement of blocks is chosen by passing a numerical ID
    to the constructor.

    The arena layouts are defined as follows:
        0 -- empty
        1 -- large square in middle
        2 -- four columns near corners
        3 -- wall with a central passage
        4 -- plus sign
    """

    #-------------------------------------------------------------------------

    def get_names():
        """Arena.get_names() -> str[]
        Static method to return a list of arena layout names.

        The names in this list correspond to the layout ID numbers.
        """

        return ["Empty", "Central Column", "Corner Columns", "Doorway",
                "Plus"]

    #=========================================================================

    def __init__(self, size=(400, 400), layout=0, walls=5):
        """Arena([size], [layout], [walls]) -> Arena
        Arena constructor, including obstacle setup.

        Accepts the following optional keyword arguments:
            size (tuple (int, int)) [(400, 400)] -- arena width/height (px)
            layout (int) [0] -- arena obstacle layout ID (see class docstring)
            walls (int) [5] -- thickness (px) of walls surrounding arena
                (walls excluded unless argument is positive)

        The arena is centered at the origin and has the specified total width
        and height. If any walls are included, their thickness is taken from
        the interior of the arena so that the total arena dimensions
        (including the walls) remains the same.
        """

        # Assign given attributes
        self.size = size

        # Initialize block object list
        self.blocks = []

        # Generate walls around arena
        if walls > 0:
            self._create_walls(walls)

        # Generate the walls defined by the layout (default to empty)
        if layout == 1:
            # Large square in middle
            pass
        elif layout == 2:
            # Four small squares near corners
            pass
        elif layout == 3:
            # Central wall with passage
            pass
        elif layout == 4:
            # Plus sign
            pass

        ###
        # Add some methods for automatically generating specific layouts, or
        # possibly random layouts. Also handle the window.

    #-------------------------------------------------------------------------

    def __del__(self):
        """~Arena() -> None
        Arena destructor deletes all blocks in arena.
        """

        del self.blocks[:]

    #-------------------------------------------------------------------------

    def _create_walls(self, width):
        """Arena._create_walls() -> None
        Generates blocks to define the walls of an arena.

        Walls are Block objects which are added to the Arena's block list.
        The arena's size is considered to be the external dimension of the
        arena, with the wall thickness reducing the interior size.

        Requires the following positional arguments:
            width (int) -- thickness of walls (px)
        """

        # Determine coordinates of edges
        left = int(-self.size[0]/2)
        right = int(self.size[0]/2)
        top = int(self.size[1]/2)
        bottom = int(-self.size[1]/2)

        # Define walls
        self.blocks.append(Block(left, left+width, top, bottom))
        self.blocks.append(Block(right-width, right, top, bottom))
        self.blocks.append(Block(left, right, top, top-width))
        self.blocks.append(Block(left, right, bottom+width, bottom))
