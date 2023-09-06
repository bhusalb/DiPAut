import argparse
import functools

example = ''

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-number', '-n', type=int, required=True)

args = parser.parse_args()

assignment_template = '''(q{initial_state}:non-input,{d},0): {var1}:= insample; output obot; goto q{second_state}
(q{second_state}:non-input,{d},1): {var2}:= insample; output obot; goto q{third_state}'''

n_box = '''(q{first_state},{d},0): if (insample >= {var1} && insample < {var2}) then output ocontinue; goto q{second_state} elseif (insample >= {var1} && insample > {var2}) then output otop; goto q{exit_state} elseif (insample < {var1} && insample < {var2}) then output obot; goto q{exit_state}'''

line = 1

var_list = []

exit_state = None
d = f'1/{4 * args.number}'

for i in range(1, args.number + 1):
    l = f'l{i}'
    r = f'r{i}'
    var_list.append((l, r))

    n_box_args = dict()
    n_box_args['d'] = d
    n_box_args['initial_state'] = line
    n_box_args['var1'] = l
    n_box_args['var2'] = r
    line += 1
    n_box_args['second_state'] = line
    line += 1
    n_box_args['third_state'] = line
    example += ('\n' if example else '') + assignment_template.format(**n_box_args)

exit_state = None
starting_loop = line

d = f'1/4'

for l, r in var_list:
    n_box_args = dict()
    n_box_args['d'] = d
    n_box_args['first_state'] = line
    n_box_args['var1'] = l
    n_box_args['var2'] = r
    line += 1
    n_box_args['second_state'] = line

    if not exit_state:
        exit_state = starting_loop + len(var_list)

    if var_list.index((l, r)) + 1 == len(var_list):
        n_box_args['second_state'] = starting_loop

    n_box_args['exit_state'] = exit_state
    example += ('\n' if example else '') + n_box.format(**n_box_args)

print(example)
