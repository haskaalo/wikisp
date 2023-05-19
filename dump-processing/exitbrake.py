class ExitBrake:
    def __init__(self):
        self._shutdown = False

    def brake(self):
        self._shutdown = True

    def shutdown(self):

        return self._shutdown
