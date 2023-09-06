import csv

new_fieldnames = ['n', 'number_of_variables', 'number_of_states', 'number_of_transitions',
                  'mean_time_usage', 'well_formed', 'weight']

for report in ['simple_examples_result.csv']:
    fp = open(f'./reports/{report}', 'r+')
    new_fp = open(f'./reports/new_{report}', 'w+')
    csv_reader = csv.DictReader(fp)
    rows = list(csv_reader)
    csv_writer = csv.DictWriter(new_fp, fieldnames=new_fieldnames)
    csv_writer.writeheader()
    for row in rows:
        row['mean_time_usage'] = row['mean_time_usage'] + row['time_usage_unit'][0]
        row['weight_calculation_time'] = row['weight_calculation_time'] + row['time_usage_unit'][0]

        if row['well_formed'] == 'False':
            row['weight'] = ''

        for rm_field in ['time_usage_unit', 'weight_calculation_time']:
            del row[rm_field]

    csv_writer.writerows(rows)
