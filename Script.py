import random
import itertools
cidades = {
    'A': {'F': 2}, 'B': {'C': 9}, 'C': {'D': 5}, 'D': {'E': 2},
    'E': {'J': 5}, 'F': {'B': 2}, 'G': {'L': 3}, 'H': {'M': 1},
    'I': {'N': 1}, 'J': {'O': 1}, 'K': {'L': 1}, 'L': {'G': 3, 'K': 1},
    'M': {'H': 1}, 'N': {'I': 1}, 'O': {'J': 1}
}
def distance(cidade1, cidade2):
    if cidade2 in cidades[cidade1]:
        return cidades[cidade1][cidade2]
    elif cidade1 in cidades[cidade2]:
        return cidades[cidade2][cidade1]
    else:
        return 10
def total_distance(rotas):
    return sum(distance(rotas[i], rotas[i+1]) for i in range(len(rotas)-1)) + distance(rotas[-1], rotas[0])
def initialize_populacao(size):
    populacao = []
    for _ in range(size):
        individual = list(cidades.keys())
        random.shuffle(individual)
        populacao.append(individual)
    return populacao
def evaluate_populacao(populacao):
    return [total_distance(individual) for individual in populacao]
def selection(populacao, fitnesses, num_parents):
    selected = list(zip(populacao, fitnesses))
    selected.sort(key=lambda x: x[1])
    return [individual for individual, fitness in selected[:num_parents]]
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]
    pointer = 0
    for i in range(size):
        if not child[i]:
            while parent2[pointer] in child:
                pointer += 1
            child[i] = parent2[pointer]
    return child
def mutate(individual):
    i, j = random.sample(range(len(individual)), 2)
    individual[i], individual[j] = individual[j], individual[i]
def replace_populacao(populacao, new_populacao):
    combined = populacao + new_populacao
    combined.sort(key=total_distance)
    return combined[:len(populacao)]
def genetic_algorithm(populacao_size, generations, num_parents, mutation_rate):
    populacao = initialize_populacao(populacao_size)
    for generation in range(generations):
        fitnesses = evaluate_populacao(populacao)
        parents = selection(populacao, fitnesses, num_parents)
        new_populacao = []
        while len(new_populacao) < populacao_size:
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                mutate(child)
            new_populacao.append(child)
        populacao = replace_populacao(populacao, new_populacao)
        best_distance = min(evaluate_populacao(populacao))
        print(f"Generation {generation}: {best_distance}")
    best_rotas = min(populacao, key=total_distance)
    return best_rotas, total_distance(best_rotas)
populacao_size = 100
generations = 500
num_parents = 20
mutation_rate = 0.1
best_rotas, best_distance = genetic_algorithm(populacao_size, generations, num_parents, mutation_rate)
print("Best Route:", best_rotas)
print("Best Distance:", best_distance)