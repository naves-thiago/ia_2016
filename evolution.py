from random import randint

numPop = 100;
population = [];
best = -1;
bestIndex = -1;
candyAp = [1.1, 1.2, 1.3, 1.4, 1.5];
glade = [150, 140, 130, 120, 110, 100, 95, 90, 85, 80];

class Ind:
    def __init__(self):
        self.values = [[0 for j in range(len(candyAp))] for i in range(len(glade))]
        self.fitness = 0
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
        
    def lineFit(self, line):
        fit = 0;
        ap = 0;
        for i in range (0, len(candyAp)):
            ap += candyAp[i] * self.values[line][i]
        fit = glade[line]/ap
        #print ("linefit = %.2f" % fit)
        return fit

    def totalFit(self):
        for i in range (0, len(glade)):
            self.fitness += self.lineFit(i)
        
def initPop():
    global best
    global bestIndex
    global population
    ind = Ind()
    while (ind.validate() == False):
        ind = Ind()
    ind.totalFit()
    best = ind.fitness
    bestIndex = 0
    population.append(ind)
    while (len(population) < numPop):
        ind = Ind()
        if (ind.validate()):
            ind.totalFit()
            population.append(ind)
            if (ind.fitness < best):
                best = ind.fitness
                bestIndex = len(population)-1
            
def main():
    global bestIndex
    global population
    initPop()
    
    print(len(population))
    print("final bestIndex = %d" % bestIndex)
    print("best = %.2f" % best)
main()