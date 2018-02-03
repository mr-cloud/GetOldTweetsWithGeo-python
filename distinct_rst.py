import os


print('Task started.')

tweets_set = set()
dir_targets = ['datasets-0', 'datasets-1']

with open('dist_rst.txt', 'w') as dist_file:
    cnt = 0
    filtered = 0
    files = 0
    for dir_name in dir_targets:
        for filename in os.listdir(dir_name):
            print('Processing file: ' + filename)
            with open(os.path.join(dir_name, filename), 'r') as input_file:
                files += 1
                for line in input_file:
                    cnt += 1
                    line = line.strip()
                    sep_one = line.index(';')
                    sep_sec = line.index(';', sep_one+1)
                    key = line[:sep_sec]
                    if tweets_set.__contains__(key):
                        filtered += 1
                        continue
                    dist_file.write(line)
                    dist_file.write(os.linesep)
                    dist_file.flush()
                    tweets_set.add(key)
    print('Files = {}, all = {}, filtered = {}, disct = {}'.format(files, cnt, filtered, tweets_set.__len__()))
print('Task finished.')