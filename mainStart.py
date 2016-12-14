from runSim import *
from generation import *
import sys
import pygame
from pygame.locals import *
import pymunk
from pymunk import pygame_util
import math
import circle

FINDJOINTS = False

def calcFitness(beams):
    score = 0
    for bbb in beams:
        adif = bbb.body.position.x - bbb.previousPosition[0]
        bdif = bbb.body.position.y - bbb.previousPosition[1]
        diff = int(abs(adif)+abs(bdif))
        score += 5 - diff
    return int(score)

def main():
    global FINDJOINTS

    RUNS = 20
    BEAMNUM = 15
    MUTATIONRATE = 7
    BRIDGE = False
    CIRCLE = False
    beamBoundYMinT = 100
    beamBoundYMaxT = 175
    beamBoundXMinT = 125
    beamBoundXMaxT = 175
    beamBoundYMinB = 150
    beamBoundYMaxB = 175
    beamBoundXMinB = 70
    beamBoundXMaxB = 235

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Building")
    clock = pygame.time.Clock()

    myfont = pygame.font.SysFont("monospace", 15)

    space = freshSpace(BRIDGE)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    beams = []
    beamInfo = []
    scores = []
    fitnessScore = 0
    movementScore = 0
    boxMovementScore = 0
    boxXScore = 0
    boxFallScore = 0
    boxHeightScore = 0
    fitnessScoreHistory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    paused = False
    oneframe = False
    squareLive = None

    timesRun = 0
    generation = 1
    for x in range(0, RUNS):
        if BRIDGE:
            beamInfo.append(
                genBeamsBridge(space, beamBoundXMinB, beamBoundXMaxB, beamBoundYMinB, beamBoundYMaxB, BEAMNUM))
        else:
            beamInfo.append(generateBeamsTower(space, beamBoundXMinT, beamBoundXMaxT, beamBoundYMinT, beamBoundYMaxT, BEAMNUM))
    beams = beamInfo[timesRun]
    addBeams(space, beams)
    ticks_to_next_beam = 200
    FINDJOINTS = True
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
                elif event.key == K_SPACE:
                    paused = not paused
                    if oneframe:
                        oneframe = False
                elif event.key == K_DOWN:
                    if paused:
                        oneframe = True
                        paused = False

        if paused:
            continue

        ticks_to_next_beam -= 1
        if ticks_to_next_beam <= 0:
            if fitnessScore < 0:
                fitnessScore = 0
            scores.append(fitnessScore)
            timesRun += 1
            if timesRun == RUNS:
                if CIRCLE:
                    with open('circleScores.txt', 'a') as the_file:
                        the_file.write('{0:1}. avg: {1:4} high:{2:4} low: {3:4}\n'
                                       .format(generation, int(sum(scores) / RUNS), max(scores), min(scores)))
                        with open('circleBest.txt', 'a') as the_file:
                            the_file.write(str(generation)+"----------------\n")
                            ms = scores.index(max(scores))
                            for bi in range(0, BEAMNUM):
                                the_file.write('beams.append(beam.beam({0}, {1}, {2}, {3}, {4}))\n'
                                               .format(beamInfo[ms][bi].beamID, beamInfo[ms][bi].startingPosition[0],
                                                       beamInfo[ms][bi].startingPosition[1],
                                                       beamInfo[ms][bi].angle, beamInfo[ms][bi].length))
                else:
                    with open('scores.txt', 'a') as the_file:
                        the_file.write('{0:1}. avg: {1:4} high:{2:4} low: {3:4}\n'
                                       .format(generation, int(sum(scores) / RUNS), max(scores), min(scores)))
                        with open('best.txt', 'a') as the_file:
                            the_file.write(str(generation)+"----------------\n")
                            ms = scores.index(max(scores))
                            for bi in range(0, BEAMNUM):
                                the_file.write('beams.append(beam.beam({0}, {1}, {2}, {3}, {4}))\n'
                                               .format(beamInfo[ms][bi].beamID, beamInfo[ms][bi].startingPosition[0],
                                                       beamInfo[ms][bi].startingPosition[1],
                                                       beamInfo[ms][bi].angle, beamInfo[ms][bi].length))
                tempBeam = newGeneration(scores, beamInfo)
                beamInfo = mutate(MUTATIONRATE, tempBeam)
                scores = []
                timesRun = 0
                generation += 1
                if generation == 30:
                    if CIRCLE:
                        with open('circleScores.txt', 'a') as the_file:
                            the_file.write('------------------------------------------------\n')
                        with open('circleBest.txt', 'a') as the_file:
                            the_file.write("------------------------------------------------\n")
                        CIRCLE = True
                    else:
                        with open('scores.txt', 'a') as the_file:
                            the_file.write('------------------------------------------------\n')
                        with open('best.txt', 'a') as the_file:
                            the_file.write("------------------------------------------------\n")
                        CIRCLE = False
                    beamInfo = []
                    for x in range(0, RUNS):
                        if BRIDGE:
                            beamInfo.append(
                                genBeamsBridge(space, beamBoundXMinB, beamBoundXMaxB, beamBoundYMinB, beamBoundYMaxB,
                                               BEAMNUM))
                        else:
                            beamInfo.append(generateBeamsTower(space, beamBoundXMinT, beamBoundXMaxT, beamBoundYMinT,
                                                               beamBoundYMaxT, BEAMNUM))
                    generation = 0
            space = freshSpace(BRIDGE)
            draw_options = pymunk.pygame_util.DrawOptions(screen)
            fitnessScore = 0
            movementScore = 0
            boxMovementScore = 0
            boxXScore = 0
            boxFallScore = 0
            boxHeightScore = 0
            fitnessScoreHistory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ticks_to_next_beam = 200
            beams = beamInfo[timesRun]
            addBeams(space, beams)
            FINDJOINTS = True
            squareLive = None
        if ticks_to_next_beam == 100:
            boxHeightScore = 100000000000000000000
            if CIRCLE:
                squareLive = circle.circle(300, 350, 30)
                space.add(squareLive.body, squareLive.shape)
            else:
                squareLive = addSquare(space, 250, 500, beams)

        space.step(1/50.0)
        if FINDJOINTS:
            jointNum = jointStart(beams, space)
            FINDJOINTS = False

        #----------
        # Calculate Fitness
        #----------

        fitnessScoreHistory.pop(0)
        fitnessScoreHistory.append(calcFitness(beams))
        movementScore = int(sum(fitnessScoreHistory)/10)

        if squareLive != None:
            if CIRCLE:
                tempScore = int(squareLive.body.position.y) - 100
            else:
                tempScore = int(600 - 200 + squareLive.body.position.y + 50)
            # This is so the lowest point is the score
            if tempScore < boxHeightScore:
                boxHeightScore = tempScore

        for bb in beams:
            bb.previousPosition = [bb.body.position.x, bb.body.position.y]

        fitnessScore = boxHeightScore


        #-------------

        screen.fill((255,255,255))
        space.debug_draw(draw_options)

        screen.blit(myfont.render("Countdown: " + str(ticks_to_next_beam), 1, (0, 0, 0)), (50, 10))
        screen.blit(myfont.render("Current Fitness: "+str(fitnessScore), 1, (0, 0, 0)), (50, 30))
        screen.blit(myfont.render("Generation " + str(generation), 1, (0, 0, 0)), (50, 50))
        for x in range(1, timesRun+1):
            screen.blit(myfont.render(str(x)+". " + str(scores[x-1]), 1, (0, 0, 0)), (50, 50 + x*20))

        pygame.display.flip()
        clock.tick(50)

        if oneframe:
            paused = True

if __name__ == "__main__":
    main()
