import argparse
import csv
import json
import os
import pyperf
import subprocess
import sys

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--file', '-i', type=str, required=True)

args = parser.parse_args()

file = args.file
rows = []
cmd_template = '''python main.py -input ./{file} -m --calculate-weight-time'''
benchmark_time_template = '''python3 -m pyperf command --pipe=1  {python} main.py -input ./{file} -m'''

print('We are working on ' + ' ' + file)

cmd = cmd_template.format(file=file)
# process_output = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
# process_output = json.loads(process_output.strip(), parse_int=int)

output = dict()

benchmark = subprocess.run(benchmark_time_template.format(python=sys.executable, file=file),
                           stdout=subprocess.PIPE,
                           shell=True).stdout.decode('utf-8')

benchmark = pyperf.BenchmarkSuite.loads(benchmark)
benchmark = benchmark.get_benchmark('command')
output['mean_time_usage'] = round(benchmark.mean(), 3)
output['time_usage_unit'] = benchmark.get_unit()

print(output)
