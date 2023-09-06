__name__ = "Leaking Pair"

from dp_tests.utils import *


def check_if_sources_reachable_from_targets(_graph, sources, targets):
    graph, length_of_vertices = get_copy_of_graph_without_attributes(_graph, 2)

    vertex_a = length_of_vertices
    vertex_b = length_of_vertices + 1

    add_edges_from_a_vertex_to_list_of_vertices(graph, vertex_a, targets)
    add_edges_from_list_of_vertices_to_a_vertex(graph, sources, vertex_b)

    return is_there_path(graph, graph.vs[vertex_a], graph.vs[vertex_b])


def check_sv2v1_condition(_graph, target_l1, target_l4, l1_index_map, l4_index_map, target_index_map,
                          source_index_map):
    sv2v1 = set(v.index for v in _graph.vs if ('V2', 'V1') in v['lt'])
    graph, length_of_vertices = get_copy_of_graph_without_attributes(_graph, 1)
    vertex_c = length_of_vertices

    add_edges_from_list_of_vertices_to_a_vertex(graph, sv2v1, vertex_c)

    s14 = set(graph.subcomponent(graph.vs[vertex_c], mode='in'))
    s14.remove(vertex_c)

    s14_n_l1_target = s14.intersection(target_l1)
    s14_n_l4_target = s14.intersection(target_l4)

    l1_prime = {l1 for l1_target in s14_n_l1_target for l1 in l1_index_map[l1_target]}
    l4_prime = {l4 for l4_target in s14_n_l4_target for l4 in l4_index_map[l4_target]}

    l1_prime_sources = {source_index_map[t_prime] for t_prime in l1_prime}
    l1_prime_targets = {target_index_map[t_prime] for t_prime in l1_prime}
    l4_prime_sources = {source_index_map[t_prime] for t_prime in l4_prime}
    l4_prime_targets = {target_index_map[t_prime] for t_prime in l4_prime}

    return check_if_sources_reachable_from_targets(_graph, l1_prime_sources, l4_prime_targets) or \
           check_if_sources_reachable_from_targets(_graph, l4_prime_sources, l1_prime_targets)


def check_sv1v2_condition(_graph, target_l2, target_l3, l2_target_index_map, l3_target_index_map, target_index_map,
                          source_index_map):
    sv1v2 = {v.index for v in _graph.vs if ('V1', 'V2') in v['lt']}
    graph, length_of_vertices = get_copy_of_graph_without_attributes(_graph, 1)
    vertex_c = length_of_vertices

    add_edges_from_list_of_vertices_to_a_vertex(graph, sv1v2, vertex_c)

    s23 = set(graph.subcomponent(graph.vs[vertex_c], mode='in'))
    s23.remove(vertex_c)

    s23_n_l2_target = s23.intersection(target_l2)
    s23_n_l3_target = s23.intersection(target_l3)

    l2_prime = {l2 for l2_target in s23_n_l2_target for l2 in l2_target_index_map[l2_target]}
    l3_prime = {l3 for l3_target in s23_n_l3_target for l3 in l3_target_index_map[l3_target]}

    l2_prime_sources = {source_index_map[t_prime] for t_prime in l2_prime}
    l2_prime_targets = {target_index_map[t_prime] for t_prime in l2_prime}
    l3_prime_sources = {source_index_map[t_prime] for t_prime in l3_prime}
    l3_prime_targets = {target_index_map[t_prime] for t_prime in l3_prime}

    return check_if_sources_reachable_from_targets(_graph, l2_prime_sources, l3_prime_targets) or \
           check_if_sources_reachable_from_targets(_graph, l3_prime_sources, l2_prime_targets)


def perform_test(kwargs):
    graph = kwargs['graph']
    aug_graph = kwargs['aug_graph_b_1_and_2']
    variables = kwargs['variables']

    scc_transitions = aug_graph.es.select(cycle=True)
    l1, l2, l3, l4 = set(), set(), set(), set()
    src_l1, src_l2, src_l3, src_l4 = set(), set(), set(), set()
    target_l1, target_l2, target_l3, target_l4 = set(), set(), set(), set()
    l1_target_index_map, l2_target_index_map, l3_target_index_map, l4_target_index_map = (defaultdict(list),) * 4
    target_index_map = dict()
    source_index_map = dict()
    for t in scc_transitions:
        target_index_map[t.index] = t.target
        source_index_map[t.index] = t.source
        if t.source_vertex['b'] == 1 and 'V1' in get_sm_vars(__name__, t, variables):
            l1.add(t.index)
            src_l1.add(t.source)
            target_l1.add(t.target)
            l1_target_index_map[t.target].append(t.index)

        if t.source_vertex['b'] == 1 and 'V1' in get_lg_vars(__name__, t, variables):
            l2.add(t.index)
            src_l2.add(t.source)
            target_l2.add(t.target)
            l2_target_index_map[t.target].append(t.index)

        if t.source_vertex['b'] == 2 and 'V2' in get_sm_vars(__name__, t, variables):
            l3.add(t.index)
            src_l3.add(t.source)
            target_l3.add(t.target)
            l3_target_index_map[t.target].append(t.index)

        if t.source_vertex['b'] == 2 and 'V2' in get_lg_vars(__name__, t, variables):
            l4.add(t.index)
            src_l4.add(t.source)
            target_l4.add(t.target)
            l4_target_index_map[t.target].append(t.index)

    if check_if_sources_reachable_from_targets(aug_graph, src_l2, target_l1) or \
            check_if_sources_reachable_from_targets(aug_graph, src_l1, target_l2) or \
            check_sv2v1_condition(aug_graph, target_l1, target_l4, l1_target_index_map, l4_target_index_map,
                                  target_index_map,
                                  source_index_map) or \
            check_sv1v2_condition(aug_graph, target_l2, target_l3, l2_target_index_map, l3_target_index_map,
                                  target_index_map,
                                  source_index_map):
        return {
            'name': __name__,
            'result': True
        }

    return {
        'name': __name__,
        'result': False
    }
