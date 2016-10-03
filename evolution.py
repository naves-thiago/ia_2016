from random import randint, uniform
from math import floor

candyAp = [1.1, 1.2, 1.3, 1.4, 1.5];
glade = [150, 140, 130, 120, 110, 100, 95, 90, 85, 80];
numPop = 100;
maxGen = 500;
bestGen = 0
mRate = 0
population = [];
parent1 = None;
parent2 = None;

class Ind:
    def __init__(self):
        self.values = [[0 for j in range(len(candyAp))] for i in range(len(glade))]
        self.totalCost = 0
    
    def rand(self):
        candy = [5]*len(candyAp)
        rand = 0
        for i in range(0, len(glade)):
            for j in range (0, len(candyAp)):
                rand = randint(0, 1)
                if (rand and candy[j] > 0):
                    self.values[i][j] = rand
                    candy[j] -= rand
                
    def validate(self):
        self.numCandy = 0;
        usedInLine = 0;
        self.used = [0]*len(candyAp);
        for i in range (0, len(glade)):
            usedInLine = 0
            for j in range (0, len(candyAp)):
                if (self.values[i][j] < 0 or self.values[i][j] > 1):
                    return False
                self.used[j] += self.values[i][j]
                usedInLine += self.values[i][j]
                self.numCandy += self.values[i][j]
                if (self.used[j] > 5 or self.numCandy > 24):
                    return False
            if (usedInLine == 0): #Pelo menos um doce deve ser deixado na clareira
                return False
        return True
        
    def lineCost(self, line):
        fit = 0;
        ap = 0;
        for i in range (0, len(candyAp)):
            ap += candyAp[i] * self.values[line][i]
        fit = glade[line]/ap
        return fit

    def calcFit(self):
        self.costs = []
        
        for i in range (0, len(glade)):
            line = self.lineCost(i)
            self.totalCost += line
            self.costs.append(line)
        
        self.fitness = 1000 - self.totalCost
        return self.costs
        
def initPop():
    while (len(population) < numPop):
        ind = Ind()
        ind.rand()
        if (ind.validate()):
            ind.calcFit()
            population.append(ind)

def selectInd(group):
    ind = None
    totalFit = sum(ind.fitness for ind in group)
    weights = []

    for i in range (0, len(group)):
        weights.append(group[i].fitness/totalFit)
    
    rand = uniform(0, 1)
    
    i = 0
    sumOfWeights = weights[i]
    while (rand > sumOfWeights):
        i += 1
        sumOfWeights += weights[i]
    ind = group[i]

    return (ind)
        
def crossOver(a, b):
    f1 = Ind()
    f2 = Ind()
    corte = randint(1, len(candyAp)*len(glade) - 1)
    corteX = corte % len(candyAp)
    corteY = floor(corte / len(candyAp))
    for y in range(len(glade)):
        if y <= corteY:
            f1.values[y] = [vy for vy in a.values[y]]
            f2.values[y] = [vy for vy in b.values[y]]
        else:
            f1.values[y] = [vy for vy in b.values[y]]
            f2.values[y] = [vy for vy in a.values[y]]
    for x in range(len(candyAp)):
        if x < corteX:
            f1.values[corteY][x] = a.values[corteY][x]
            f2.values[corteY][x] = b.values[corteY][x]
        else:
            f1.values[corteY][x] = b.values[corteY][x]
            f2.values[corteY][x] = a.values[corteY][x]
    return (f1, f2)

def mutate(g, ind):
    
    rand = uniform(0, 1)    
    
    if (rand < mRate):
        for i in range(0, len(glade)):
            for j in range (0, len(candyAp)):
                rand = uniform(0, 1)
                if (rand < mRate):
                    #print("MUTATED")
                    if (ind.values[i][j] == 1):
                        ind.values[i][j] = 0
                    else:
                        ind.values[i][j] = 1

    return ind
    
def newGeneration(g):
    global population
    newGen = []
    p1 = None
    p2 = None
    f1 = None
    f2 = None
    
    while (len(population) < 5*numPop):
        p1 = selectInd(population)
        p2 = selectInd(population)
        (f1, f2) = crossOver(p1, p2)
        
        f1 = mutate(g, f1)
        f2 = mutate(g, f2)
        
        if (f1.validate() and f2.validate()):
            f1.calcFit()
            f2.calcFit()
            if (f1.totalCost >= f2.totalCost):
                if (f1.values not in [ind.values for ind in population]):
                    population.append(f1)
            else:
                if (f2.values not in [ind.values for ind in population]):
                    population.append(f2)
        else:
            if (f1.validate()):
                f1.calcFit()
                if (f1.values not in [ind.values for ind in population]):
                    population.append(f1)
            if (f2.validate()):
                f2.calcFit()
                if (f2.values not in [ind.values for ind in population]):
                    population.append(f2)
                
        population.sort(key = lambda ind: ind.fitness)

    for i in range (0, numPop):
        newGen.append(population[len(population) - 1 - i])
        
    population = newGen
    population.sort(key = lambda ind: ind.fitness)
    
def evolution():
    global numPop
    global mRate
    global bestGen
    bestFit = 0
    best = None
    log = open('log.txt', 'a')
    
    initPop()

    for g in range (0, maxGen):
        newGeneration(g)
        
        mRate = 3*g*g/(maxGen*maxGen) - 3*g/maxGen + 0.8

        if (g - bestGen > 20):
            mRate *= 1+uniform(0,1)
            if mRate > 1:
                mRate -= (mRate - 1) + 0.05 
        
        bestGenFit = population[len(population) - 1].fitness
        
        if (bestFit < bestGenFit):
            bestFit = bestGenFit
            best = population[len(population) - 1]
            bestGen = g
        
        print("Best after %d => %.2f  BestGen = %d  mRate = %.2f" % (g, best.totalCost, bestGen, mRate))
    
    print("best totalCost = %f" % population[len(population) - 1].totalCost)
    print("worst totalCost = %f" % population[0].totalCost)
    
    print("Best after %d => %.2f" % (g, best.totalCost))
    log.write("\nBest after %d => %.2f\n" % (g, best.totalCost))
    for i in range (0, len(glade)):
        print(best.values[i])
        log.write(str(best.values[i]))
        log.write('\n')
    log.write('\n')
    
    log.close
    return best

def main():
    evolution()
    
main()