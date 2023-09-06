from collections import defaultdict
import copy

from igraph import Graph
from . import transitive_closure_of_graph_builder


def build(graph, aug_graph, variables):
    return None
    # number_of_edges = len(aug_graph.es)
    #
    # dep_graph = Graph(directed=True)
    #
    # dep_graph.add_vertices(number_of_edges)
    #
    # already_connected_dep_graph = dict()
    #
    # for variable in variables:
    #     assignment_edges = []
    #     non_assignment_edges = []
    #
    #     for edge in aug_graph.es:
    #         if variable in edge['assignment']:
    #             assignment_edges.append(edge)
    #         else:
    #             non_assignment_edges.append(edge)
    #
    #     graph_without_assignment_edges = aug_graph.copy()
    #
    #     graph_without_assignment_edges.delete_edges(assignment_edges)
    #
    #     trans_closure_without_assignment = transitive_closure_of_graph_builder.build(graph_without_assignment_edges)
    #
    #     for assignment_edge in assignment_edges:
    #         t_c_graph_vertex = trans_closure_without_assignment[assignment_edge.target]
    #
    #         for target_vertex_index, has_edge in enumerate(t_c_graph_vertex):
    #             if has_edge:
    #                 out_edges = aug_graph.vs[target_vertex_index].out_edges()
    #
    #                 for edge in out_edges:
    #
    #                     if variable in edge['lt'] and (
    #                             assignment_edge.index, edge.index) not in already_connected_dep_graph:
    #                         dep_graph.add_edge(assignment_edge.index, edge.index)
    #                         already_connected_dep_graph[(assignment_edge.index, edge.index)] = True
    #                     elif variable in edge['gt'] and (
    #                             edge.index, assignment_edge.index) not in already_connected_dep_graph:
    #                         dep_graph.add_edge(edge.index, assignment_edge.index)
    #                         already_connected_dep_graph[(edge.index, assignment_edge.index)] = True
    #
    # return dep_graph
