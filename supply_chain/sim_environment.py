class SimEnvironment:
    """This class represents the environment of the simulation.
    The map is an element in the environment"""

    def __init__(
        self,
    ) -> None:
        self.time: int = 0
        """The current time of the simulation"""

    def get_time(self) -> int:
        """Get the current time of the simulation"""
        return self.time
