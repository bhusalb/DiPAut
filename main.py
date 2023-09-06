from statistics import mean

from rich import box

import dp_tests
from core import parser, tokenizer
from builders import augmentation_graph_builder, graph_builder, component_graph_builder
from rich.console import Console
from rich.table import Table
import json

import argparse


def read_file(file_name):
    with open(file_name) as fp:
        lines = fp.readlines()
    return lines


def parse(lines):
    parsed_program = []

    for line in lines:
        parser_obj = parser.make_parser()
        lexer = tokenizer.make_lexer()
        parsed_program.append(parser_obj.parse(line, lexer=lexer, debug=False))

    return parsed_program


def process(parse_list):
    graph = graph_builder.build(parse_list)

    # graph.vs['old_index'] = graph.vs.indices
    # graph.vs['b'] = 0
    #
    # augmentation_graph_builder.raw_build(graph)
    # import sys
    # sys.exit(0)
    aug_graph, variables = augmentation_graph_builder.build_augmentation_for_leaking_pair(
        graph)

    aug_graph_b_0 = aug_graph.vs.select(b_eq=0).subgraph()

    aug_graph_b_0_scc_subgraphs = aug_graph_b_0.clusters().subgraphs()
    aug_graph_b_1_and_2 = aug_graph.vs.select(b_in=[1, 2]).subgraph()

    output = []

    args_dict = dict()

    args_dict['graph'] = graph
    args_dict['aug_graph_b_0'] = aug_graph_b_0
    args_dict['aug_graph_b_0_scc_subgraphs'] = aug_graph_b_0_scc_subgraphs
    args_dict['aug_graph_b_1_and_2'] = aug_graph_b_1_and_2
    args_dict['variables'] = variables

    for test in dp_tests.active_tests:
        test_op = test.perform_test(args_dict)
        output.append(test_op)
        if test_op['result']:
            break

    op_distinction = dp_tests.output_distinction.perform_test(args_dict)
    return output, op_distinction, graph, aug_graph_b_0, variables


def print_output_table(file_name, output, output_distinction, graph, aug_graph):
    print('----------------------------------------------------------------------------')

    table = Table(title=f'Result of {file_name}', show_lines=True, expand=True, box=box.SQUARE)
    if is_differentially_private(output):
        table.add_row('Automata is differentially private and weight is {}.'.format(
            component_graph_builder.compute_weight(graph, aug_graph)))
        table.box = None
    else:
        table.add_column("Test")
        table.add_column("Detected?")

        for item in output:
            table.add_row(item['name'], 'Yes' if item['result'] else 'No')

        if not output_distinction['result']:
            table.caption = 'Automata is not differentially private.'
        else:
            table.caption = 'Automata is not well-formed.'

    console = Console()
    console.print(table)


def get_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-input', '-i', type=str, required=True)
    parser.add_argument('--show-graph', '-g', action='store_true')
    parser.add_argument('--metadata', '-m', action='store_true')
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--profile', action='store_true')
    parser.add_argument('--calculate-weight-time', action='store_true')

    return parser.parse_args()


def is_differentially_private(output):
    is_not_differentially_private = False

    for test in output:
        is_not_differentially_private = is_not_differentially_private or test['result']

    return not is_not_differentially_private


def metadata_collector(args, output, graph, aug_graph, filename):
    metadata = dict()
    try:
        metadata['n'] = int(filename.split('/')[-1].split('.')[0])
    except ValueError:
        metadata['n'] = filename.split('/')[-1].split('.')[0]

    metadata['number_of_variables'] = len(augmentation_graph_builder.get_all_variables(graph))
    metadata['number_of_states'] = len(graph.vs)
    metadata['number_of_transitions'] = len(graph.es)
    # metadata['number_of_states_in_aug'] = len(aug_graph.vs)
    # metadata['number_of_transitions_in_aug'] = len(aug_graph.es)
    metadata['well_formed'] = is_differentially_private(output)

    metadata['weight'] = str(component_graph_builder.compute_weight(graph, aug_graph))
    # metadata['weight_time'] = ''
    if args.calculate_weight_time:
        import timeit
        fun = lambda: component_graph_builder.compute_weight(graph, aug_graph)
        fun()

        metadata['weight_calculation_time'] = round(mean(timeit.Timer('fun()', globals=locals()).repeat(
            repeat=10, number=3)), 5)

    return metadata


def run(args):
    parsed_program = parse(read_file(args.input))

    output, output_distinction, graph, aug_graph, variables = process(parsed_program)

    if args.metadata:
        print(json.dumps(metadata_collector(args, output, graph, aug_graph, args.input)))
        return

    print_output_table(args.input, output, output_distinction, graph, aug_graph)

    if args.show_graph:
        graph_builder.draw_graph(graph, args.input)
        graph_builder.draw_graph(aug_graph, args.input, True)


if __name__ == "__main__":
    args = get_args()

    if args.profile:
        from core import profiler

        profiler.run(run, args)
    else:
        run(args)
