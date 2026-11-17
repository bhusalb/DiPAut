import itertools
from copy import deepcopy
from igraph import *
from collections import defaultdict


def get_unmergeable_states(graph):
    # States of the original automaton whose copies must not be merged: those in a
    # strongly connected component that contains an assignment transition.
    # Graph.clusters() was renamed to connected_components() in python-igraph 0.10.
    strong_components = getattr(graph, 'connected_components', None) or graph.clusters
    membership = strong_components(mode='strong').membership
    bad_components = {membership[edge.source] for edge in graph.es
                      if edge['assignment'] and membership[edge.source] == membership[edge.target]}
    return {vertex.index for vertex in graph.vs if membership[vertex.index] in bad_components}


def get_initially_related(graph, aug_graph):
    unmergeable = get_unmergeable_states(graph)

    return {(_q1.index, _q2.index): (_q1.index, _q2.index) for _q1 in aug_graph.vs for _q2 in aug_graph.vs if
            _q1.index == _q2.index or (
                    _q1['initial_graph_index'] == _q2['initial_graph_index'] and
                    _q1['initial_graph_index'] not in unmergeable)}


def check_if_each_transition_match_with_a_transition(aug_graph, _q1, _q2, q1_q2_related_map):
    q1 = aug_graph.vs[_q1]
    q2 = aug_graph.vs[_q2]
    for q1_out_edge in q1.out_edges():
        for q2_out_edge in q2.out_edges():
            if q1_out_edge['output'] == q2_out_edge['output'] and \
                    q1_out_edge['real_assignment'] == q2_out_edge['real_assignment'] and \
                    q1_out_edge['lt'] == q2_out_edge['lt'] and \
                    q1_out_edge['gt'] == q2_out_edge['gt'] and \
                    ((q1_out_edge.target, q2_out_edge.target) in q1_q2_related_map or (
                            q2_out_edge.target, q1_out_edge.target) in q1_q2_related_map):
                break
        else:
            return False

    return True


def modifying_the_relation(graph, aug_graph, initially_related):
    related = initially_related
    related_but_not_equal = {k: v for k, v in initially_related.items() if k[0] != k[1]}
    change = True
    while change:
        change = False
        for combination in list(related_but_not_equal.keys()):
            q1, q2 = combination

            if not (check_if_each_transition_match_with_a_transition(aug_graph, q1, q2, related) and
                    check_if_each_transition_match_with_a_transition(aug_graph, q2, q1, related)):
                del related[(q1, q2)]
                del related_but_not_equal[(q1, q2)]
                change = True

    return related


def get_equivalence_classes(relation):
    eq_classes_map = dict()
    number_of_eq_classes = 0
    for value in relation:
        q1, q2 = value
        q1_eq_class_index = -1

        if q1 in eq_classes_map:
            q1_eq_class_index = eq_classes_map[q1]

        q2_eq_class_index = -1
        if q2 in eq_classes_map:
            q2_eq_class_index = eq_classes_map[q2]

        if q1_eq_class_index == -1 and q2_eq_class_index == -1:
            eq_classes_map[q1] = number_of_eq_classes
            eq_classes_map[q2] = number_of_eq_classes
            number_of_eq_classes += 1
        elif q1_eq_class_index != -1 and q2_eq_class_index == -1:
            eq_classes_map[q2] = q1_eq_class_index
        elif q2_eq_class_index != -1 and q1_eq_class_index == -1:
            eq_classes_map[q1] = q2_eq_class_index
        elif q1_eq_class_index != -1 and q2_eq_class_index != -1 and q1_eq_class_index != q2_eq_class_index:
            min_eq_class_index = min(q1_eq_class_index, q2_eq_class_index)
            eq_classes_map[q1] = min_eq_class_index
            eq_classes_map[q2] = min_eq_class_index

    res = defaultdict(list)
    for key, val in eq_classes_map.items():
        res[val].append(key)
    return list(res.values())


def generate_map_for_eq_classes(equivalence_classes):
    eq_classes_map = dict()

    for eq_class_index, eq_class in enumerate(equivalence_classes):
        for vertex in eq_class:
            eq_classes_map[vertex] = eq_class_index

    return eq_classes_map


def assign_attribute_to_vertex(equivalence_classes, aug_graph, new_graph):
    for vertex in new_graph.vs:
        vertex['old_vs_index'] = aug_graph.vs[equivalence_classes[vertex.index][0]]['old_vs_index']
        vertex['initial_graph_index'] = aug_graph.vs[equivalence_classes[vertex.index][0]]['initial_graph_index']


def build_bisimulation_quotient_graph(equivalence_classes, eq_classes_map, aug_graph):
    graph = Graph(directed=True)
    graph.add_vertices(len(equivalence_classes))
    assign_attribute_to_vertex(equivalence_classes, aug_graph, graph)
    for old_edge in aug_graph.es:
        graph.add_edge(
            eq_classes_map[old_edge.source],
            eq_classes_map[old_edge.target],
            **old_edge.attributes()
        )

    return graph


def build(graph, aug_graph):
    initially_related = get_initially_related(graph, aug_graph)
    relation = modifying_the_relation(graph, aug_graph, initially_related)
    equivalence_classes = get_equivalence_classes(relation)
    eq_classes_map = generate_map_for_eq_classes(equivalence_classes)

    return build_bisimulation_quotient_graph(equivalence_classes, eq_classes_map, aug_graph)
