from itertools import chain

__name__ = 'Leaking Cycle'


def perform_test(kwargs):
    """
    Check if there is a SCC of G that has an edge
    labeled (c, true) and an edge labeled (c′, b′) where c′ ̸= true.
    """

    aug_graph_b_0_scc_subgraphs = kwargs['aug_graph_b_0_scc_subgraphs']
    variables = kwargs['variables']

    for subgraph in aug_graph_b_0_scc_subgraphs:
        lt_list = list(chain.from_iterable(subgraph.es.select(lt_ne=[])['lt']))
        gt_list = list(chain.from_iterable(subgraph.es.select(gt_ne=[])['gt']))
        assignment_list = list(chain.from_iterable(subgraph.es.select(assignment_ne=[])['assignment']))

        for variable in variables:
            if ((variable in lt_list) or (variable in gt_list)) and (variable in assignment_list):
                return {
                    'name': __name__,
                    'result': True
                }

    return {
        'name': __name__,
        'result': False
    }
