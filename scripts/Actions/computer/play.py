from bge.types import KX_Scene, KX_GameObject
import math

def callback(gameObject: KX_GameObject, scene: KX_Scene):
    from threading import Thread

    def increaseStatus():
        import time

        WAIT_TIME = 30

        status: KX_GameObject = scene.objects.get("Status")
        targetMood: dict = status.status["mood"]
        targetCalm: dict = status.status["calm"]
        config: KX_GameObject = scene.objects.get("Global")

        config["lock"] = True
        gameObject.parent.close()
        text: KX_GameObject = scene.objects.get("Texts")
        text.drawMessage(f"Plaing...", False, False, WAIT_TIME+1, 0.05)
        time.sleep(1)

        passTime = 0
        while passTime < WAIT_TIME:
            status.increase(targetMood, 0.04)
            status.increase(targetCalm, 0.08)
            passTime += 1
            time.sleep(1)
            if targetMood["value"] >= targetMood["max"] and targetCalm["value"] >= targetCalm["max"]: break

        config["lock"] = False
        pass

    t: Thread = Thread(target=increaseStatus, args=[])
    t.start()

    pass