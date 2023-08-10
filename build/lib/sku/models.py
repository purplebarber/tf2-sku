from json import dumps


class itemClass:
    def __init__(self, data=None):
        # Initialize the properties with their default values
        self.Defindex = 0
        self.Quality = 6
        self.Craftable = True
        self.Killstreak = 0
        self.Australium = False
        self.Festive = False
        self.Effect = None
        self.PaintKit = None
        self.Wear = None
        self.ElevatedQuality = None
        self.Target = None
        self.CraftNum = None
        self.CrateSn = None
        self.Output = None
        self.OutputQuality = None

        # Update the properties with the provided data
        if data is not None:
            self.__dict__.update(data)


    def __str__(self):
        # Serialize the object to a JSON string
        return dumps(self.__dict__)
