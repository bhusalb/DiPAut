from igraph import Graph, plot

from exceptions.no_goto_exception import NoGotoException
from exceptions.unable_to_process import UnableToProcess
from fractions import Fraction

comparison_dict = {
    '>': 'G',
    '>=': 'G',
    '<': 'L',
    '<=': 'L'
}


def get_vertex_name(state):
    return int(state[1:]) - 1


def get_lt_gt_list(comparisons):
    gt = []
    lt = []

    for comparison in comparisons:
        if comparison[1][0] == '>':
            lt.append(comparison[-1])

        if comparison[1][0] == '<':
            gt.append(comparison[-1])

    return lt, gt


def process_statement(statement, vertex, vertices, edges, output_list, assignment_list, lt_list, gt_list,
                      last_condition=[]):
    """
    1. check if block and else block
    2. process assignment, output and comparisons
    """

    if statement[0][0] == 'ifBlock':
        # check if statement
        condition = statement[0][1][2]
        process_statement(statement[0][1][5], vertex, vertices, edges, output_list, assignment_list, lt_list, gt_list,
                          condition)
        if statement[-1][0] == 'elseBlock':
            # check else statement
            else_blocks = statement[-1][1]

            for else_block in else_blocks:
                condition = else_block[2]
                process_statement(else_block[5], vertex, vertices, edges, output_list, assignment_list, lt_list,
                                  gt_list,
                                  condition)
    else:

        # let find goto index
        if statement[-1][0] != 'goto':
            raise NoGotoException()

        goes_to = get_vertex_name(statement[-1][1])

        assignment = []
        if statement[0][0] == 'output':
            output = statement[0][1]
        elif statement[0][0] == 'assignment':
            assignment = statement[0][1]
            output = statement[1][1]
        else:
            raise UnableToProcess()

        edges.append([vertex, goes_to])
        assignment_list.append(sorted(assignment))
        lt, gt = get_lt_gt_list(last_condition)
        gt_list.append(gt)
        lt_list.append(lt)
        output_list.append(output)
        vertices.add(goes_to)


def is_non_input_vertex(state):
    return 'non-input' in state


def remove_unreachable_vertices(graph):
    visited = [False] * len(graph.vs)

    queue = []

    queue.append(0)
    visited[0] = True

    while queue:
        s = queue.pop(0)

        for out_edge in graph.vs[s].out_edges():
            target_vertex = out_edge.target
            if not visited[target_vertex]:
                queue.append(target_vertex)
                visited[target_vertex] = True

    for vertex, reachable in enumerate(visited):
        if not reachable:
            graph.delete_vertices(vertex)


def assign_attributes_to_edges(graph, output_list, assignment_list, lt_list, gt_list):
    graph.es['lt'] = lt_list
    graph.es['gt'] = gt_list
    graph.es['output'] = output_list
    graph.es['assignment'] = assignment_list


def assign_attributes_to_vertices(graph, vertices_properties):
    for vertex, properties in vertices_properties.items():
        for property_name, property_value in properties.items():
            graph.vs[vertex][property_name] = property_value


def get_number(value):
    if isinstance(value, tuple):
        value = ''.join(value)

    return Fraction(value)


def get_vertices_properties(state):
    properties = {
        'non-input': is_non_input_vertex(state),
        'd': None,
        'dprime': None,
        'mean': None,
        'meanprime': None
    }

    if properties['non-input']:
        starting_index = 5
    else:
        starting_index = 3

    properties['d'] = get_number(state[starting_index])

    properties['mean'] = get_number(state[starting_index + 2])

    if len(state) > 10:
        properties['dprime'] = get_number(state[starting_index + 4])

        properties['meanprime'] = get_number(state[starting_index + 6])

    return properties


def build(parsed_program):
    output_list = []
    assignment_list = []
    edges = []
    vertices = set()
    vertices_properties = {}
    lt_list = []
    gt_list = []

    for row in parsed_program:
        vertex = get_vertex_name(row[0][1])
        vertices.add(vertex)
        vertices_properties[vertex] = get_vertices_properties(row[0])
        process_statement(row[2], vertex, vertices, edges, output_list, assignment_list, lt_list, gt_list)

    graph = Graph(directed=True)

    graph.add_vertices(len(vertices))
    graph.add_edges(edges)

    assign_attributes_to_edges(graph, output_list, assignment_list, lt_list, gt_list)

    assign_attributes_to_vertices(graph, vertices_properties)

    remove_unreachable_vertices(graph)

    # strongly_connected_components = graph.clusters()

    return graph


def get_label(edge):
    label = f'i={edge.index}, '
    # label = ''
    if 'assignment' in edge.attribute_names() and edge['assignment']:
        label += 'a=' + str(edge['assignment'])

    if 'gt' in edge.attribute_names() and edge['gt']:
        label += ', gt=' + str(edge['gt'])

    if 'lt' in edge.attribute_names() and edge['lt']:
        label += ' lt=' + str(edge['lt'])

    if 'output' in edge.attribute_names() and edge['output']:
        label += (', ' if label else ' ') + edge['output']

    if 'weight' in edge.attribute_names():
        label += ', c=' + str(edge['weight'])

    return label


def draw_graph(g, filename, is_big=False):
    box_size = (2048, 2048) if is_big else (1024, 1024)

    g.es['curved'] = True

    layout = g.layout("kk")
    visual_style = {}
    visual_style["vertex_size"] = 40
    visual_style["vertex_color"] = ["green"]
    visual_style["vertex_label_color"] = ["blue"]
    visual_style["vertex_label_angle"] = 180
    visual_style['vertex_label_dist'] = 2
    visual_style['edge_align_label'] = True

    visual_style["vertex_label"] = list(map(lambda x: f'q{x + 1}', g.vs.indices))
    visual_style["edge_label"] = list(map(get_label, g.es))
    visual_style['edge_color'] = '#C0C0C0'
    visual_style["layout"] = layout
    visual_style["bbox"] = box_size
    visual_style["margin"] = 100
    visual_style['autocurve'] = True
    visual_style['edge_curved'] = False
    # visual_style['target'] = f"{filename.split(os.path.sep)[-1].split('.')[0]}.png"

    plot(g, **visual_style)
