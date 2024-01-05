import pygame

class TextureCache:
    textures = {}

    def load(self, path, size):
        if path not in self.textures:
            s = pygame.image.load(path)
            s = pygame.transform.scale(s, size)
            self.textures[path] = s.convert_alpha()

        return self.textures[path]
     
