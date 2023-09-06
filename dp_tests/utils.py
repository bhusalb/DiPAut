from collections import defaultdict

from igraph import Graph

sm_vars_memo = defaultdict(dict)
lg_vars_memo = defaultdict(dict)


def is_there_path(aug_graph, source, destination):
    visited = [False] * len(aug_graph.vs)

    visited[source.index] = True
    queue = [source]

    while queue:
        m = queue.pop(0)

        for edge in m.out_edges():
            if destination.index == edge.target:
                return True

            if not visited[edge.target]:
                visited[edge.target] = True
                queue.append(edge.target_vertex)

    return False


def is_there_path_to_condition(aug_graph, vertex, var1, var2):
    visited = [False] * len(aug_graph.vs)

    visited[vertex.index] = True
    queue = [vertex]

    while queue:
        m = queue.pop(0)

        for edge in m.out_edges():
            if (var1, var2) in edge.target_vertex['lt']:
                return True

            if not visited[edge.target]:
                visited[edge.target] = True
                queue.append(edge.target_vertex)

    return False


def get_sm_vars(module, t, vars):
    if t.index in sm_vars_memo:
        return sm_vars_memo[t.index]

    sm_vars = []
    eq_matrix = t.source_vertex['eq']
    for xj in t['lt']:
        for xi in vars:
            if (xi, xj) in eq_matrix:
                sm_vars.append(xi)

    sm_vars_memo[t.index] = sm_vars

    return sm_vars


def get_lg_vars(module, t, vars):
    if t.index in lg_vars_memo[module]:
        return lg_vars_memo[module][t.index]

    lg_vars = []
    eq_matrix = t.source_vertex['eq']
    for xj in t['gt']:
        for xi in vars:
            if (xj, xi) in eq_matrix:
                lg_vars.append(xi)

    lg_vars_memo[module][t.index] = lg_vars

    return lg_vars


def get_copy_of_graph_without_attributes(_graph, extra_number_of_vertices):
    new_graph = Graph(directed=True)
    number_of_vertices = len(_graph.vs)
    new_graph.add_vertices(number_of_vertices + extra_number_of_vertices)
    new_graph.add_edges(_graph.get_edgelist())

    return new_graph, number_of_vertices


def add_edges_from_a_vertex_to_list_of_vertices(graph, source, list_of_targets):
    graph.add_edges([(source, target) for target in list_of_targets])


def add_edges_from_list_of_vertices_to_a_vertex(graph, list_of_sources, target):
    graph.add_edges([(source, target) for source in list_of_sources])
