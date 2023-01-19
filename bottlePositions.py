class bottlePositions:
    def __init__(self, visualizor):
      self.positions = [
            {
                "x": 200,
                "y": 50
            },
            {
                "x": 100,
                "y": -50
            },
            {
                "x": 10,
                "y": 0
            }
        ]

    def getPosition(self):
        return self.positions