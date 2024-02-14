import random

class Graph:

    def __init__(self):
        self.graph = {}
        self.mst = {}

    def AddEdge(self, u, v, w):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []

        self.graph[u].append((v, w))
        self.graph[v].append((u, w))

    def AddDummy(self, u, v, w):
        self.AddEdge(u, 'DUMMY', w)
        self.AddEdge(v, 'DUMMY', w)

    def IsAdjacent(self, u, v):
        for m, w in self.graph[v]:
            if m == u:
                return True
        return False

    def GetVertices(self):
        return "".join(list(self.graph.keys()))

    def getWeight(self, u, v):
        for m, w in self.graph[v]:
            if m == u:
                return w
        return 0

    def ComputeCost(self, path):
        sum = 0
        for i in range(len(path) - 1):
            sum += self.getWeight(path[i], path[i+1])
        return sum

gr = Graph()
gr.AddEdge('A', 'B', 500)
gr.AddEdge('A', 'C', 650)
gr.AddEdge('A', 'D', 850)
gr.AddEdge('C', 'B', 1000)
gr.AddEdge('C', 'D', 600)
gr.AddEdge('B', 'D', 590)
gr.AddEdge('B', 'G', 1250)
gr.AddEdge('D', 'G', 1500)
gr.AddEdge('D', 'E', 700)
gr.AddEdge('E', 'G', 2500)

manhattancost = {'A': 5, 'B': 3, 'C': 5, 'D': 1.5, 'E': 1.5, 'G': 0}

# Genetic Algorithm
def create_individual(start, end, graph):
    individual = [start]
    current = start
    while current != end:
        neighbors = [neighbor for neighbor, _ in graph[current] if neighbor != 'DUMMY']
        current = random.choice(neighbors)
        individual.append(current)
    return individual

def crossover(parent1, parent2):
    crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(individual, graph):
    index = random.randint(1, len(individual) - 2)
    neighbors = [neighbor for neighbor, _ in graph[individual[index]] if neighbor != 'DUMMY']
    individual[index] = random.choice(neighbors)
    return individual

def evaluate(individual, graph, manhattancost):
    total_cost = gr.ComputeCost(individual)
    manhattan_heuristic = sum(manhattancost[node] for node in individual)
    return total_cost + manhattan_heuristic

def genetic_algorithm(start, end, graph, manhattancost, population_size=50, generations=100):
    population = [create_individual(start, end, graph) for _ in range(population_size)]
    for _ in range(generations):
        population = sorted(population, key=lambda x: evaluate(x, graph, manhattancost))
        new_population = population[:population_size // 2]
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:population_size // 2], k=2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, graph)
            child2 = mutate(child2, graph)
            new_population.extend([child1, child2])
        population = new_population
    return population[0]

start_node = 'A'
end_node = 'G'
shortest_path = genetic_algorithm(start_node, end_node, gr.graph, manhattancost)
print("Shortest Path:", shortest_path)
print("Path Cost:", gr.ComputeCost(shortest_path))
