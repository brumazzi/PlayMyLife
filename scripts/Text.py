from __future__ import annotations

import bge, blf, bpy, os
import re
from bge.types import KX_GameObject, SCA_PythonController, KX_Scene, SCA_AlwaysSensor
from mathutils import Vector
from threading import Thread
import aud
from aud import Sound

class TextDraw(KX_GameObject):
    args: dict = {}

    textComponents: dict = {}
    textMessage: dict = {
        "block": True,
        "time": 0,
        "text": "",
        "finish": False,
        "position": [bge.render.getWindowWidth()/2, 36, 0]
    }

    letterSound: Sound
    media: KX_GameObject

    def start(self, args: dict):
        self.scene.post_draw.append(self.drawCallback)
        self.scene.post_draw.append(self.messageCallback)

        self.media = self.scene.objects.get("Media")
        pass

    def addText(self, alias: str, text: Text):
        if alias in self.textComponents and self.textComponents[alias]: return False

        self.textComponents[alias] = text
        return True

    def removeText(self, alias):
        if alias in self.textComponents and not self.textComponents[alias] is None:
            self.textComponents.pop(alias)
            return True
        return False

    def setMessagePosition(self, x: int, y: int):
        self.textMessage["position"] = [x, y, 0]

    def drawMessage(self, text: str, dynanic: bool = False, block: bool = False, sleepTime: int = 0, textDelay: int = 0.2, audio: bool = True):
        if not block and sleepTime == 0: sleepTime = 5

        self.textMessage["block"] = block
        self.textMessage["time"] = sleepTime
        self.textMessage["text"] = ""
        self.textMessage["finish"] = False
        self.textMessage["audio"] = audio

        if dynanic:
            def drawTextLetters(textMessage: dict, letters: str, delay: int):
                import time

                for letter in letters:
                    time.sleep(delay)
                    textMessage["text"] += letter
                    self.media.play("Letter")
                textMessage["finish"] = True
                pass
            t: Thread = Thread(target=drawTextLetters, args=[self.textMessage, text, textDelay])
            t.start()
            pass
        else:
            self.textMessage["text"] = text
            self.textMessage["finish"] = True
            if self.textMessage["audio"]: self.media.play("Letter")

        if sleepTime > 0:
            def destroyText(textMessage: dict, sleepTime: int):
                import time

                while not textMessage["finish"]:
                    time.sleep(0.1)

                time.sleep(sleepTime)
                textMessage["text"] = ""
            t: Thread = Thread(target=destroyText, args=[self.textMessage, sleepTime])
            t.start()

    def messageCallback(self):
        fontId = 0
        drawPosition = [self.textMessage["position"][0]-(len(self.textMessage["text"])*28/4), self.textMessage["position"][1], self.textMessage["position"][2]]
        blf.position(fontId, *drawPosition)
        blf.size(fontId, 28, 75)
        blf.color(fontId, 1, 1, 1, 1)
        blf.draw(fontId, self.textMessage["text"])
        pass

    def drawCallback(self):
        for key in self.textComponents:
            text: Text = self.textComponents[key]

            if not text.visible: continue

            blf.position(text.fontId, *text.statusTextPosition)
            blf.size(text.fontId, int(text.fontSizeDraw), 75)
            blf.color(text.fontId, *text.colorProcessed())
            blf.draw(text.fontId, text.textProcessed())
        pass

    def update(self):
        pass

class Text(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = {
        "name":         "",
        "cameraSize":   14.0,
        "text":         "",
        "position":     Vector(),
        "fontSize":     2.0,
        "visible":      True,
        "fontFamily":   "//fonts/RobotoMono-VariableFont_wght.ttf",
        "fontColor":    [1.0, 1.0, 1.0, 1.0],
        "checkString":  "",
        "colorIf":      [1.0, 1.0, 1.0, 1.0],
        "align": {"Left", "Center", "Right"}

    }
    cameraSize: float
    text: str
    position: Vector
    fontSize: float
    visible: bool
    fontFamily: str
    fontColor: list
    statusTextPosition: Vector
    fontSizeDraw: float
    fontId: int
    checkString: str
    colorIf: list
    align: str = "Left"

    def start(self, args):
        for key, value in args.items():
            self.__setattr__(key, value)

        fontPath: str = bpy.path.abspath(self.fontFamily)
        scene: KX_Scene = bge.logic.getCurrentScene()

        self.position = Vector(self.position)

        if os.path.exists(fontPath):
            self.fontId = blf.load(fontPath)

        self.install()

    def install(self):
        from threading import Thread

        def installTextCallback(text: Text):
            import time
            time.sleep(0.5)
            text.calculateTextPosition()

            scene: KX_Scene = bge.logic.getCurrentScene()
            textDraw: TextDraw = scene.objects["Texts"]
            textDraw.addText(text.name, text)
            pass

        t: Thread = Thread(target=installTextCallback, args=[self])
        t.start()

    def colorProcessed(self):
        strList: list[str] = self.checkString.split('|')
        if self.checkString == "": return self.fontColor

        for text in strList:
            if text in self.textProcessed():
                return self.colorIf
        return self.fontColor

    def textProcessed(self):
        props: list[str] = re.findall("\$\w+", self.text)
        props = list(dict.fromkeys(props))
        attrs: list[str] = re.findall("{[^}]+}", self.text)
        attrs = list(dict.fromkeys(attrs))
        object: any = self.object

        newText: str = self.text
        for prop in props:
            newText = newText.replace(prop, str(self.object[prop.replace("$", "")]))

        for attr in attrs:
            newText = newText.replace(attr, eval(attr.replace("{", "").replace("}", "")))
        return newText

    def update(self):
        pass

    def calculateTextPosition(self):
        windowWidth = bge.render.getWindowWidth()
        windowHeight = bge.render.getWindowHeight()
        camWidthSize = self.cameraSize
        camHeightSize = self.cameraSize/(windowWidth / windowHeight)
        windowWidthDivision = windowWidth / self.cameraSize
        windowHeightDivision = windowHeight / camHeightSize

        fontSize = (windowWidthDivision / camWidthSize * self.fontSize)

        positionX: float = windowWidthDivision * self.position.x
        positionY: float = (windowHeight - fontSize) - (self.position.y * windowHeightDivision)

        newPositionText: Vector = Vector()
        newPositionText.x = positionX
        newPositionText.y = positionY
        newPositionText.z = 0

        self.statusTextPosition = newPositionText
        self.fontSizeDraw = fontSize

        if self.align == "Right":
            newPositionText.x -= len(self.textProcessed()) * (fontSize/1.5)
        elif self.align == "Center":
            newPositionText.x -= (len(self.textProcessed())/2) * (fontSize/1.5)
