from __future__ import annotations

import bge, bpy, blf, json

import time
from threading import Thread

from bge.types import KX_GameObject, SCA_PythonController, KX_Scene, KX_PythonComponent
from mathutils import Vector
from Decorators import ParamsToObjectVar

# BASE_STATUS_DECREASE = {
#     "healthDecrease":           0.0,
#     "satiateDecrease":          0.0,
#     "calmDecrease":             0.0,
#     "wakeDecrease":             0.0,
#     "moodDecrease":             0.0,
#     "hygieneDecrease":          0.0,
#     "bathDecrease":             0.0,
#     "sickNoneDecrease":         0.0,
#     "sickFluDecrease":          0.0,
#     "sickAnemiaDecrease":       0.0
# }

class Status(KX_GameObject):
    args: dict = {
        "statusFile": ""
    }

    statusFile: str
    status: dict = {}
    statusDecrease: dict = {}
    statusIncrease: dict = {}

    @ParamsToObjectVar
    def start(self, args):
        filePath: str = f"{bpy.path.abspath('//')}{self.statusFile}.json"
        jsonFile = open(filePath, "r")
        jsonDict = json.loads(jsonFile.read())
        jsonFile.close()

        if "status" in jsonDict: self.status = jsonDict["status"]
        if "statusDecrease" in jsonDict: self.statusDecrease = jsonDict["statusDecrease"]
        if "statusIncrease" in jsonDict: self.statusIncrease = jsonDict["statusIncrease"]

        config = self.scene.objects["Global"]
        for key in self.statusIncrease.keys():
            increase = self.statusIncrease[key]
            def update(object: Status, self: dict, config: KX_GameObject):
                if type(self["value"]) != float and type(self["value"]) != int: return None
                target: dict = object.status[self["target"]]
                status = object.status

                cursor = 0
                while True:
                    time.sleep(1)
                    if not config["started"]: continue

                    if cursor == config["_TimeLimit"]:
                        if "condition" in self:
                            if eval(self["condition"]): object.increase(target, self["value"])
                        else:
                            object.increase(target, self["value"])

                        cursor = 0
                    else:
                        cursor += 1
            t: Thread = Thread(target=update, args=[self, increase, config])
            t.start()

        for key in self.statusDecrease.keys():
            decrease = self.statusDecrease[key]
            def update(object: Status, self: dict, config: KX_GameObject):
                if type(self["value"]) != float and type(self["value"]) != int: return None
                target: dict = object.status[self["target"]]
                status = object.status

                cursor = 0
                while True:
                    time.sleep(1)
                    if not config["started"]: continue

                    if cursor == config["_TimeLimit"]:
                        if "condition" in self:
                            if eval(self["condition"]): object.decrease(target, self["value"])
                        else:
                            object.decrease(target, self["value"])

                        cursor = 0
                    else:
                        cursor += 1
            t: Thread = Thread(target=update, args=[self, decrease, config])
            t.start()
        pass

    def increase(self, target: dict, value: float):
        target["value"] += value
        if target["value"] >= target["max"]:
            target["value"] = target["max"]
            return True
        return False

    def decrease(self, target: dict, value: float):
        target["value"] -= value
        if target["value"] <= target["min"]:
            target["value"] = target["min"]
            return True
        return False

    def set(self, target: dict, value: str|bool):
        if type(target["value"]) == type(value):
            target["value"] = value
            return True
        return False

    def update(self):
        pass

#class Draw(KX_PythonComponent):
#    # Put your arguments here of the format ("key", default_value).
#    # These values are exposed to the UI.
#    args: dict = {
#        "position":     Vector(),
#        "visible":      True,
#        "fontFamily":   "//fonts/RobotoMono-VariableFont_wght.ttf",
#        "fontSize":     16.0,
#        "fontColor":    ["r", "g", "b", "a"],
#        "cameraSize":   1.0,
#    }
#    windowWidth: float
#    windowHeight: float
#    fontSizeDraw: float
#    position: Vector
#    visible: bool
#    fontFamily: str
#    fontSize: int
#    fontColor: list
#    cameraSize: float
#    fontId: int = 0
#    statusTextPosition: list = []
#    statusProgressPosition: list = []
#    progressBars: list = []
#    globalVars: KX_GameObject
#    scene: KX_Scene

