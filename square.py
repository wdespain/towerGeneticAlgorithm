import pymunk

class square:
    mass = 200
    moment = None
    body = None
    shape = None
    firstHit = False
    hitGround = False
    previousPosition = []

    def __init__(self, x, y):
        self.mass = 100
        self.previousPosition = [x, y]
        self.moment = pymunk.moment_for_poly(self.mass, [(x, y + 50), (x, y), (x + 50, y), (x + 50, y + 50)])
        self.body = pymunk.Body(self.mass, self.moment)
        self.shape = pymunk.Poly(self.body, [(x, y + 50), (x, y), (x + 50, y), (x + 50, y + 50)])
        self.shape.friction = 1
        self.shape.collision_type = 2