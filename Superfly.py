####Superfly
##################
import math, random, matplotlib, numpy, pylab

class Grid(object):
    def __init__(self, width, height, humnum, health, mosnum, ninfected, loss):
        self.width = width
        self.height = height
        size = width*height
        self.tileNumberList = range(size)
        humanList = []
        mosquitoList = []
        self.health = health
        randList = random.sample(self.tileNumberList, humnum)
        self.loss = loss
        for i in range(humnum):
            humanList.append(Human(randList[i], health, 0, self.loss, 0))
        randList2 = random.sample(self.tileNumberList, mosnum+ninfected)

        for j in range(mosnum):
            mosquitoList.append(Mosquito(randList2[j], 0, self.width, self.height))
        for k in range(ninfected):
            mosquitoList.append(Mosquito(randList2[mosnum-ninfected+k], 1, self.width, self.height))

        self.humanList = humanList
        self.mosquitoList = mosquitoList
        self.humanPosList = []
        for human in humanList:
            self.humanPosList.append(human.position)

        self.freeList = self.tileNumberList
        for i in self.tileNumberList:
            if i in self.humanPosList:
                self.freeList.remove(i)

        self.infectedMos = ninfected
        self.uninfectedMos = mosnum
        self.infectedHuman = 0
        self.uninfectedHuman = len(humanList)
        self.immuneHuman = 0
        self.deaths = 0
        
    def randomPosition(self):
        return random.choice(self.freeList)

    def randomMosPosition(self):
        return random.choice(self.tileNumberList)

    def update(self):
        infectedHuman = 0
        uninfectedHuman = 0
        for human in self.humanList:
            if human.sick == 1:
                infectedHuman +=1
            else:
                uninfectedHuman +=1
            human.update()
            if human.die():
                index = self.humanList.index(human)
                self.freeList.append(human.position)
                self.humanList.remove(human)
                # Probability 0.05 to mutate
                if random.random() < 0.05:
                    immune = 1-human.immune
                else:
                    immune = human.immune
                self.immuneHuman += immune-human.immune
                # Probability 0.5 to get or lose net
                if random.random() < 0.5:
                    net = 1-human.net
                else:
                    net = human.net
                newHuman = Human(self.randomPosition(), self.health, net,
                                 self.loss, immune)
                self.humanList.append(newHuman)
                self.freeList.remove(newHuman.position)
                self.deaths += 1
                if human.sick == 1:
                    self.infectedHuman -= 1
                    self.uninfectedHuman += 1
##            print human.position == self.humanPosList[self.humanList.index(human)]
##        print "Human", infectedHuman, uninfectedHuman

        infectedMos = 0
        uninfectedMos = 0
        for mosquito in self.mosquitoList:
            if mosquito.infected == 1:
                infectedMos +=1
            else:
                uninfectedMos +=1
            mosquito.update()
            if mosquito.die():
                self.mosquitoList.remove(mosquito)
                if mosquito.infected == 1:
                    self.infectedMos -= 1
                    self.uninfectedMos += 1
                newMos = Mosquito(self.randomMosPosition(), 0, self.width, self.height)
                self.mosquitoList.append(newMos)

            else:
                mosquito.fly()
                if mosquito.hungry() and (mosquito.position in self.humanPosList):
                        humanIndex = self.humanPosList.index(mosquito.position)
                        human = self.humanList[humanIndex]
                        if human.net*0.5 < random.random():
                            mosquito.bite()
                            if human.immune != 1:
                                if mosquito.infected == 1:
                                    if human.sick == 0:
                                        human.getSick()
                                        self.infectedHuman += 1
                                        self.uninfectedHuman -= 1
                                elif human.sick == 1:
                                        mosquito.getInfected()
                                        self.infectedMos += 1
                                        self.uninfectedMos -= 1
##        print "Mos", infectedMos, uninfectedMos, len(self.mosquitoList)

        return self.infectedMos, self.uninfectedMos, self.infectedHuman, \
                self.uninfectedHuman, self.immuneHuman, self.deaths




