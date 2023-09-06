__name__ = 'Privacy Violating Path'

from dp_tests.utils import *
from builders.augmentation_graph_builder import pre_build_augmentation_for_privacy_violating_path, raw_build


def perform_test(kwargs):
    graph = kwargs['graph']

    if 'insample' not in graph.es['output']:
        return {
            'name': __name__,
            'result': False
        }

    aug_graph, variables = raw_build(pre_build_augmentation_for_privacy_violating_path(graph))

    restricted_aug_graph = aug_graph.vs.select(b_in=[(1, 0), (1, 1)]).subgraph()

    scc_transitions = restricted_aug_graph.es.select(cycle=True)

    for t in scc_transitions:
        if 'V1' in get_sm_vars(__name__, t, variables) and (('V1', 'Vinsample') in t.source_vertex['eq'] or \
                                                            is_there_path_to_condition(restricted_aug_graph,
                                                                                       t.target_vertex,
                                                                                       'Vinsample', 'V1')):
            return {
                'name': __name__,
                'result': True
            }

        if 'V1' in get_lg_vars(__name__, t, variables) and (('V1', 'Vinsample') in t.source_vertex['eq'] or \
                                                            is_there_path_to_condition(restricted_aug_graph,
                                                                                       t.target_vertex,
                                                                                       'V1', 'Vinsample')):
            return {
                'name': __name__,
                'result': True
            }

    return {
        'name': __name__,
        'result': False
    }
