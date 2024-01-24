from __future__ import annotations

import bge, math
from mathutils import Vector, Euler
from bge.types import KX_GameObject, SCA_PythonController, KX_Scene, KX_PythonComponent, KX_Camera

from Decorators import ParamsToObjectVar
from Config import Media

class Image(KX_GameObject):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args: dict = {}

    #media: Media

    @ParamsToObjectVar
    def start(self, args: dict):
        #self.media = self.scene.objects.get("Media")
        #print(self.media.imageLib)
        #self.setFace("Normal")
        pass

    #def setFace(self, face: str):
    #    textureID = bge.texture.materialID(self, "MACharacterImage")
    #    objTexture = bge.texture.Texture(self, textureID)

    #    bge.logic.texture[self.name] = objTexture
    #    bge.logic.texture[self.name].source = self.media.imageLib[face]
    #    bge.logic.texture[self.name].refresh(False)
    #    pass
