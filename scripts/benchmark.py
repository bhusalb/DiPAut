import argparse
import csv
import json
import os
import pyperf
import subprocess
import sys

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--folder', '-i', type=str, required=True)

args = parser.parse_args()

folder = args.folder
rows = []
n_box_directory = os.path.join(os.getcwd(), folder)
cmd_template = '''python main.py -input ./{folder}/{file} -m --calculate-weight-time'''
benchmark_time_template = '''python3 -m pyperf command --processes=2 --values=2  --pipe=1  {python} main.py -input ./{folder}/{file} -m'''

for file in os.listdir(n_box_directory):
    print('We are working on ' + folder + ' ' + file)

    cmd = cmd_template.format(file=file, folder=folder)
    process_output = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    process_output = json.loads(process_output.strip(), parse_int=int)

    output = process_output

    benchmark = subprocess.run(benchmark_time_template.format(python=sys.executable, file=file, folder=folder),
                               stdout=subprocess.PIPE,
                               shell=True).stdout.decode('utf-8')

    benchmark = pyperf.BenchmarkSuite.loads(benchmark)

    benchmark = benchmark.get_benchmark('command')
    output['mean_time_usage'] = round(benchmark.mean(), 3)
    output['time_usage_unit'] = benchmark.get_unit()

    rows.append(output)

rows.sort(key=lambda a: a['n'], reverse=False)

with open(f'reports/{folder}_result.csv', 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
