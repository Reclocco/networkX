import networkx as nx
import matplotlib.pyplot as plt
import random


def calc_traffic(graph, N):
    nx.set_edge_attributes(graph, 0, 'a')

    for ii, row in enumerate(N):
        for jj, traffic in enumerate(row):
            path = nx.shortest_path(graph, ii, jj)

            for k in range(len(path) - 1):
                graph[path[k]][path[k + 1]]['a'] += traffic


def calc_delay(graph, N):
    calc_traffic(graph, N)

    return 1 / sum_matrix(N) * sum([graph[e1][e2]['a'] / (graph[e1][e2]['c'] - graph[e1][e2]['a'])
                                    if graph[e1][e2]['c'] > graph[e1][e2]['a'] else -1 for e1, e2 in graph.edges()])


def gen_matrix():
    N = []
    for i in range(10):
        N.append([])
        for j in range(10):
            if i == j:
                N[i].append(0)
            else:
                N[i].append(random.randint(1, 9))

    return N


def sum_matrix(N):
    x = 0
    for row in N:
        for element in row:
            x += element

    return x


def calc_reliability(start_graph, matrix, t_max, p, intervals=10, repetitions=1000):
    nx.set_edge_attributes(start_graph, p, 'reliability')
    passed_tests = 0
    for _ in range(repetitions):
        graph = start_graph.copy()

        for _ in range(intervals):
            for edge in list(graph.edges()):
                if random.random() > graph[edge[0]][edge[1]]['reliability']:
                    graph.remove_edge(*edge)

            if not nx.is_connected(graph):
                break

            if 0 < calc_delay(graph, matrix) < t_max:
                passed_tests += 1

    return passed_tests / (repetitions * intervals)


def main():
    G = nx.petersen_graph()
    print("Graf- krawędzie: ", len(G.edges()), " wierzhołki: ", len(G))

    # macierz natężeń
    matrix = gen_matrix()

    # ustalamy niezawodność
    for edge in G.edges():
        G[edge[0]][edge[1]]['reliability'] = 0.91
        G[edge[0]][edge[1]]['c'] = 100
        G[edge[0]][edge[1]]['a'] = 0

    # nx.draw(G)
    # plt.show()

    print("sr. opoznienie: ", calc_delay(G, matrix))
    print("niezawodnosc: ", calc_reliability(G, matrix, 0.05, 0.98) * 100, "%")


def main2():
    reliability_increase_strain = []

    for i in range(100):
        G = nx.petersen_graph()
        print("Graf- krawędzie: ", len(G.edges()), " wierzhołki: ", len(G))

        # macierz natężeń
        matrix = gen_matrix()
        for j in range(i):
            for row in range(len(matrix)):
                for element in range(len(matrix[row])):
                    matrix[row][element] += 1

        # ustalamy niezawodność
        for edge in G.edges():
            G[edge[0]][edge[1]]['reliability'] = 0.91
            G[edge[0]][edge[1]]['c'] = 1000
            G[edge[0]][edge[1]]['a'] = 0

        reliability_increase_strain.append(calc_reliability(G, matrix, 0.05, 0.98, repetitions=10))
        print(i)

    plt.plot(reliability_increase_strain)
    plt.show()


def main3():
    reliability_increase_thruput = []

    for i in range(100):
        G = nx.petersen_graph()
        print("Graf- krawędzie: ", len(G.edges()), " wierzhołki: ", len(G))

        # macierz natężeń
        matrix = gen_matrix()

        # ustalamy niezawodność
        for edge in G.edges():
            G[edge[0]][edge[1]]['reliability'] = 0.91
            G[edge[0]][edge[1]]['c'] = 50 + i
            G[edge[0]][edge[1]]['a'] = 0

        reliability_increase_thruput.append(calc_reliability(G, matrix, 0.05, 0.98, repetitions=10))
        print(i)

    plt.plot(reliability_increase_thruput)
    plt.show()


def main4():
    reliability_increase_edges = []

    for i in range(100):
        G = nx.path_graph(20)
        added = 0
        while added < i:
            n1 = random.randint(0, 19)
            n2 = random.randint(0, 19)

            if n1 != n2 and n1 not in G.neighbors(n2):
                G.add_edge(n1, n2)
                added += 1

        print("Graf- krawędzie: ", len(G.edges()), " wierzhołki: ", len(G))

        # macierz natężeń
        matrix = gen_matrix()

        # ustalamy niezawodność
        for edge in G.edges():
            G[edge[0]][edge[1]]['reliability'] = 0.89
            G[edge[0]][edge[1]]['c'] = 100
            G[edge[0]][edge[1]]['a'] = 0

        reliability_increase_edges.append(calc_reliability(G, matrix, 0.05, 0.98, repetitions=10))
        print(i)

    plt.plot(reliability_increase_edges)
    plt.show()


# main()
# main2()
# main3()
main4()