#    @ParamsToObjectVar
#    def start(self, args):

#        self.scene = bge.logic.getCurrentScene()

#        self.globalVars = self.scene.objects["Global"]
#        for status in self.object.status:
#            newBar: KX_GameObject = self.scene.addObject("ProgressBar", "Camera", 0)
#            newBar.name = f"StatusBar{status.capitalize()}"
#            newBar["status"] = status
#            newBar.setParent(self.scene.objects["Camera"])
#            self.progressBars.append(newBar)

#        self.position = Vector(self.position)
#        self.calculateTextPosition()

#        fontPath: str = bpy.path.abspath(self.fontFamily)
#        import os
#        if os.path.exists(fontPath):
#            self.fontId = blf.load(fontPath)

#        def drawCallback():
#            if not self.visible or self.globalVars["opened_menu"].__class__ == KX_GameObject: return None

#            status: list = self.object.status
#            for index in range(len(status)):
#                text: str = status[index].capitalize()

#                blf.position(self.fontId, *self.statusTextPosition[index])
#                blf.size(self.fontId, int(self.fontSizeDraw), 75)
#                blf.color(self.fontId, *self.fontColor)
#                blf.draw(self.fontId, text)
#            pass

#        self.scene.post_draw.append(drawCallback)

#    def calculateTextPosition(self):

#        statusTextPosition: list = []
#        statusProgressPosition: list = []
#        windowWidth = bge.render.getWindowWidth()
#        windowHeight = bge.render.getWindowHeight()
#        camWidthSize = self.cameraSize
#        camHeightSize = self.cameraSize/(windowWidth / windowHeight)
#        windowWidthDivision = windowWidth / self.cameraSize
#        windowHeightDivision = windowHeight / camHeightSize

#        fontSize = (windowWidthDivision / camWidthSize * self.fontSize)

#        positionX: float = windowWidthDivision * self.position[0]
#        positionY: float = (windowHeight - fontSize) - (self.position[1] * windowHeightDivision)

#        positionPX: float = -(camWidthSize/2)
#        positionPY: float = (camHeightSize/2)

#        for index in range(len(self.object.status)):
#            newPositionText: Vector = Vector()
#            newPositionText.x = positionX
#            newPositionText.y = positionY - index*(fontSize*2.1)
#            newPositionText.z = 0
#            statusTextPosition.append(newPositionText)

#            newPositionProgress: Vector = Vector()
#            newPositionProgress.x = positionPX + self.position[0]
#            newPositionProgress.y = (positionPY - self.position[1]) - 0.3*index - .2
#            newPositionProgress.z = -1
#            statusProgressPosition.append(newPositionProgress)
#        self.statusProgressPosition = statusProgressPosition
#        self.statusTextPosition = statusTextPosition
#        self.fontSizeDraw = fontSize

#    def update(self):
#        pass

#    def ApplyProgressBarPosition(self):
#        # TODO: Change progresse bar to characters
#        object: KX_GameObject = self.object
#        for index in range(len(self.progressBars)):
#            progressBar: KX_GameObject = self.progressBars[index]
#            if self.globalVars["opened_menu"].__class__ == KX_GameObject:
#                if progressBar.visible: progressBar.visible = False
#            else:
#                if not progressBar.visible: progressBar.visible = True
#            if progressBar.localPosition.x != self.statusProgressPosition[index].x or progressBar.localPosition.y != self.statusProgressPosition[index].y:
#                progressBar.localPosition = self.statusProgressPosition[index]
#            barSize: float = object.__getattribute__(progressBar["status"])/100.0
#            if round(progressBar.localScale.x, 4) != round(barSize, 4):
#                progressBar.localScale.x = barSize
#        pass