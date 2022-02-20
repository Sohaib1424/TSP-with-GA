import math
import random
import numpy as np


# a function to generate the initial population
def generatePop(initPopCount, cities):
    if initPopCount > math.factorial(len(cities)) / 2:
        raise EnvironmentError()

    population = []

    for _ in range(initPopCount):
        population.append(list(np.random.permutation(cities)))

    return population


# performing mutation
def mutate(order, mutation_rate=.05):
    citiesCount = len(order)
    newOrder = list(np.copy(order))

    for _ in range(citiesCount):
        if random.random() <= mutation_rate:
            inds = random.sample([i for i in range(citiesCount)], 2)
            tmp1, tmp2 = newOrder[inds[0]], newOrder[inds[1]]
            newOrder[inds[0]], newOrder[inds[1]] = tmp2, tmp1

    return newOrder


# performing crossover
def crossOver(order1, order2):
    citiesCount = len(order1)
    ind = random.randint(0, citiesCount)
    inds = sorted([ind, (ind + random.randint(1, 5)) % citiesCount])

    offSpring1 = list(order1[inds[0]: inds[1]])
    for city in order2:
        if not offSpring1.__contains__(city):
            offSpring1.append(city)

    offSpring2 = list(order2[inds[0]: inds[1]])
    for city in order1:
        if not offSpring2.__contains__(city):
            offSpring2.append(city)

    return offSpring1, offSpring2


def calcDistance(coord1, coord2):
    x = (coord1[0] - coord2[0]) ** 2
    y = (coord1[1] - coord2[1]) ** 2

    return math.sqrt(x + y)


# a function to evaluate scores (or the cost function)
def evaluate(pop, coordination):
    scores = []
    for order in pop:
        totalDist = 0
        for i in range(len(order)):
            totalDist += calcDistance(coordination[order[i] - 1], coordination[order[(i + 1)%len(order)] - 1])

        scores.append(totalDist)

    return scores


def createProb(scores):
    prob = list(-np.log10(scores))
    prob = list(np.exp(prob))
    prob /= sum(prob)

    return prob
