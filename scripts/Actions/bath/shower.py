from bge.types import KX_Scene, KX_GameObject
import math

def callback(gameObject: KX_GameObject, scene: KX_Scene):
    from threading import Thread

    def increaseStatus():
        import time

        status: KX_GameObject = scene.objects.get("Status")
        target: dict = status.status["hygiene"]
        config: KX_GameObject = scene.objects.get("Global")

        config["lock"] = True
        time.sleep(1)
        gameObject.parent.close()
        while target["value"] < target["max"]:
            status.increase(target, 3.4)
            time.sleep(1)

        config["lock"] = False
        pass

    t: Thread = Thread(target=increaseStatus, args=[])
    t.start()

    pass