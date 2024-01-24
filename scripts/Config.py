from __future__ import annotations

import bge, bpy, aud, os
from bge.types import KX_GameObject, SCA_PythonController
from threading import Thread

# def setDelay(sensor: SCA_AlwaysSensor, delay: float):
#     fps: float = bpy.context.scene.render.fps * delay

#     if sensor.skippedTicks != fps or sensor.usePosPulseMode == False:
#         print(f"Setting {sensor} sensor to delay with {delay}s")
#         sensor.skippedTicks = int(fps)
#         sensor.usePosPulseMode = True
#         return True
#     return False
from Decorators import ParamsToObjectVar

class TimePass(KX_GameObject):
    args: dict = {
        "day": "01",
        "hour": "12",
        "minute": "00",
    }

    week_day: str
    day: str
    hour: str
    minute: str

    @ParamsToObjectVar
    def start(self, args: dict):
        self.week_day: str = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fry", "Sat"][(int(self.day)-1) % 7]

        def increaseTime(self: TimePass):
            import time
            while True:
                time.sleep(10)
                WEEK_DAYS: list = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fry", "Sat"]
                minute: int = int(self.minute) + 10
                if minute >= 60:
                    minute = 0
                    hour: int = int(self.hour) + 1
                    if hour >= 24:
                        hour = 0
                        day: int = int(self.day)
                        if day >= 28:
                            day = 0
                        self.week_day = WEEK_DAYS[day % 7]
                        self.day = str(day+1).rjust(2,"0")
                    self.hour = str(hour).rjust(2,"0")
                self.minute = str(minute).rjust(2,"0")
                pass

        t: Thread = Thread(target=increaseTime, args=[self])
        t.start()
        pass

    def run(self):
        pass

class Media(KX_GameObject):
    args: dict = {
        "audioPath": "Assets/Audios",
        "imagePath": "Assets/Images"
    }

    audioPath: str
    imagePath: str
    audioLib: dict = {}
    imageLib: dict = {}
    textureLib: dict = {}
    device: aud.Device

    @ParamsToObjectVar
    def start(self, args: dict):
        audioPath: str = f"{bpy.path.abspath('//')}{self.audioPath}"
        imagePath: str = f"{bpy.path.abspath('//')}{self.imagePath}"
        for file in os.listdir(audioPath):
            if file[-4:32] == ".ogg" or file[-4:32] == ".mp3":
                self.audioLib[file[0:-4]] = aud.Sound(f"{audioPath}/{file}")
                pass
        for file in os.listdir(imagePath):
            if file[-4:32] == ".png" or file[-4:32] == ".jpg" or file[-4:32] == ".bmp":
                self.imageLib[file[0:-4]] = bge.texture.ImageFFmpeg(f"{imagePath}/{file}")
                self.imageLib[file[0:-4]].filter = bge.texture.FilterNormal()
                pass
        self.device = aud.Device()

    def play(self, audio: str):
        if audio in self.audioLib:
            self.device.play(self.audioLib.get(audio))
            self.currentPlaying = audio
            return True
        return False

    def stop(self):
        pass


class Image(KX_GameObject):
    args: dict = {}

    media: Media

    @ParamsToObjectVar
    def start(self, args: dict):
        self.media = self.scene.objects.get("Media")
        self.changed = False

        pass

    def setFace(self, face: str):
        if face in self.media.imageLib:
            materialID = bge.texture.materialID(self, "MACharacterImage")
            if not face in self.media.textureLib:
                self.media.textureLib[face] = bge.texture.Texture(self, materialID, 0)

            self.media.textureLib[face].source = self.media.imageLib[face]
            self.media.textureLib[face].refresh(False)
        pass

    def update(self):
        # self.setFace("CharacterFear")
        pass

# def increaseTime(owner: KX_GameObject):
#     WEEK_DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fry", "Sat"]

#     minute: int = int(owner["minute"]) + 10
#     if minute >= 60:
#         minute = 0
#         hour: int = int(owner["hour"]) + 1
#         if hour >= 24:
#             hour = 0
#             day: int = int(owner["day"])
#             if day >= 28:
#                 day = 0
#             owner["week_day"] = WEEK_DAYS[day % 7]
#             owner["day"] = str(day+1).rjust(2,"0")
#         owner["hour"] = str(hour).rjust(2,"0")
#     owner["minute"] = str(minute).rjust(2,"0")
#     pass

# def UpdateStatusPosition(controller: SCA_PythonController):
#     SENSOR_DELAY = 0.2

#     if setDelay(controller.sensors["AlwaysStatusDraw"], SENSOR_DELAY): return None

#     owner: Player = controller.owner
#     owner.components["Draw"].calculateTextPosition()
#     owner.components["Draw"].ApplyProgressBarPosition()
#     pass

# def TimeCount(controller: SCA_PythonController):
#     SENSOR_DELAY = 1
#     if setDelay(controller.sensors["AlwaysTimeCount"], SENSOR_DELAY): return None

#     globalConfig: KX_GameObject = controller.owner.scene.objects["Global"]
#     currentTime: int = globalConfig["current_time"]

#     if currentTime == 0: increaseTime(controller.owner)

# def SpendGlobalTime(controller: SCA_PythonController):
#     SENSOR_DELAY = 1
#     if setDelay(controller.sensors["SpendGlobalTime"], SENSOR_DELAY): return None

#     owner: KX_GameObject = controller.owner

#     fixedTime: int = owner["delay_time"]

#     if owner["fast_pass"] and owner["skip"]:
#         owner["current_time"] = 0
#         return None

#     if owner["current_time"] <= 0:
#         owner["current_time"] = fixedTime
#         return None

#     owner["current_time"] -= 1

# def FollowCursor(controller: SCA_PythonController):
#     owner: KX_GameObject = controller.owner
#     mouse = controller.sensors["Mouse"]
#     #print(dir(mouse))
#     position = mouse.position
#     owner.localPosition.x = -8*100/position[0]
#     owner.localPosition.y = 4*100/position[1]
#     print(position)
#     print(owner.localPosition)

#def FollowCharacter(controller: SCA_PythonController):
#    owner: KX_Camera = controller.owner
#    if not "START_POSITION" in owner:
#        owner["START_POSITION"] = owner.worldPosition.to_tuple()

#    player: Player = owner.scene.objects["Character"]

#    owner.worldPosition.x = owner["START_POSITION"][0] + player.worldPosition.x
#    owner.worldPosition.y = owner["START_POSITION"][1] + player.worldPosition.y
#    owner.worldPosition.z = owner["START_POSITION"][2] + player.worldPosition.z
