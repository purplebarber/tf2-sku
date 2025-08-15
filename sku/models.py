from json import dumps
from typing import Optional


class itemClass:
    Defindex: int
    Quality: int
    Craftable: bool
    Killstreak: int
    Australium: bool
    Festive: bool
    Effect: Optional[int]
    PaintKit: Optional[int]
    Wear: Optional[int]
    ElevatedQuality: Optional[int]
    Target: Optional[int]
    CraftNum: Optional[int]
    CrateSn: Optional[int]
    Output: Optional[int]
    OutputQuality: Optional[int]

    def __init__(self, data: Optional[dict] = None):
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

        if data is not None:
            self.__dict__.update(data)

    def __str__(self) -> str:
        return dumps(self.__dict__)