class Human(object):    
    def __init__(self, position, health, net, loss, immune):
        self.position = position
        self.health = health
        self.net = net
        #Sickness: 0=healthy, 1=sick
        self.sick = 0
        self.immune = immune
        self.loss = loss

    def updateHealth(self, delta):
        self.health = self.healt - delta

    def getSick(self):
        self.sick = 1
        loss = random.random()*5+10
        self.loss = loss

    def getImmune(self):
        self.immune = 1

    def update(self):
        self.health = self.health - self.loss

    def die(self):
        if self.health < 0:
            return True

    def buyNet(self):
        self.net = 1


class Mosquito(object):
    def __init__(self, position, infected, width, height):
        self.position = position
        self.infected = infected
        self.daysnoteaten = 0
        self.age = 0
        self.width = width
        self.height = height

    def getInfected(self):
        self.infected = 1

    def update(self):
        self.daysnoteaten += 1
        self.age += 1

    def hungry(self):
        if self.daysnoteaten > 2:
            return True

    def bite(self):
        self.daysnoteaten = 0

    def offGrid(self, index):
        x, y = self.getTile(index)
        if x < 0:
            x = x + self.width
        elif x > self.width:
            x = x - self.width
        if y > self.height:
            y = y - self.height
        elif y < 0:
            y = y + self.height
        return self.tileToIndex((x,y))

    def getTile(self, index):
        y = 0
        while (index >= self.width):
            index = index - self.width
            y += 1
        x = index
        return (x,y)

    def tileToIndex(self, tile):
        x, y = tile
        return x + self.width*y

    def fly(self):
        index = self.position
        newPos = random.choice([self.position+1, self.position-1,
                       self.position + self.width,
                       self.position - self.width,
                       self.position + self.width + 1,
                       self.position + self.width - 1,
                       self.position - self.width + 1,
                       self.position - self.width - 1])
        self.position = self.offGrid(newPos)

    def die(self):
        if self.age == 15:
            return True

    
def runSim(duration, width, height, humnum, health, mosnum, ninfected, loss):
    grid = Grid(width, height, humnum, health, mosnum, ninfected, loss)
##    print grid.humanList[1].position
##    print grid.getTile(grid.humanList[1].position)
##    for i in range(grid.width*grid.height):
##        print grid.getTile(i)

    infectedMosList = []
    uninfectedMosList = []
    infectedHumanList = []
    uninfectedHumanList = []
    immuneHumanList = []
    deathList = []
    timeList = []
    
    for time in range(duration):
        infectedMos, uninfectedMos, infectedHuman, \
                uninfectedHuman, immuneHuman, deaths = grid.update()
        
        infectedMosList.append(infectedMos)
        uninfectedMosList.append(uninfectedMos)
        infectedHumanList.append(infectedHuman)
        uninfectedHumanList.append(uninfectedHuman)
        immuneHumanList.append(immuneHuman)
        deathList.append(deaths)
        timeList.append(time)
    print True
        
        
##        print grid.mosquitoList[0].position
##        print grid.mosquitoList[0].getTile(grid.mosquitoList[0].position)
    fig = pylab.figure()
    fig.add_subplot(211)
    pylab.plot(timeList, deathList)
    pylab.ylabel('Number of deaths')
    
    fig.add_subplot(212)
    pylab.plot(timeList, infectedMosList, label = 'Infected Mosquitos')
    pylab.plot(timeList, uninfectedMosList, label = 'Uninfected Mosquitos')
    pylab.plot(timeList, infectedHumanList, label = 'Infected Humans')
    pylab.plot(timeList, uninfectedHumanList, label = 'Uninfected Humans')
    pylab.plot(timeList, immuneHumanList, label = 'Number of immune Humans')
    title = 'Start: Human=' + str(humnum) + ' Mosquitos= ' + str(mosnum) + \
            'Infected Mosquitos=' + str(ninfected) + 'Size= ' + str(width) + \
            '*' + str(height) +' Health= ' + str(health) 
    pylab.title(title) 
    pylab.ylabel('Numbers') 
    pylab.xlabel('Time steps')
    pylab.legend(loc='upper center', bbox_to_anchor=(0.6, -0.005),
                     fancybox=True, shadow=True, ncol=3)
    pylab.show()

runSim(duration = 1000, width = 50, height = 50, humnum = 500, health = 1000,
       mosnum = 200, ninfected = 50, loss = 1)
