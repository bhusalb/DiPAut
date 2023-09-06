import matplotlib.pyplot as plt
import csv


def read_csv(file):
    fp = open(file, 'r+')
    csv_reader = csv.DictReader(fp)

    return list(csv_reader)


k_min_max_rows = read_csv('./reports/k_min_max_examples_result.csv')
n_box_rows = read_csv('./reports/m_range_examples_result.csv')

plt.figure(1)
plt.plot(list(map(lambda row: int(row['n']), n_box_rows)),
         list(map(lambda row: float(row['mean_time_usage']), n_box_rows)), label='m-range')
plt.legend(loc="upper left")
plt.xlabel("m")
plt.xlim(0, int(n_box_rows[-1]['n']))

plt.ylabel("running time")
plt.title('Performance')
plt.savefig('./plots/performance-m-box-running.png')

plt.figure(2)

plt.plot(list(map(lambda row: int(row['n']), k_min_max_rows)),
         list(map(lambda row: float(row['mean_time_usage']), k_min_max_rows)),
         '-.', label='k-min-max')
plt.legend(loc="upper left")
plt.xlabel("k")
plt.xlim(0, int(k_min_max_rows[-1]['n']))

plt.ylabel("running time")
plt.title('Performance')
plt.savefig('./plots/performance-k-min-max-running.png')

plt.figure(3)
plt.plot(list(map(lambda row: int(row['number_of_states']), n_box_rows)),
         list(map(lambda row: int(row['number_of_transitions']), n_box_rows)), label='m-range')

plt.plot(list(map(lambda row: int(row['number_of_states']), k_min_max_rows)),
         list(map(lambda row: float(row['number_of_transitions']), k_min_max_rows)),
         '-.', label='k-min-max')

plt.legend(loc="upper left")
plt.xlabel("states")
plt.ylabel("transitions")
plt.title('States Vs Transitions')
plt.savefig('./plots/states-vs-transitions.png')

plt.figure(4)

plt.plot(list(
    map(lambda row: int(row['number_of_states']) + int(row['number_of_transitions']) + int(row['number_of_variables']),
        n_box_rows)),
    list(map(lambda row: float(row['mean_time_usage']), n_box_rows)), label='m-range')

plt.legend(loc="upper left")
plt.xlabel("size")
plt.ylabel("running time")
plt.title('Size vs Running time')
plt.savefig('./plots/size-vs-running-time-m-box.png')

plt.figure(5)

plt.plot(list(
    map(lambda row: int(row['number_of_states']) + int(row['number_of_transitions']) + int(row['number_of_variables']),
        k_min_max_rows)),
    list(map(lambda row: float(row['mean_time_usage']), k_min_max_rows)),
    '-.', label='k-min-max')

plt.legend(loc="upper left")
plt.xlabel("size")
plt.ylabel("running time")
plt.title('Size vs Running time')
plt.savefig('./plots/size-vs-running-time-k-min-max.png')

plt.figure(6)

plt.plot(list(
    map(lambda row: int(row['number_of_variables']),
        n_box_rows)),
    list(map(lambda row: float(row['mean_time_usage']), n_box_rows)), label='m-range')

plt.legend(loc="upper left")
plt.xlabel("number of variables")
plt.ylabel("running time")
plt.title('Variables vs Running time')
plt.savefig('./plots/variables-vs-running-time-m-box.png')

plt.figure(7)

plt.plot(list(
    map(lambda row: int(row['number_of_variables']),
        k_min_max_rows)),
    list(map(lambda row: float(row['mean_time_usage']), k_min_max_rows)),
    '-.', label='k-min-max')

plt.legend(loc="upper left")
plt.xlabel("number of variables")
plt.ylabel("running time")
plt.title('Variables vs Running time')
plt.savefig('./plots/variables-vs-running-time-k-min-max.png')

plt.figure(8)
plt.plot(list(map(lambda row: int(row['n']), n_box_rows)),
         list(map(lambda row: float(row['mean_time_usage']), n_box_rows)), label='m-range')

plt.plot(list(map(lambda row: int(row['n']), n_box_rows)),
         list(map(lambda row: pow(int(row['n']), 4) * (0.000018), n_box_rows)), '--', label='0.000018$m^{4}$')

plt.plot(list(map(lambda row: int(row['n']), n_box_rows)),
         list(map(lambda row: pow(int(row['n']), 4) * (0.000008), n_box_rows)), '--', label='0.000008$m^{4}$')
plt.legend(loc="upper left")
plt.xlabel("m")
plt.xlim(0, int(n_box_rows[-1]['n']))
plt.ylabel("running time")
# plt.title('Performance')
plt.savefig('./plots/performance-m-box-running-with-n-cube.png')

plt.figure(9)
plt.plot(list(map(lambda row: int(row['n']), k_min_max_rows)),
         list(map(lambda row: float(row['mean_time_usage']), k_min_max_rows)), label='k-min-max')

plt.plot(list(map(lambda row: int(row['n']), k_min_max_rows)),
         list(map(lambda row: 0.22 + 0.0022 * int(row['n']), k_min_max_rows)), '--', label='0.22 + 0.0022k')

plt.plot(list(map(lambda row: int(row['n']), k_min_max_rows)),
         list(map(lambda row: 0.19 + 0.002 * int(row['n']), k_min_max_rows)), '--', label='0.19 + 0.002k')
plt.legend(loc="upper left")
plt.xlabel("k")
plt.xlim(0, int(k_min_max_rows[-1]['n']))
plt.ylabel("running time")
# plt.title('Performance')
plt.savefig('./plots/performance-k-box-running-with-line.png')
