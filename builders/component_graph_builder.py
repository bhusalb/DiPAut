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
    node_wt = dict()
    edges = graph.es.select(_within=component)

    dx1 = defaultdict(list)
    dx2 = defaultdict(list)
    var_set = set()

    for edge in edges:
        old_source_vertex = old_graph.vs[edge.source_vertex['initial_graph_index']]
        for var in edge['assignment']:
            var_set.add(var)
            if old_source_vertex['non-input']:
                dx2[var].append(old_source_vertex['d'])
            else:
                dx1[var].append(2 * old_source_vertex['d'])

    for var in var_set:
        if is_there_path_from_assignment_to_lt_or_gt(graph, var, component[0]):
            node_wt[var] = max(max(dx1[var]) if var in dx1 else 0,
                               max(dx2[var]) if var in dx2 else 0)
        else:
            node_wt[var] = 0

    return sum(node_wt.values())


def is_there_path_from_assignment_to_lt_or_gt(graph, var, starting_index):
    visited = [False] * (len(graph.vs))
    s = starting_index
    queue = [s]
    visited[s] = True
    while queue:

        s = queue.pop(0)

        for edge in graph.vs[s].out_edges():
            if not visited[edge.target]:

                if var in edge['lt'] or var in edge['gt']:
                    return True

                if var not in edge['assignment']:
                    queue.append(edge.target)

                visited[edge.target] = True

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


def calculate_maximum_weight_path(graph):
    _visited = [False] * len(graph.vs)

    graph.vs['max_weight_upto_here'] = 0
    graph.vs[0]['max_weight_upto_here'] = graph.vs[0]['weight']

    _visited[0] = True

    queue = [[0, _visited]]

    while queue:
        source, visited = queue.pop(0)
        source_vertex = graph.vs[source]

        max_weight_upto_source = source_vertex['max_weight_upto_here']

        for out_edge in source_vertex.out_edges():
            target_vertex = out_edge.target_vertex
            target = out_edge.target

            if not visited[target]:

                visited[target] = True

                queue.append([target, visited.copy()])

                new_max_weight_upto_here = max_weight_upto_source + out_edge['weight'] + out_edge.target_vertex[
                    'weight']

                if target_vertex['max_weight_upto_here'] < new_max_weight_upto_here:
                    target_vertex['max_weight_upto_here'] = new_max_weight_upto_here

    return max(graph.vs['max_weight_upto_here'])


def compute_weight(graph, aug_graph):
    bisimulation_graph = bisimulation_builder.build(graph, aug_graph)
    component_graph, vertex_map = component_graph_builder(graph, bisimulation_graph)

    return calculate_maximum_weight_path(component_graph)
