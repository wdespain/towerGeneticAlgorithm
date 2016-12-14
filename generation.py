import random
import beam

def findPlace(choice, probs):
    for pb in range(0, len(probs)):
        if choice >= probs[pb][0]:
            if choice <= probs[pb][1]:
                return pb
    return -1

def newGeneration(sc, bI):
    if len(sc) != len(bI):
        return None
    numGroups = len(sc)
    numBeams = len(bI[0])
    p = []
    total = sum(sc)
    for x in range(0, numGroups):
        prob = int((sc[x]/total)*100)
        p.append(prob)
    probability = []
    past = 0
    for x in range(0, numGroups):
        probability.append([past, past+p[x]])
        past += p[x] + 1
    newBeamInfo = []
    for x in range(0, numGroups):
        newBeams=[]
        parent1 = findPlace(random.randint(0, 100), probability)
        parent2 = parent1
        while parent2 == parent1:
            parent2 = findPlace(random.randint(0, 100), probability)
        point1 = random.randint(0, numBeams-2)
        point2 = random.randint(point1+1, numBeams-1)
        for y in range(0, point1+1):
            newBeams.append(beam.beam(bI[parent1][y].beamID, bI[parent1][y].startingPosition[0],
                                      bI[parent1][y].startingPosition[1],
                                      bI[parent1][y].angle,
                                      bI[parent1][y].length))
        for y in range(point1+1, point2+1):
            newBeams.append(beam.beam(bI[parent2][y].beamID, bI[parent2][y].startingPosition[0],
                                      bI[parent2][y].startingPosition[1],
                                      bI[parent2][y].angle,
                                      bI[parent2][y].length))
        for y in range(point2+1, numBeams):
            newBeams.append(beam.beam(bI[parent1][y].beamID, bI[parent1][y].startingPosition[0],
                                      bI[parent1][y].startingPosition[1],
                                      bI[parent1][y].angle,
                                      bI[parent1][y].length))
        newBeamInfo.append(newBeams)
    return newBeamInfo

def mutate(rate, beamI):
    mutated = 0
    for x in range(0, len(beamI)-1):
        #implement adding beams?
        if x >= len(beamI[0]) or x<0:
            break
        for y in range(0, len(beamI[0])-1):
            if y>= len(beamI[0]) or y<0:
                continue
            mute = random.randint(0, 100)
            if mute <= rate:
                mutated += 1
                #print(str(x)+", "+str(y))
                kind = random.randint(0, 90)
                try:
                    BEAMID = beamI[x][y].beamID
                    BEAMX = beamI[x][y].startingPosition[0]
                    BEAMY = beamI[x][y].startingPosition[1]
                    BEAMANGLE = beamI[x][y].angle
                    BEAMLENGTH = beamI[x][y].length
                except:
                    continue
                if kind <= 30:
                    BEAMANGLE = random.randint(0, 90)
                elif kind <= 90:
                    BEAMX += random.randint(-30, 30)
                    BEAMY += random.randint(-30, 30)
                elif kind <= 60:
                    BEAMLENGTH = BEAMLENGTH + random.randint(-20, 20)
                beamI[x][y] = beam.beam(BEAMID, BEAMX, BEAMY, BEAMANGLE, BEAMLENGTH)
    return beamI