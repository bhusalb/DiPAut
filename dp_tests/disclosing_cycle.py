__name__ = 'Disclosing Cycle'


def perform_test(kwargs):
    """
    Check if there is a SCC of G that contains an edge
    from an input state that outputs insample or insample′.
    """

    aug_graph_b_0_scc_subgraphs = kwargs['aug_graph_b_0_scc_subgraphs']
    graph = kwargs['graph']

    for subgraph in aug_graph_b_0_scc_subgraphs:
        edges = subgraph.es.select(output_in=["insample", "insampleprime"])
        for edge in edges:
            if not graph.vs[edge.source_vertex['initial_graph_index']]['non-input']:
                return {
                    'name': __name__,
                    'result': True
                }

    return {
        'name': __name__,
        'result': False
    }
