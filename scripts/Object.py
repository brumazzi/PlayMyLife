import bge, mathutils, math
from collections import OrderedDict

from bge.types import KX_GameObject, KX_Camera
from Decorators import ParamsToObjectVar
from Scene import Render

class Door(KX_GameObject):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args: dict = {
        "openRequired": ""
    }

    openRequired: str
    globalConfig: KX_GameObject

    @ParamsToObjectVar
    def start(self, args):
        self.globalConfig = self.scene.objects["Global"]
        pass

    def canOpen(self):
        if self.openRequired != "": return False
        return True

    def open(self):
        if not "open" in self or self["open"] == "":
            return None
        render: Render = self.scene.objects["RenderController"]
        render.render = self["open"]
        render.clear()
        render.draw()

    def update(self):
        pass

class Camera(KX_Camera):
    args: dict = {
        "target": "Character"
    }

    @ParamsToObjectVar
    def start(self, args):
        self["START_POSITION"] = self.worldPosition.to_tuple()
        self.target = self.scene.objects[self.target]
        pass

    def update(self):
        self.worldPosition.x = self["START_POSITION"][0] + self.target.worldPosition.x
        self.worldPosition.y = self["START_POSITION"][1] + self.target.worldPosition.y
        self.worldPosition.z = self["START_POSITION"][2] + self.target.worldPosition.z