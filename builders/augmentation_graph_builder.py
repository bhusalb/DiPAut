import copy

from igraph import Graph
from rich.console import Console
from rich.table import Table


def pre_build_augmentation_for_privacy_violating_path(_graph):
    graph = Graph(directed=True)
    graph.add_vertices(len(_graph.vs) * 4)
    new_vertices_map = dict()
    current_index = 0

    for old_index in range(len(_graph.vs)):
        new_vertices_map[old_index] = dict()
        for b1 in range(2):
            new_vertices_map[old_index][b1] = dict()
            for b2 in range(2):
                graph.vs[current_index]['old_index'] = old_index
                graph.vs[current_index]['b'] = b1, b2
                graph.vs[current_index]['name'] = f'q{old_index}#{b1}{b2}'
                new_vertices_map[old_index][b1][b2] = current_index
                current_index += 1

    for edge in _graph.es:
        edge['has_real_assignment'] = len(edge['assignment']) > 0
        edge['real_assignment'] = edge['assignment'].copy()
        for b1 in range(2):
            for b2 in range(2):
                graph.add_edge(
                    new_vertices_map[edge.source][b1][b2],
                    new_vertices_map[edge.target][b1][b2],
                    **edge.attributes()
                )

        if edge['assignment']:
            attributes = copy.copy(edge.attributes())
            add_V1 = copy.copy(edge['assignment'])
            add_V1.append('V1')
            attributes['assignment'] = add_V1
            graph.add_edge(
                new_vertices_map[edge.source][0][0],
                new_vertices_map[edge.target][1][0],
                **attributes
            )

            graph.add_edge(
                new_vertices_map[edge.source][0][1],
                new_vertices_map[edge.target][1][1],
                **attributes
            )

        if edge['output'] == 'insample':
            attributes = copy.copy(edge.attributes())
            add_Vinsample = copy.copy(edge['assignment'])
            add_Vinsample.append('Vinsample')
            attributes['assignment'] = add_Vinsample

            graph.add_edge(
                new_vertices_map[edge.source][0][0],
                new_vertices_map[edge.target][0][1],
                **attributes
            )

            graph.add_edge(
                new_vertices_map[edge.source][1][0],
                new_vertices_map[edge.target][1][1],
                **attributes
            )

            if edge['assignment']:
                add_Vinsample = add_Vinsample.copy()
                add_Vinsample.append('V1')

                attributes['assignment'] = add_Vinsample

                graph.add_edge(
                    new_vertices_map[edge.source][0][0],
                    new_vertices_map[edge.target][1][1],
                    **attributes
                )

    return graph


def get_all_variables(graph):
    assignments = graph.es['assignment']
    variables = set()

    for assigment_list in assignments:
        for item in assigment_list:
            variables.add(item)

    return sorted(variables)


def get_empty_lt_eq_matrix(variables):
    lt = dict()
    eq = dict()
    # for variable in variables:
    #     for inner_variable in variables:
    #         lt[variable, inner_variable] = False
    #         eq[variable, inner_variable] = variable == inner_variable

    return lt, eq


def get_edges_and_attributes_for_aug_graph(vertices, aug_graph_edges, vertices_index_memo):
    edge_attributes = []
    edges = []
    for source, destination, attributes in aug_graph_edges:
        edges.append(
            (
                vertices_index_memo[source['hash']],
                vertices_index_memo[destination['hash']],
            )
        )

        edge_attributes.append(attributes)

    return edges, edge_attributes


def assign_vertex_attributes(aug_graph, vertices):
    for index, attributes in enumerate(vertices):
        for property_name, property_value in attributes.items():
            aug_graph.vs[index][property_name] = property_value


def assign_edge_attributes(aug_graph, edge_attributes):
    for index, old_edge_obj in enumerate(edge_attributes):
        aug_graph.es[index].update_attributes(old_edge_obj.attributes().copy())


def assign_cycle_attribute(aug_graph):
    for component in aug_graph.clusters():
        selected_edges = aug_graph.es.select(_within=component)
        selected_edges['cycle'] = True

    return aug_graph


def check_intersect_eq_lt_before(eq, lt, vars):
    for xi, xj in lt.keys():
        if xi == xj or (xi, xj) in eq:
            return False

    return True


def pre_build_augmentation_for_leaking_pair(_graph):
    graph = Graph(directed=True)
    graph.add_vertices(len(_graph.vs) * 3)
    new_vertices_map = dict()
    current_index = 0

    for old_index in range(len(_graph.vs)):
        new_vertices_map[old_index] = dict()
        for b in range(3):
            graph.vs[current_index]['old_index'] = old_index
            graph.vs[current_index]['b'] = b
            graph.vs[current_index]['name'] = f'q{old_index}#{b}'
            new_vertices_map[old_index][b] = current_index
            current_index += 1

    for edge in _graph.es:
        edge['has_real_assignment'] = len(edge['assignment']) > 0
        edge['real_assignment'] = edge['assignment'].copy()
        for b in range(3):
            graph.add_edge(
                new_vertices_map[edge.source][b],
                new_vertices_map[edge.target][b],
                **edge.attributes()
            )

        if edge['assignment']:
            attributes = copy.copy(edge.attributes())
            add_V1 = copy.copy(edge['assignment'])
            add_V1.append('V1')
            attributes['assignment'] = add_V1
            graph.add_edge(
                new_vertices_map[edge.source][0],
                new_vertices_map[edge.target][1],
                **attributes
            )

            add_V2 = copy.copy(edge['assignment'])
            add_V2.append('V2')
            attributes['assignment'] = add_V2

            graph.add_edge(
                new_vertices_map[edge.source][1],
                new_vertices_map[edge.target][2],
                **attributes
            )

    return graph


