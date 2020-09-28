import tc.tcplayer

class KeyboardTurtle(tc.tcplayer.CombatTurtle):
    """Human-controlled Combat Turtle that uses keyboard inputs.

    Controls are as follows:
        [Up] -- move forward
        [Down] -- move backward
        [Left] -- turn left
        [Right] -- turn right
        [Space] -- fire missile
    """

    def class_name():
        """KeyboardTurtle.class_name() -> str
        Returns the name of the Combat Turtle AI.
        """

        return "Keyboard"

    #=========================================================================

    def setup(self):
        """KeyboardTurtle.setup() -> None
        Initialization code for human-controlled Combat Turtle.

        Sets up listeners for keyboard input.
        """

        pass

    #-------------------------------------------------------------------------

    def step(self):
        """KeyboardTurtle.setup() -> None
        Step event code for human-controlled Combat Turtle.

        Listens for keyboard input to control movement and firing.
        """

        pass

    #-------------------------------------------------------------------------

    def _up_key(self):
        """KeyboardTurtle._up_key() -> None
        Event handler for the [Up] key.

        [Up] should move the turtle forward.
        """

        pass

    #-------------------------------------------------------------------------

    def _down_key(self):
        """KeyboardTurtle._down_key() -> None
        Event handler for the [Down] key.

        [Down] should move the turtle backward.
        """

        pass

    #-------------------------------------------------------------------------

    def _left_key(self):
        """KeyboardTurtle._left_key() -> None
        Event handler for the [Left] key.

        [Left] should turn the turtle left.
        """

        pass

    #-------------------------------------------------------------------------

    def _right_key(self):
        """KeyboardTurtle._right_key() -> None
        Event handler for the [Right] key.

        [Right] should turn the turtle right.
        """

        pass

    #-------------------------------------------------------------------------

    def _space_bar(self):
        """KeyboardTurtle._space_bar() -> None
        Event handler for the [Space] bar.

        [Space] should attempt to fire a missile.
        """

        pass
