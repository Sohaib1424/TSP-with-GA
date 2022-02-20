###
# TSP
###
import matplotlib.pyplot as plt
from Helpers import *

###### pre-processing the data ######

data = open("data.txt").readlines()  # loading the data file
# removing extra characters
data[0] = data[0][1:]
for i in range(len(data)):
    data[i] = list(map(int, data[i][:-1].split(" ")))

cities = [datum[0] for datum in data]
coordination = [datum[1:] for datum in data]

##### solution #####

# parameters
iterations = 5000
mutationRate = .05
popCount = 180  # population count
earlyStopping, counter = 200, 0

population = generatePop(popCount, cities)
bestScores = []
bestRes = cities

scores = evaluate(population, coordination)
population = [order for _, order in sorted(zip(scores, population))]
scores = sorted(scores)
# performing GA

for i in range(iterations):
    if popCount < 2:
        raise EnvironmentError("population count should be greater than 1!")
    if mutationRate < 0 or mutationRate > 1:
        raise EnvironmentError("mutation rate should be between 0 and 1")
    if earlyStopping < 1:
        raise EnvironmentError()

    newGen = []

    for j in range(2 * (popCount//2)):

        probs = createProb(scores)
        choioces = random.choices(population, probs, k=2)
        offSpring1, offSpring2 = crossOver(choioces[0], choioces[1])

        newGen.append(mutate(offSpring1, mutation_rate=mutationRate))
        newGen.append(mutate(offSpring2, mutation_rate=mutationRate))

    for newOrder in newGen:
        population.append(newOrder)  # merging the old and the new population

    scores = evaluate(population, coordination)  # calculating the scores

    # sorting the population based on the scores in ascending order
    population = [order for _, order in sorted(zip(scores, population))]
    # cutting the population
    population = population[:popCount]
    scores = sorted(scores)[:popCount]

    bestScores.append(np.array([scores[0], i]))

    if evaluate(list([bestRes]), coordination) > evaluate(list([population[0]]), coordination):
        counter = 0
        bestRes = population[0]
        print("Iteration {:d}: min Distance = {:.2f}".format(i, bestScores[-1][0]), f"best Result: {bestRes}")

    else:
        counter += 1
        if counter == earlyStopping:
            print("Iteration {:d}: min Distance = {:.2f}".format(i, bestScores[-1][0]), f"best Result: {bestRes}")
            break

x = [coordination[i-1][0] for i in bestRes]
x.append((coordination[bestRes[0]-1][0]))

y = [coordination[i-1][1] for i in bestRes]
y.append((coordination[bestRes[0]-1][1]))

plt.plot(x, y)
plt.scatter(x, y)
plt.xlabel(evaluate([bestRes], coordination)[0])
plt.show()