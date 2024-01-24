from __future__ import annotations

from Character import Player

import time
from threading import Thread

import bge, math, random
from bge.types import KX_GameObject, KX_PythonComponent, KX_Camera, SCA_AlwaysSensor, KX_LightObject, SCA_PythonController
from Decorators import ParamsToObjectVar

from bge import events

# def OpenMenu(controller: SCA_PythonController):
#     if bge.logic.KX_INPUT_JUST_ACTIVATED in bge.logic.mouse.inputs[events.LEFTMOUSE].queue:
#         controller.owner.open()
#     pass

# class Menu(KX_GameObject):

#     args: dict = {}

#     distance: float
#     actionPoint: KX_GameObject
#     globalVars: KX_GameObject
#     actionItemComponents: list = []
#     actionItems: list[KX_GameObject] = []
#     itemTarget: int
#     itemPivot: KX_GameObject

#     @ParamsToObjectVar
#     def start(self, args: dict):
#         self.actionPoint = None
#         self.globalVars = self.scene.objects["Global"]
#         self["action_text"] = ""

#     def open(self):
#         self.continue_action = False
#         self.globalVars["opened_menu"] = self
#         self.globalVars["lock"] = True
#         self.itemTarget = 0

#         camera: KX_Camera = self.scene.objects["Camera"]

#         self.itemPivot = self.scene.addObject("Pivot", camera)
#         self.itemPivot.setParent(camera)
#         self.itemPivot.localPosition.z -= 1
#         componentCount: int = self.actionItemComponentsCount()
#         self.actionItemComponents.clear()

#         for index in range(len(self.components)):
#             component: Item = self.components[index]
#             if component.__class__ != Item: continue

#             self.actionItemComponents.append(component)
#             icon: str = component.icon.title().replace("_","")
#             item: KX_GameObject = self.scene.addObject(f"ActionIcon{icon}", self.itemPivot)

#             item.setParent(self.itemPivot)
#             item.applyRotation([0, 0, math.pi/componentCount*index*2], True)
#             item.applyMovement([0, 1, 0], True)
#             self.actionItems.append(item)
#         self.actionItems[self.itemTarget].scaling = [2,2,2]
#         pass

#     def actionItemComponentsCount(self):
#         count: int = 0
#         for component in self.components:
#             if type(component) == Item: count += 1
#         return count

#     def close(self):
#         for item in self.actionItems:
#             item.endObject()
#         self.itemPivot.endObject()

#         self.actionItems.clear()

#         self.globalVars["lock"] = False
#         self.globalVars["opened_menu"] = None
#         self.globalVars["action_target_string"] = ""
#         pass

#     def update(self):
#         pass
#         # TODO: pass keys actions to pivot
#         # if "opened_menu" in self.globalVars and self.globalVars["opened_menu"] and self.globalVars["opened_menu"].name == self.name:
#         #     import Character
#         #     player: Character.Player = self.scene.objects["Character"]

#         #     self.globalVars["action_target_string"] = self.actionItemComponents[self.itemTarget].text
#         #     if player.keyboard["Active"].eventRelease():
#         #         self.continue_action = True

#         #     if not self.continue_action: return None

#         #     if player.keyboard["MoveRight"].eventPress():
#         #         self.actionItems[self.itemTarget].scaling = [1,1,1]
#         #         self.itemPivot.applyRotation([0, 0, -2*math.pi/len(self.actionItemComponents)], True)
#         #         self.itemTarget = (1 + self.itemTarget) % len(self.actionItemComponents)
#         #         self.actionItems[self.itemTarget].scaling = [2,2,2]
#         #         pass
#         #     elif player.keyboard["MoveLeft"].eventPress():
#         #         self.actionItems[self.itemTarget].scaling = [1,1,1]
#         #         self.itemPivot.applyRotation([0, 0, 2*math.pi/len(self.actionItemComponents)], True)
#         #         self.itemTarget -= 1
#         #         if self.itemTarget < 0: self.itemTarget = len(self.actionItems) - 1
#         #         self.actionItems[self.itemTarget].scaling = [2,2,2]
#         #         pass
#         #     elif player.keyboard["Cancel"].eventPress():
#         #         self.close()
#         #         pass
#         #     elif player.keyboard["Active"].eventPress():
#         #         if self.components[self.itemTarget].active():
#         #             self.close()
#         #             pass
#         #         pass

#         #    self["action_text"] = self.components[self.itemTarget].text

# class ActionMove(KX_PythonComponent):
#     # Put your arguments here of the format ("key", default_value).
#     # These values are exposed to the UI.
#     args: dict = {
#         "moveSize": 0.5,
#         "baseUp": 1.0
#     }

#     @ParamsToObjectVar
#     def start(self, args):
#         pass

#     def update(self):
#         sin = math.sin(bge.logic.getFrameTime()) * self.moveSize
#         parentHeight:float = 0.0

#         if self.parent.__class__ is Menu:
#             parentHeight = self.parent.getDimension()

#         self.object.applyRotation([0, 0, 0.025], True)
#         self.object.localPosition.z = sin + self.baseUp + parentHeight + self.moveSize
#         pass

# ITEM_ACTIONS = {"work", "open",  "play_online", "play_offline", "chat", "see_video", "rest", "sleep", "buy_food", "buy_medicine", "go_bath", "go_shower"}
# class Item(KX_PythonComponent):
#     args: dict = {
#         "text": "",
#         "icon": "",
#         "action": ITEM_ACTIONS,
#         "minMinutes": 1,
#         "maxMinutes": 0,
#         "lock": True,
#         "stopOnFull": False,
#         "status": ""
#     }

#     text: str = ""
#     icon: str
#     action: str
#     minMinutes: int
#     maxMinutes: int
#     lock: bool = True
#     stopOnFull: bool = False
#     status: str = ""
#     globalConfig: KX_GameObject

#     @classmethod
#     def actions(self):
#         return ITEM_ACTIONS

#     @ParamsToObjectVar
#     def start(self, args: dict):
#         self.globalConfig: KX_GameObject = self.object.scene.objects["Global"]
#         pass

#     def work(self):
#         pass
#     def play_online(self):
#         pass
#     def play_offline(self):
#         pass
#     def chat(self):
#         pass
#     def see_video(self):
#         pass
#     def rest(self):
#         pass
#     def sleep(self):
#         pass
#     def buy_food(self):
#         pass
#     def buy_medicine(self):
#         pass
#     def go_bath(self):
#         pass
#     def go_shower(self):
#         pass

#     def active(self):
#         action = self.action.lower()
#         self.object["action_text"] = ""

#         self.__getattribute__(action)()

#         if self.lock:
#             self.globalConfig["skip"] = True

#             waitTime: int
#             if self.maxMinutes == 0:
#                 waitTime = self.minMinutes
#             else:
#                 waitTime = random.randint(self.minMinutes, self.maxMinutes)

#             # self.object.target.setStatus(action, waitTime, self.status)

#             # banner: KX_Camera = self.object.scene.addObject("Banner", "Camera", waitTime*60)
#             # banner.setParent(self.object.scene.objects["Camera"])
#             # banner.localPosition.z = -1
#         return True

#     def update(self):
#         pass
#     pass

class ActionArea(KX_GameObject):

    args: dict = {
        "name": "",
        "target": "",
        "visible": False
    }

    name: str
    target: KX_GameObject
    visible: bool
    globalConfig: KX_GameObject = None

    @ParamsToObjectVar
    def start(self, args: dict):
        # def cp
        pass

    def update(self):
        pass
