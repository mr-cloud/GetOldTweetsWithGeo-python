import time
import subprocess
import os


t_format = '%Y-%m-%d'
base_cmd = 'python2 Exporter.py --querysearch "{}"  --since {} --until {} --maxtweets {} --output {}/{}_output_got.csv'
queries = ['timessquare', 'times_square']
for idx, query in enumerate(queries):
    if idx == 0:
        continue
    dir_name = 'datasets-' + str(idx)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    maxtweets = 3000
    start_date = '2009-01-01'
    end_date = '2018-02-28'

    start = time.mktime(time.strptime(start_date, t_format))
    end = time.mktime(time.strptime(end_date, t_format))
    step = 1 * 30 * 24 * 3600
    to = start + step
    metric_s = time.time()
    with open('fail.log', 'a') as f:
        while start < end:
            start_date = time.strftime(t_format, time.localtime(start))
            to_date = time.strftime(t_format, time.localtime(to))
            print(time.strftime('%Y-%m-%d %H:%M:%S') + ' Processing: ' + start_date + '_' + to_date)
            cmd = base_cmd.format(query, start_date, to_date, maxtweets, dir_name, start_date + '_' + to_date)
            try:
                subprocess.check_call(cmd.split(), stdout=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                f.write('Crawling failed! start={}, end={}, error={}\n'.format(start_date, to_date, e.message))
                f.flush()
            start = to
            to += step
    metric_e = time.time()
    print('Consume time {} hours.'.format((metric_e - metric_s) / 3600.0))