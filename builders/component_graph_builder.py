from collections import defaultdict

from igraph import *

from builders import bisimulation_builder


def calculate_weight_for_edge(old_graph, edge):
    wt = 0
    old_source_vertex = old_graph.vs[edge.source_vertex['initial_graph_index']]
    if not old_source_vertex['non-input'] and edge['output'] != "insampleprime":
        wt = 2 * old_source_vertex['d']
    elif not old_source_vertex['non-input'] and edge['output'] == "insampleprime":
        wt = 2 * old_source_vertex['d'] + old_source_vertex['dprime']
    elif old_source_vertex["non-input"]:
        wt = old_source_vertex['d']

    return wt


def calculate_weight_for_component_node(old_graph, graph, component):
    # For every variable: the largest charge (2d for an input state, d for a non-input
    # state) among the assignments inside the component whose value is read later.
    node_wt = defaultdict(int)

    for edge in graph.es.select(_within=component):
        if not edge['assignment']:
            continue

        old_source_vertex = old_graph.vs[edge.source_vertex['initial_graph_index']]
        charge = old_source_vertex['d'] if old_source_vertex['non-input'] else 2 * old_source_vertex['d']

        for var in edge['assignment']:
            if charge > node_wt[var] and is_there_path_from_assignment_to_lt_or_gt(graph, var, edge.target):
                node_wt[var] = charge

    return sum(node_wt.values())


def is_there_path_from_assignment_to_lt_or_gt(graph, var, starting_index):
    # Is some transition whose guard mentions `var` reachable from `starting_index`
    # (the target of the assigning transition) without another assignment of `var`?
    visited = [False] * (len(graph.vs))
    queue = [starting_index]
    visited[starting_index] = True
    while queue:
        s = queue.pop(0)

        for edge in graph.vs[s].out_edges():
            if var in edge['lt'] or var in edge['gt']:
                return True

            if var not in edge['assignment'] and not visited[edge.target]:
                visited[edge.target] = True
                queue.append(edge.target)

    return False


def component_graph_builder(old_graph, graph):
    components = list(graph.clusters())
    component_graph = Graph(directed=True)
    component_graph.add_vertices(len(components))

    new_vertex_map = dict()

    for component_index, component in enumerate(components):
        for vertex in component:
            new_vertex_map[vertex] = component_index

        component_graph.vs[component_index]['old_indices'] = component
        component_graph.vs[component_index]['weight'] = calculate_weight_for_component_node(old_graph, graph, component)

    for component_index, component in enumerate(components):
        for vertex in component:
            for edge in graph.vs[vertex].out_edges():
                if new_vertex_map[edge.target] != component_index:
                    edge['weight'] = calculate_weight_for_edge(old_graph, edge)
                    component_graph.add_edge(component_index, new_vertex_map[edge.target], **edge.attributes())

    return component_graph, new_vertex_map


def calculate_maximum_weight_path(graph, start=0):
    # Maximum weight of a path from `start` in the component graph (a DAG),
    # summing vertex and edge weights.
    best = [None] * len(graph.vs)
    best[start] = graph.vs[start]['weight']

    for source in graph.topological_sorting(mode='out'):
        if best[source] is None:
            continue  # not reachable from the start component

        for out_edge in graph.vs[source].out_edges():
            target = out_edge.target
            candidate = best[source] + out_edge['weight'] + graph.vs[target]['weight']
            if best[target] is None or best[target] < candidate:
                best[target] = candidate

    return max(weight for weight in best if weight is not None)


def compute_weight(graph, aug_graph):
    bisimulation_graph = bisimulation_builder.build(graph, aug_graph)
    component_graph, vertex_map = component_graph_builder(graph, bisimulation_graph)

    # vertex 0 of the quotient is the class of the initial state
    return calculate_maximum_weight_path(component_graph, vertex_map[0])
