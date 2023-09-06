import csv

new_fieldnames = ['n', 'number_of_variables', 'number_of_states', 'number_of_transitions', 'weight_calculation_time',
                  'mean_time_usage']

for report in ['k_min_max_examples_result.csv', 'm_range_examples_result.csv']:
    fp = open(f'./reports/{report}', 'r+')
    new_fp = open(f'./reports/new_{report}', 'w+')
    csv_reader = csv.DictReader(fp)
    rows = list(csv_reader)
    csv_writer = csv.DictWriter(new_fp, fieldnames=new_fieldnames)
    csv_writer.writeheader()
    for row in rows:
        row['mean_time_usage'] = row['mean_time_usage'] + row['time_usage_unit'][0]

        row['weight_calculation_time'] = str(round(float(row['weight_calculation_time']), 3)) + row['time_usage_unit'][0]
        for rm_field in ['weight', 'well_formed', 'time_usage_unit']:
            del row[rm_field]

    csv_writer.writerows(rows)
