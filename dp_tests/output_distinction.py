__name__ = "No output distinction"


def perform_test(kwargs):
    graph = kwargs['graph']
    for vertex in graph.vs:
        for out_edge in vertex.out_edges():
            for inner_out_edge in vertex.out_edges():
                if out_edge.index != inner_out_edge.index and out_edge['output'] == inner_out_edge['output']:
                    return {
                        'name': __name__,
                        'result': True
                    }

    return {
        'name': __name__,
        'result': False
    }
