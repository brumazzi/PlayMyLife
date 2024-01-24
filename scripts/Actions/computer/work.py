from bge.types import KX_Scene, KX_GameObject
import math

def callback(gameObject: KX_GameObject, scene: KX_Scene):
    from threading import Thread

    def decreaseStatus():
        import time

        WAIT_TIME = 60

        status: KX_GameObject = scene.objects.get("Status")
        targetWake: dict = status.status["wake"]
        targetMood: dict = status.status["mood"]
        targetCalm: dict = status.status["calm"]
        config: KX_GameObject = scene.objects.get("Global")

        config["lock"] = True
        gameObject.parent.close()
        text: KX_GameObject = scene.objects.get("Texts")
        text.drawMessage(f"Working...", False, False, WAIT_TIME+1, 0.05)
        time.sleep(1)

        passTime = 0
        while passTime < WAIT_TIME:
            status.decrease(targetMood, 0.64)
            status.decrease(targetCalm, 0.89)
            status.decrease(targetWake, 0.58)
            passTime += 1
            time.sleep(1)

        config["lock"] = False
        pass

    t: Thread = Thread(target=decreaseStatus, args=[])
    t.start()

    pass