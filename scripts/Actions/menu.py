from bge.types import KX_Scene, KX_GameObject
import math

def callback(gameObject: any, scene: KX_Scene):
    items: dict = gameObject["menu"]["items"]

    render = scene.objects["RenderController"]
    count = 0
    PI_2 = math.pi*2
    itemsCount = len(items.keys())
    camera = scene.objects["Camera"]
    for key in items.keys():
        item: dict = items[key]

        position = [0, 0, 0]
        rotation = [0, 0, 0]
        properties = {}
        if "position" in item: position = item["position"]
        if "rotation" in item: rotation = item["rotation"]
        if "properties" in item: properties = item["properties"]

        object: KX_GameObject = scene.addObject(item["target"], camera)
        for prop in properties:
            object[prop] = properties[prop]

        render.objects.append(key)
        object.name = key

        object.applyRotation([0, 0, PI_2/itemsCount*count], True)
        object.applyMovement([0, 1.75, -0.1], True)
        object.setParent(gameObject)
        object.applyRotation([0, 0, -PI_2/itemsCount*count], True)

        count += 1

    background: KX_GameObject = scene.addObject("MenuBackground", camera)
    background.name = "MenuBackground.001"
    render.objects.append(background.name)
    background.localPosition.z -= 0.2