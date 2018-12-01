"""class that handles if music is playing or not"""


class StopSign:
    """creates a flag that is for checking if music is
       playing or not.

    Args:
        flag (bool): if music is playing
    """
    # pylint: disable=W0613
    def __init__(self, flag):
        self.flag = False

    def get_flag(self):
        """Gets the flag"""
        return self.flag

    def set_flag(self, new):
        """Sets the flag to a new state.

        Args:
            new (bool): new state of music
        """
        self.flag = new
