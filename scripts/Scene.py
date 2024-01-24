from __future__ import annotations

import bge, mathutils, math, json, bpy
from os import listdir, path
from bge.types import KX_Scene, KX_GameObject
from Decorators import ParamsToObjectVar

class Render(bge.types.KX_GameObject):
    args = {
        "title": "",
        "render": ""
    }

    title: str
    render: str
    target: str
    visible: bool
    objects: list = []
    sceneMaps: dict = {}

    @ParamsToObjectVar
    def start(self, args):
        sceneMapPath: str = f"{bpy.path.abspath('//')}Assets/Scenes"

        for file in listdir(sceneMapPath):
            if path.isdir(f"{sceneMapPath}/{file}"):
                self.getJsonRecursive(self.sceneMaps, sceneMapPath, file)

        self.draw()
        pass

    def getJsonRecursive(self, jsonDict: dict, basePath: str, subPath: str):
        for file in listdir(f"{basePath}/{subPath.replace('.', '/')}"):
            if path.isdir(file):
                self.getJsonRecursive(basePath, f"{subPath}.{file}")
            else:
                jsonFile = open(f"{basePath}/{subPath.replace('.','/')}/{file}")
                jsonDict[f"{subPath}.{file[0:-5]}"] = json.loads(jsonFile.read())
                jsonFile.close()
        pass

    def addObject(self, target: str, name: str, position: list, rotation: list, properties: dict):
        object: KX_GameObject = self.scene.addObject(target, None)
        object.name = name
        if len(position) == 3: object.position = position
        if len(rotation) == 3: object.orientation = mathutils.Euler(rotation)

        for key in properties:
            object[key] = properties[key]

        self.objects.append(name)
        return object

    def draw(self):
        dictObject = self.sceneMaps.get(self.render)

        self.clear()
        for key in dictObject.keys():
            item = dictObject.get(key)

            position = [0, 0, 0]
            rotation = [0, 0, 0]
            properties = {}
            if "position" in item: position = item["position"]
            if "rotation" in item: rotation = item["rotation"]
            if "properties" in item: properties = item["properties"]

            self.addObject(item["target"], key, position, rotation, properties)
        pass

    def clear(self):
        for object in self.objects:
            if object in self.scene.objects: self.scene.objects[object].endObject()
        self.objects.clear()

    def update(self):
        pass