from PIL import Image, ImageFont, ImageDraw
import pygame as pg
import sys, random


class TextureManager:
    class TextureLoadError(Exception): pass

    textures: dict[object] = {}

    def __init__(self):
        pass

    def new(self, name: str, path: str):
        if self.textures.get(name, False):
            raise self.TextureLoadError(f"name texture {name} exists, path exists texture - {self.textures[name].path}")
        self.textures[name] = self.Texture(path=path, manager=self)
        return self.textures[name]

    def get(self, name: str):
        return self.textures.get(name, None)

    class Texture(object):
        img: object = None
        path: str = None
        manager: object = None

        def __init__(self, path: str, manager: object):
            self.img = Image.open(path)
            self.path = path
            self.manager = manager


class GameObject:
    childs: list
    name: str = "Undefined"
    texture: TextureManager.Texture = None
    z_index = 0
    deepth = 0

    def __init__(self, name: str, texture: TextureManager.Texture):
        self.childs = []
        self.texture = texture
        self.name = name

    def draw(self):
        if not self.childs:
            return self.texture.img

        for gameObject in self.childs:
            pass
        exit("Дядь, а это доделать, куда несколько объектов в клетку одну")


class Cell(object):
    objects: list[GameObject]
    size: int

    def __init__(self, size: int):
        self.objects = []
        self.size = size

    def AddGameObject(self, gameObject: GameObject):
        self.objects.append(gameObject)

    def draw(self):
        resultImg = Image.new("RGBA", (self.size, self.size), '#232529')
        for gameObject in self.objects:
            img = gameObject.draw()
            resultImg.paste(img, (0, 0, 64, 64))

        return resultImg


class Map(object):
    cells: list[list[Cell]]

    Scene: object = None
    sizeProperty: tuple[int, int, int, int] = None

    def __init__(self, size_x: int, size_y: int, size_cell: int,
                 defaultFill: TextureManager.Texture = None,
                 indent: int = 3,
                 listMap: list[list[Cell]] = None):
        self.cells = []
        self.sizeProperty = (size_x, size_y, size_cell, indent)

        for i in range(size_x):
            self.cells.append([])
            for j in range(size_y):
                cell = Cell(size_cell)
                if defaultFill: cell.AddGameObject(
                    GameObject("ground", texture=defaultFill)
                )
                self.cells[i].append(cell)

    def getCell(self, x, y):
        return self.cells[x][y]

    def draw(self):
        size_x, size_y, size_cell, indent = self.sizeProperty

        size = (size_x*size_cell + indent*size_x,
                size_y*size_cell + indent*size_y)
        startIndentX = 0
        sceneImg = Image.new("RGBA", size, '#232529')
        for i in range(len(self.cells)):
            startIndentY = 0
            for j in range(len(self.cells[i])):
                cell = self.cells[i][j]
                img = cell.draw()
                sceneImg.paste(img, (i*size_cell+startIndentX, j*size_cell+startIndentY))
                startIndentY += indent
            startIndentX += indent

        return sceneImg


if __name__ == "__main__":
    tm = TextureManager()
    defaultTexture = tm.new(name="grass64x", path="resources/textures/grass64.png")

    GameMap = Map(10, 10, 16*4, defaultFill=defaultTexture)

    imgGame = GameMap.draw()
    imgGame.save('img.png')
