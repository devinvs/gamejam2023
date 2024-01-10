import pygame

class TextureCache:
    textures = {}

    def load(self, path, size):
        if path not in self.textures:
            s = pygame.image.load(path).convert_alpha()
            s = pygame.transform.smoothscale(s, size)
            self.textures[path] = s

        return self.textures[path]
     
