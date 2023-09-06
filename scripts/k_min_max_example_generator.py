import argparse
import functools

example = ''

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-number', '-n', type=int, required=True)

args = parser.parse_args()

assignment_template = '''(q1,{d},0): min:= insample,max:= insample; output oread; goto q2'''

n_box = '''(q{first_state},{d},0): if (insample > max && insample > min) then max:= insample; output oread; goto q{second_state} elseif (insample <= max && insample >= min) then output oread; goto q{second_state} elseif (insample < max && insample < min) then min:= insample; output oread; goto q{second_state}'''

var_list = []

exit_state = None
d = f'1/{4 * args.number}'

example += assignment_template.format(d=d)

line = 2

for i in range(1, args.number):
    n_box_args = dict()
    n_box_args['d'] = d
    n_box_args['first_state'] = line
    line += 1
    n_box_args['second_state'] = line

    example += ('\n' if example else '') + n_box.format(**n_box_args)

exit_loop = '''(q{first_state},{d},0): if (insample < max && insample < min) then output obot; goto q{exit_state} elseif (insample > max && insample > min) then output otop; goto q{exit_state} elseif (insample <= max && insample >= min) then output ocontinue; goto q{first_state}'''

n_box_args = dict()
n_box_args['d'] = '1/4'
n_box_args['first_state'] = line
line += 1
n_box_args['exit_state'] = line

example += '\n' + exit_loop.format(**n_box_args)

print(example)
