from bge.types import KX_Scene, KX_GameObject
import math

def callback(gameObject: KX_GameObject, scene: KX_Scene):
    from threading import Thread

    def increaseStatus():
        import time

        WAIT_TIME = 30

        status: KX_GameObject = scene.objects.get("Status")
        target: dict = status.status["mood"]
        config: KX_GameObject = scene.objects.get("Global")

        config["lock"] = True
        gameObject.parent.close()
        text: KX_GameObject = scene.objects.get("Texts")
        text.drawMessage(f"Chating...", False, False, WAIT_TIME+1, 0.05)
        time.sleep(1)

        passTime = 0
        while passTime < WAIT_TIME:
            status.increase(target, 0.07)
            passTime += 1
            time.sleep(1)
            if target["value"] >= target["max"]: break

        config["lock"] = False
        pass

    t: Thread = Thread(target=increaseStatus, args=[])
    t.start()

    pass