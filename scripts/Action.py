from __future__ import annotations

import bge, math, random, bpy
from bge.types import KX_GameObject, SCA_PythonController
from Decorators import ParamsToObjectVar
from Scene import Render


def Click(controller: SCA_PythonController):
    if bge.logic.KX_INPUT_JUST_ACTIVATED in bge.logic.mouse.inputs[bge.events.LEFTMOUSE].queue:
        if hasattr(controller.owner, "active"): controller.owner.active()
    pass

def CursorPointer(controller: SCA_PythonController):
    bpy.context.window.cursor_set("HAND")

def CursorArrow(controller: SCA_PythonController):
    bpy.context.window.cursor_set("DEFAULT")


class Action(KX_GameObject):
    args: dict = {}

    open: bool = False
    config: KX_GameObject

    @ParamsToObjectVar
    def start(self, args):
        self.config = self.scene.objects.get("Global")
        pass

    def active(self):
        if not "action" in self: return None
        if self.config["lock"]: return None
        if self["action"] == "menu": self.open = True

        filePath: str = f"{bpy.path.abspath('//')}scripts/Actions/{self['action']}.py"
        pyFile = open(filePath, "r")

        exec(pyFile.read())
        eval("callback(self, self.scene)")
        pyFile.close()

    def close(self):
        for item in self["menu"]["items"].keys():
            object = self.scene.objects.get(item)
            if object: object.endObject()
        pass
        if "MenuBackground.001" in self.scene.objects:
            self.scene.objects["MenuBackground.001"].endObject()
        self.open = False

    def update(self):
        if bge.logic.KX_INPUT_JUST_ACTIVATED in bge.logic.mouse.inputs[bge.events.RIGHTMOUSE].queue:
            if "action" in self and self["action"] == "menu" and self.open: self.close()
        pass