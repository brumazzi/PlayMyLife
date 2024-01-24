from bge.types import KX_Scene, KX_GameObject
import math

def callback(gameObject: KX_GameObject, scene: KX_Scene):
    from threading import Thread
    from Text import TextDraw

    renderController: KX_GameObject = scene.objects.get("RenderController")
    renderController.sceneMaps[gameObject["ref"]][gameObject.name] = None

    dt: TextDraw = scene.objects.get("Texts")
    dt.drawMessage(f"Get pack", False, False, 2, 0.1)


    gameObject.endObject()

    pass