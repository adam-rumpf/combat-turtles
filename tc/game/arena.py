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
        """Arena.get_names() -> list
        Static method to return list of arena layout names.
        """

        return ["Empty Arena", "Central Column Arena", "Corner Column Arena",
                "Doorway Arena", "Plus-Shaped Arena"]

    #-------------------------------------------------------------------------

    def get_p1_coords(index):
        """Arena.get_p1_coords() -> (int, int)
        Static method to return the default starting coordinates of Player 1.

        Requires the following positional arguments:
            index (int) -- arena layout index
        """

        # All currently-defined arenas use the same initial coordinates
        return (200, 0)

    #-------------------------------------------------------------------------

    def get_p2_coords(index):
        """Arena.get_p2_coords() -> (int, int)
        Static method to return the default starting coordinates of Player 2.

        Requires the following positional arguments:
            index (int) -- arena layout index
        """

        # All currently-defined arenas use the same initial coordinates
        return (-200, 0)

    #-------------------------------------------------------------------------

    def get_p1_heading(index):
        """Arena.get_p1_heading() -> int
        Static method to return the default starting heading of Player 1.

        Requires the following positional arguments:
            index (int) -- arena layout index
        """

        # All currently-defined arenas use the same initial headings
        return 90

    #-------------------------------------------------------------------------

    def get_p2_heading(index):
        """Arena.get_p2_heading() -> int
        Static method to return the default starting heading of Player 2.

        Requires the following positional arguments:
            index (int) -- arena layout index
        """

        # All currently-defined arenas use the same initial headings
        return -90

    #=========================================================================

    def __init__(self, size=(600, 400), layout=0, walls=5):
        """Arena([size], [layout], [walls]) -> Arena
        Arena constructor, including obstacle setup.

        Accepts the following optional keyword arguments:
            size (tuple (int, int)) [(600, 400)] -- arena width/height (px)
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
            self._single_block()
        elif layout == 2:
            # Four small squares near corners
            self._corner_blocks()
        elif layout == 3:
            # Central wall with passage
            self._doorway_blocks()
        elif layout == 4:
            # Plus sign
            self._plus_blocks()

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
        self.blocks.append(Block(left, left+width, bottom, top))
        self.blocks.append(Block(right-width, right, bottom, top))
        self.blocks.append(Block(left, right, top-width, top))
        self.blocks.append(Block(left, right, bottom, bottom+width))

    #-------------------------------------------------------------------------

    def _single_block(self):
        """Arena._single_block() -> None
        Generates the blocks of the Central Column arena type.
        """

        # Define column block
        self.blocks.append(Block(-80, 80, -80, 80))

    #-------------------------------------------------------------------------

    def _corner_blocks(self):
        """Arena._corner_blocks() -> None
        Generates the blocks of the Corner Column arena type.
        """

        # Define four small columns
        self.blocks.append(Block(-120, -80, -120, -80))
        self.blocks.append(Block(-120, -80, 120, 80))
        self.blocks.append(Block(120, 80, -120, -80))
        self.blocks.append(Block(120, 80, 120, 80))

    #-------------------------------------------------------------------------

    def _doorway_blocks(self):
        """Arena._doorway_blocks() -> None
        Generates the blocks of the Central Doorway arena type.
        """

        # Define two wall portions
        self.blocks.append(Block(-20, 20, -200, -40))
        self.blocks.append(Block(-20, 20, 40, 200))

    #-------------------------------------------------------------------------

    def _plus_blocks(self):
        """Arena._plus_blocks() -> None
        Generates the blocks of the Plus-Shaped arena type.
        """

        # Define two crossing wall portions
        self.blocks.append(Block(-20, 20, -100, 100))
        self.blocks.append(Block(-100, 100, -20, 20))
