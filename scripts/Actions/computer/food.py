from bge.types import KX_Scene, KX_GameObject
import math

def callback(gameObject: KX_GameObject, scene: KX_Scene):
    from threading import Thread


    def increaseStatus():
        import time
        from Text import TextDraw

        dt: TextDraw = scene.objects.get("Texts")

        WAIT_TIME = 40
        dt.drawMessage(f"Food will arrive in approximately {WAIT_TIME} minutes", True, False, 2, 0.1)

        renderController: KX_GameObject = scene.objects.get("RenderController")

        gameObject.parent.close()

        passTime = 0

        while passTime < WAIT_TIME:
            passTime += 1
            time.sleep(1)

        renderController.sceneMaps["City.MyHouseOut"]["pack.001"] = {
            "target": "Box",
            "position": [-0.5, 0.5, 0],
            "rotation": [0, 0, 0],
            "properties": {
                "action": "addItem",
                "item": "food",
                "quantity": 1,
                "ref": "City.MyHouseOut"
            }
        }

        if renderController.render == "City.MyHouseOut":
            renderController.draw()

        dt.drawMessage(f"iEat here!", True, False, 2, 0.1)

    t: Thread = Thread(target=increaseStatus, args=[])
    t.start()

    pass