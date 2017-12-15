import time
import subprocess


maxtweets=10000
t_format = '%Y-%m-%d'
start_date = '2010-11-21'
end_date = '2011-02-19'
base_cmd = 'python2 Exporter.py --querysearch "#timessquare"  --since {} --until {} --maxtweets {} --output datasets/{}_output_got.csv'

start = time.mktime(time.strptime(start_date, t_format))
end = time.mktime(time.strptime(end_date, t_format))
step = 3 * 30 * 24 * 3600
to = start + step
metric_s = time.time()
with open('fail.log', 'a') as f:
    while start < end:
        start_date = time.strftime(t_format, time.localtime(start))
        to_date = time.strftime(t_format, time.localtime(to))
        print('Processing: ' + start_date + '_' + to_date)
        cmd = base_cmd.format(start_date, to_date, maxtweets, start_date + '_' + to_date)
        try:
            subprocess.check_call(cmd.split(), stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            f.write('Crawling failed! start={}, end={}, error={}\n'.format(start_date, to_date, e.message))
            f.flush()
        start = to
        to += step
metric_e = time.time()
print('Consume time {} hours.'.format((metric_e - metric_s) / 3600.0))