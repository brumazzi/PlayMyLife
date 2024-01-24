def callback(gameObject, scene):
    render = scene.objects["RenderController"]
    render.render = gameObject["open"]
    render.draw()