def build_augmentation_for_leaking_pair(graph):
    return raw_build(pre_build_augmentation_for_leaking_pair(graph))


def other_variables(variables):
    vars_map = dict()
    for var in variables:
        vars_map[var] = []
        for inner_var in variables:
            if inner_var != var:
                vars_map[var].append(inner_var)

    return vars_map


def get_hash_str(new_vertex, lt_matrix, eq_matrix):
    hash_str = f'{new_vertex["old_vs_index"]}${new_vertex["b"]}$'

    lt_str = ''
    eq_str = ''
    for var, inner_var in sorted(lt_matrix.keys()):
        lt_str += f"{var},{inner_var};"

    for var, inner_var in sorted(eq_matrix.keys()):
        eq_str += f"{var},{inner_var};"

    return hash_str + lt_str + '$' + eq_str


def na_func(variables, a_vars):
    return [var for var in variables if var not in a_vars]


def get_sm_vars(lt_matrix, eq_matrix, edge, variables):
    lt1 = [xi for (xi, xj) in lt_matrix if xj in edge['lt']]
    eq1 = [xi for (xi, xj) in eq_matrix if xj in edge['lt']]

    return lt1 + eq1 + edge['lt']


def raw_build(graph):
    variables = get_all_variables(graph)
    vars_map = other_variables(variables)
    lt, eq = get_empty_lt_eq_matrix(variables)

    q0 = graph.vs[0]
    vertices_index_memo = dict()

    starting_point = {'old_vs_index': q0.index, 'initial_graph_index': q0['old_index'], 'b': q0['b'], 'lt': lt,
                      'eq': eq}
    starting_point['hash'] = hash(get_hash_str(starting_point, lt, eq))
    vertices_index_memo[starting_point['hash']] = 0
    vertices = [starting_point]

    queue = [0]

    aug_graph_edges = []

    visited = [False]

    while queue:
        s = queue.pop()
        vertex = vertices[s]
        if visited[s]:
            continue

        out_edges = graph.vs[vertex['old_vs_index']].out_edges()

        for edge in out_edges:

            eq_matrix = vertex['eq'].copy()
            lt_matrix = vertex['lt'].copy()

            a_vars = edge['assignment']
            # na_vars = na_func(variables, a_vars)

            # todo lg_vars and sm_vars can be sets
            lg_vars = []
            sm_vars = []

            if edge['lt']:
                lt1 = [xi for (xi, xj) in lt_matrix if xj in edge['lt']]
                eq1 = [xi for (xi, xj) in eq_matrix if xj in edge['lt']]
                sm_vars = lt1 + eq1 + edge['lt']

            if edge['gt']:
                lt1 = [xi for (xj, xi) in lt_matrix if xj in edge['gt']]
                eq1 = [xi for (xj, xi) in eq_matrix if xj in edge['gt']]
                lg_vars = lt1 + eq1 + edge['gt']

            sm_vars_n_na_vars = [var for var in sm_vars if var not in a_vars]
            lg_vars_n_na_vars = [var for var in lg_vars if var not in a_vars]

            for sm_var in sm_vars:
                for lg_var in lg_vars:
                    lt_matrix[sm_var, lg_var] = True

            if check_intersect_eq_lt_before(eq_matrix, lt_matrix, variables):

                for a_var in a_vars:
                    for var in vars_map[a_var]:
                        if (a_var, var) in lt_matrix:
                            del lt_matrix[a_var, var]
                        if (a_var, var) in eq_matrix:
                            del eq_matrix[a_var, var]

                        if (var, a_var) in lt_matrix:
                            del lt_matrix[var, a_var]

                        if (var, a_var) in eq_matrix:
                            del eq_matrix[var, a_var]

                for a_var in a_vars:
                    for var in sm_vars_n_na_vars:
                        lt_matrix[var, a_var] = True

                    for var in lg_vars_n_na_vars:
                        lt_matrix[a_var, var] = True

                    for _a_var in a_vars:
                        if a_var != _a_var:
                            eq_matrix[_a_var, a_var] = True
                            eq_matrix[a_var, _a_var] = True

                new_vertex = {'old_vs_index': edge.target_vertex.index,
                              'initial_graph_index': edge.target_vertex['old_index'],
                              'b': edge.target_vertex['b'], 'lt': lt_matrix,
                              'eq': eq_matrix}

                aug_graph_edges.append((vertex, new_vertex, edge))

                new_vertex_hash = hash(get_hash_str(new_vertex, lt_matrix, eq_matrix))

                if new_vertex_hash not in vertices_index_memo:
                    vertices.append(new_vertex)

                    visited.append(False)
                    current_index = len(vertices) - 1
                    vertices_index_memo[new_vertex_hash] = current_index

                    queue.append(current_index)

                new_vertex['hash'] = new_vertex_hash

        visited[s] = True

    aug_graph = Graph(directed=True)

    aug_graph.add_vertices(len(vertices))

    assign_vertex_attributes(aug_graph, vertices)
    edges, edge_attributes = get_edges_and_attributes_for_aug_graph(vertices, aug_graph_edges, vertices_index_memo)

    aug_graph.add_edges(edges)

    assign_edge_attributes(aug_graph, edge_attributes)

    assign_cycle_attribute(aug_graph)

    return aug_graph, variables


def debug_matrix(matrix):
    table = Table(title=f'Matrix', show_lines=True, expand=False)
    mapping = {
        True: '1',
        False: '0'
    }
    table.add_column("#")

    for variable in matrix.keys():
        table.add_column(variable)

    for variable, item in matrix.items():
        table.add_row(variable, *map(lambda x: mapping[x], item.values()))

    console = Console()
    console.print(table)
