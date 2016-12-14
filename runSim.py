from beam import *
from square import *
import random
import pymunk
import math

def addStaticLine(space, bridge):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    line = pymunk.Segment(body, (0, 100), (600, 100), 5)
    line.friction = 1
    line.collision_type = 3
    space.add(line)
    if bridge == True:
        body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
        line2 = pymunk.Segment(body2, (150, 100), (150, 200), 5)
        line2.friction = 1
        line2.collision_type = 3
        space.add(line2)
        body3 = pymunk.Body(body_type=pymunk.Body.STATIC)
        line3 = pymunk.Segment(body3, (450, 100), (450, 200), 5)
        line3.friction = 1
        line3.collision_type = 3
        space.add(line3)
    else:

        body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
        line2 = pymunk.Segment(body2, (225, 100), (225, 200), 5)
        line2.friction = 1
        line2.collision_type = 3
        space.add(line2)
        body3 = pymunk.Body(body_type=pymunk.Body.STATIC)
        line3 = pymunk.Segment(body3, (375, 100), (375, 200), 5)
        line3.friction = 1
        line3.collision_type = 3
        space.add(line3)

def freshSpace(bridge):
    space = pymunk.Space()
    space.add_collision_handler(1, 1)
    space.gravity = (0.0, -700.0)
    addStaticLine(space, bridge)
    return space

def findJoints(space, beams, numBeams):
    foundJoint = False
    for bn in range(0, numBeams):
        bsx = int(beams[bn].body.position.x)
        bex = int(bsx + (math.cos(beams[bn].angle) * beams[bn].length))
        for bbn in range(bn+1, numBeams):
            if bn == bbn:
                continue
            bbsx = int(beams[bbn].body.position.x)
            bbex = int(bbsx + (math.cos(beams[bbn].angle) * beams[bbn].length))
            for bnx in range(bsx, bex):
                for bbnx in range(bbsx, bbex):
                    if bnx == bbnx:
                        bsy = int(beams[bn].body.position.y)
                        bey = int(bsy + (math.sin(beams[bn].angle) * beams[bn].length))
                        bbsy = int(beams[bbn].body.position.y)
                        bbey = int(bbsy + (math.sin(beams[bbn].angle) * beams[bbn].length))
                        for bny in range(bey, bsy):
                            for bbny in range(bbey, bbsy):
                                if bny == bbny:
                                    space.add(pymunk.PinJoint(beams[bn].body, beams[bbn].body, (bnx, bny), (bnx, bny)))
                                    foundJoint = True
                                    break
                            if foundJoint:
                                break
                    if foundJoint:
                        break
                if foundJoint:
                    break
            if foundJoint:
                continue

JOINTSCORE = 0

def jointStart(beams, space):
    global JOINTSCORE

    JOINTSCORE = 0

    for b in beams:
        b.body.each_arbiter(findJoint, space)

    return JOINTSCORE

def findJoint(arbiter, space):
    global JOINTSCORE

    if arbiter.is_first_contact:
        s1, s2 = arbiter.shapes
        if s1.collision_type!=1 or s2.collision_type!=1:
            return
        JOINTSCORE += 1
        v = pymunk.PinJoint(
            s1.body,
            s2.body,
            (
            arbiter.contact_point_set.points[0].point_a[0] / 2, arbiter.contact_point_set.points[0].point_a[1] / 2),
            (
            arbiter.contact_point_set.points[0].point_b[0] / 2, arbiter.contact_point_set.points[0].point_b[1] / 2))
        space.add(v)

def sortBeams(beams):
    if len(beams) == 1:
        return beams
    elif len(beams) == 2:
        if beams[0].startingPosition[0] > beams[1].startingPosition[0]:
            temp = beams[0]
            beams[0] = beams[1]
            beams[1] = temp
            return beams

    beamsr = sortBeams(beams[:int(len(beams)/2)])
    beamsl = sortBeams(beams[int(len(beams) / 2):])

    sortedBeams = []
    br = bl = 0
    while len(sortedBeams) < len(beams):
        if br >= len(beamsr):
            sortedBeams.append(beamsl[bl])
            bl += 1
        elif bl >= len(beamsl):
            sortedBeams.append(beamsr[br])
            br += 1
        elif beamsr[br].startingPosition[0] <= beamsl[bl].startingPosition[0]:
            sortedBeams.append(beamsr[br])
            br+=1
        else:
            sortedBeams.append(beamsl[bl])
            bl += 1

    return sortedBeams

def genBeamsBridge(space, xMin, xMax, yMin, yMax, numBeams):
    random.seed()

    beams = []
    beams.append(beam(0, xMin-30, random.randint(yMin, yMax), random.randint(0, 0), 60))
    for i in range(1, 8):
        xEnd = int(beams[i - 1].startingPosition[0] + (math.cos(beams[i - 1].angle) * (beams[i - 1].length))) - 30
        yEnd = int(beams[i - 1].startingPosition[1] + (math.sin(beams[i - 1].angle) * (beams[i - 1].length)))
        beams.append(beam(i, xEnd, yEnd,
                          0,
                          60))
    for i in range(8, numBeams):
        xEnd = random.randint(xMin, xMax)
        yEnd = random.randint(yMin, yMax)
        beams.append(beam(i, xEnd, yEnd,
                          random.randint(0, 45),
                          60))

    return sortBeams(beams)

def generateBeamsTower(space, xMin, xMax, yMin, yMax, numBeams):
    random.seed()

    beams = []
    for i in range(0, numBeams):
        beams.append(beam(i, random.randint(xMin, xMax), random.randint(yMin, yMax),
                          random.randint(0, 45),
                          60))

    return sortBeams(beams)

def addBeams(space, beams):
    for i in range(0, len(beams)):
        space.add(beams[i].body, beams[i].shape)

def firstHit(arbiter, space, data):
    if not data["square"].firstHit:
        data["square"].firstHit = True

def hitGround(arbiter, space, data):
    if not data["square"].hitGround:
        data["square"].hitGround = True

def addSquare(space, x, y, beams):
    s = square(x, y)
    space.add(s.body, s.shape)

    handler = space.add_collision_handler(1, 2)
    handler.data["square"] = s
    handler.post_solve = firstHit

    handler = space.add_collision_handler(2, 3)
    handler.data["square"] = s
    handler.post_solve = hitGround

    return s
