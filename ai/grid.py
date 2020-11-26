# Built-In Example AI

# Title: GridTurtle
# Author: Adam Rumpf
# Version: 1.0.0
# Date: 11/26/2020

import game.tcturtle

class CombatTurtle(game.tcturtle.TurtleParent):
    """Grid combat turtle.

    A turtle capable of navigating around obstacles by converting the arena
    into a grid graph and finding shortest paths between nodes. Directly
    pursues the opponent when there is line of sight.
    
    This submodule defines its own lightweight Graph class for use in
    representing the arena and determining shortest paths.
    
    For general information about mathematical graphs, see:
    https://mathworld.wolfram.com/Graph.html
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "GridTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Navigates around obstacles and pursues when close."

    #-------------------------------------------------------------------------

    def class_shape():
        """CombatTurtle.class_shape() -> (int or tuple)
        Static method to define the Combat Turtle's shape image.

        The return value can be either an integer or a tuple of tuples.

        Returning an integer index selects one of the following preset shapes:
            0 -- arrowhead (also default in case of unrecognized index)
            1 -- turtle
            2 -- plow
            3 -- triangle
            4 -- kite
            5 -- pentagon
            6 -- hexagon
            7 -- star

        A custom shape can be defined by returning a tuple of the form
        (radius, angle), where radius is a tuple of radii and angle is a tuple
        of angles (in radians) describing the polar coordinates of a polygon's
        vertices. The shape coordinates should be given for a turtle facing
        east.
        """

        return 4

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for Combat Turtle.
        """

        # Initialize a graph representation of the arena
        self.ArenaGraph = Graph()

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.
        """

        pass

##############################################################################

class Graph():
    """A rudimentary graph class.
    
    Defines a grid graph representation of the arena. A graph is made up of
    vertices which represent evenly-spaced free coordinates within the arena.
    Edges connect vertices which have a clear path between them.
    
    This class used a Vertex class (see below) as a container to store
    vertex-level attributes and adjacency lists. Edges are not stored
    explicitly, and are instead inferred from the vertex adjacency lists.
    """
    
    #-------------------------------------------------------------------------
    
    def __init__(self, rows=20, columns=20):
        """Graph([rows], [columns]) -> Graph
        Graph object constructor.
        
        Accepts the following optional keyword arguments:
            rows (int) [20] -- number of rows in the grid graph
            columns (int) [20] -- number of columns in the grid graph
        
        Initializes the vertex set of a grid graph with a specified number of
        rows and columns. The rows and columns are chosen to correspond to
        arena coordinates spaces as evenly as possible to cover the entire
        arena in a rectangular grid.
        
        A vertex is defined for each grid intersection that does not collide
        with a block, and an edge is defined between adjacent grid
        intersections (both rectilinearly and diagonally) as long as no
        obstacles fall between them.
        """
        
        # Initialize vertex list as an empty dictionary
        self.v = dict()
        
        # Scan arena and create vertices at the clear coordinates
        for i in range(columns):
            for j in range(rows):
                pass
    
    #------------------------------------------------------------------------
    
    def __del__(self):
        """Graph.__del__() -> None
        Graph destructor deletes all vertex objects.
        """
        
        self.v.clear()
    
    #------------------------------------------------------------------------
    
    def nearest_vertex(self, coord):
        """Graph.nearest_vertex(coord) -> int
        Returns the integer ID of the vertex nearest a given coordinate.
        """
        
        pass

##############################################################################

class Vertex:
    """Represents a graph vertex.
    
    A container class which stores the arena coordinates that this vertex
    represents as well as a set of the vertices adjacent to this vertex.
    """
    
    #-------------------------------------------------------------------------
    
    def __init__(self, coord):
        """Vertex(coord) -> Vertex
        Vertex object constructor.
        
        Requires the following positional arguments:
            coord (tuple) -- arena coordinate that this vertex represents
        """
        
        # Initialize coordinate attribute
        self.coord = coord
