class _Arena():
    """Arena class.

    Acts as a container to store the contents of the arena, including all of
    the blocks.
    """

    ###
    # Automatic layouts should be defined as class attributes.

    #-------------------------------------------------------------------------

    def __init__(self, width, height, walls=5.0):
        """_Arena(width, height[, walls]) -> _Arena
        Arena constructor, including obstacle setup.

        Requires the following positional arguments:
            width (float) -- width of arena (px)
            height (float) -- height of arena (px)

        Accepts the following optional keyword arguments:
            walls (float [5.0]) -- thickness (px) of walls surrounding arena,
                (walls excluded unless argument is positive)
        
        The arena is centered at the origin and has the specified total width
        and height. If any walls are included, their thickness is taken from
        the interior of the arena so that the total arena dimensions
        (including the walls) remains the same.
        """

        # Assign given attributes
        self.width = width
        self.height = height

        # Initialize block object list
        self.blocks = []

        # Generate walls around arena
        if (walls > 0):
            ### Generate blocks.
            pass

        ###
        # Add some methods for automatically generating specific layouts, or
        # possibly random layouts. Also handle the window.
