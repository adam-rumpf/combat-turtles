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

        return ["Empty", "Central Column", "Corner Columns", "Doorway", "Plus"]

    #=========================================================================

    def __init__(self, size=(200, 200), layout=0, walls=5.0):
        """Arena([size], [layout], [walls]) -> Arena
        Arena constructor, including obstacle setup.

        Accepts the following optional keyword arguments:
            size (tuple (int, int)) [(200, 200)] -- arena width/height (px)
            layout (int) [0] -- arena obstacle layout ID (see class docstring)
            walls (float [5.0]) -- thickness (px) of walls surrounding arena,
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
            ### Generate blocks.
            pass

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
