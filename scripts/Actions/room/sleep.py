from bge.types import KX_Scene, KX_GameObject
import math

def callback(gameObject: KX_GameObject, scene: KX_Scene):
    from threading import Thread

    def increaseStatus():
        import time

        status: KX_GameObject = scene.objects.get("Status")
        targetWake: dict = status.status["wake"]
        config: KX_GameObject = scene.objects.get("Global")
        text: KX_GameObject = scene.objects.get("Texts")

        if targetWake["value"] > 80.0:
            text.drawMessage(f"You can't sleep now!", False, False, 2, 0.05)
            return None

        gameObject.parent.close()

        config["lock"] = True
        text.drawMessage(f"Sleeping...", False, False, 1000, 0.05)
        time.sleep(1)

        while targetWake["value"] < targetWake["max"]:
            status.increase(targetWake, 0.07)
            time.sleep(1)

        config["lock"] = False
        text.drawMessage(f"", False, False, 1, 0.05, audio=False)
        pass

    t: Thread = Thread(target=increaseStatus, args=[])
    t.start()

    pass