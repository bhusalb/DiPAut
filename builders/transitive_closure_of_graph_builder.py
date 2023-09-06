# transitive closure using Floyd Warshall Algorithm
# Complexity : O(V^3)

from igraph import Graph


def build(aug_graph):
    """reach[][] will be the output matrix that will finally
    have reachability values.
    Initialize the solution matrix same as input graph matrix"""
    adj_matrix = aug_graph.get_adjacency()
    reach = [i[:] for i in adj_matrix]
    # Add self loop
    for vertex in aug_graph.vs.indices:
        reach[vertex][vertex] = 1

    '''Add all vertices one by one to the set of intermediate
    vertices.
    ---> Before start of a iteration, we have reachability value
    for all pairs of vertices such that the reachability values
    consider only the vertices in set
    {0, 1, 2, .. k-1} as intermediate vertices.
    ----> After the end of an iteration, vertex no. k is
    added to the set of intermediate vertices and the
    set becomes {0, 1, 2, .. k}'''
    for k in aug_graph.vs.indices:

        # Pick all vertices as source one by one
        for i in aug_graph.vs.indices:

            # Pick all vertices as destination for the
            # above picked source
            for j in aug_graph.vs.indices:
                # If vertex k is on a path from i to j,
                # then make sure that the value of reach[i][j] is 1
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])

    # transitive_closure_graph = Graph(directed=True)
    #
    # transitive_closure_graph.add_vertices(len(reach))
    #
    # for source, elements in enumerate(reach):
    #     for target, element in enumerate(elements):
    #         if element:
    #             transitive_closure_graph.add_edge(source, target)

    return reach
