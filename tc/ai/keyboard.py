import tc.ct

class KeyboardTurtle(tc.ct.CombatTurtle):
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

    def setup():
        """KeyboardTurtle.setup() -> None
        Initialization code for human-controlled Combat Turtle.

        Sets up listeners for keyboard input.
        """

        pass

    #-------------------------------------------------------------------------

    def step():
        """KeyboardTurtle.setup() -> None
        Step event code for human-controlled Combat Turtle.

        Listens for keyboard input to activate movement and firing.
        """

        pass
