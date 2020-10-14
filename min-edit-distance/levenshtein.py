import numpy as np


def print_distances(distances, token1Length, token2Length):
    for t1 in range(token1Length + 1):
        for t2 in range(token2Length + 1):
            print(int(distances[t1][t2]), end=" ")
        print()


def lev_dist_words(tokenA, tokenB):
    distances = np.zeros((len(tokenA) + 1, len(tokenB) + 1))

    for tA in range(1, len(tokenA) + 1):
        for tB in range(1, len(tokenB) + 1):
            charA = tokenA[tA - 1]
            charB = tokenB[tB - 1]
            if charA == charB:
                distances[tA][tB] = distances[tA - 1][tB - 1]
            else:
                before = distances[tA][tB - 1]
                upper = distances[tA - 1][tB]
                diagonal = distances[tA - 1][tB - 1]

                if (before <= upper and before <= diagonal):
                    distances[tA][tB] = before + 1
                elif (upper <= before and upper <= diagonal):
                    distances[tA][tB] = upper + 1
                else:
                    distances[tA][tB] = diagonal + 1

    print_distances(distances, len(tokenA), len(tokenB))
    return distances[len(tokenA)][len(tokenB)]


dist = lev_dist_words("студент", "николай")
print(dist)
