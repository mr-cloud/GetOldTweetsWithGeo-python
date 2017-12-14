import os
from textblob import TextBlob
import json


data_dir = 'datasets.test'
schema = 'username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink'
format = '%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s'
BEFORE = ';"'
AFTER = '";'
DELIMITER = ';'
POS_THRESHOLD = 0.3
NEG_THRESHOLD = -0.3
date_format = '%Y-%m-%d %H:%M'
DATE_DEL = '-'
rst = {}
TOTAL_FIELD = 'total'
hashtag = 'TimesSquare'
rst_file = hashtag + '-' + 'rst.json'
with open(rst_file, 'w') as output:
    for file in os.listdir(data_dir):
        print('processing {}'.format(file))
        with open(os.path.join(data_dir, file)) as tweets:
            line_num = 0
            for line in tweets:
                if line_num == 0:
                    line_num += 1
                    continue
                line = line.decode('utf-8')
                try:
                    before_date = line.index(DELIMITER)
                    after_date = line.index(DELIMITER, before_date + len(DELIMITER))
                    dateStr = line[before_date + len(DELIMITER): after_date]
                    dateStr = dateStr.split(DATE_DEL)[0]
                    before_text = line.index(BEFORE) + len(BEFORE) - 1
                    after_text = line.index(AFTER, before_text + 1)
                    text = line[before_text + 1: after_text]
                    after_geo = line.index(DELIMITER, after_text + len(AFTER))
                    geoStr = line[after_text + len(AFTER): after_geo]
                except ValueError as ve:
                    print(ve)
                    continue

                polarity = TextBlob(text).sentiment.polarity

                geo_sup = 0
                geo_oppo = 0
                geo_vot = 0
                total_sup = 0
                total_oppo = 0
                total_vot = 0

                time = {}
                if rst.has_key(dateStr):
                    time = rst[dateStr]

                geo = []
                if time.has_key(geoStr):
                    geo = time[geoStr]

                total = []
                if time.has_key(TOTAL_FIELD):
                    total = time[TOTAL_FIELD]

                if len(geo) != 0:
                    geo_sup = geo[0]
                    geo_oppo = geo[1]
                    geo_vot = geo[2]
                if len(total) != 0:
                    total_sup = total[0]
                    total_oppo = total[1]
                    total_vot = total[2]

                if polarity > POS_THRESHOLD:
                    geo_sup += 1
                    total_sup += 1
                elif polarity < NEG_THRESHOLD:
                    geo_oppo += 1
                    total_oppo += 1
                else:
                    pass
                geo_vot += 1
                total_vot += 1

                if geoStr != '':
                    geo = [geo_sup, geo_oppo, geo_vot]
                    time[geoStr] = geo
                total = [total_sup, total_oppo, total_vot]
                time[TOTAL_FIELD] = total
                rst[dateStr] = time
    rstStr = json.dumps(rst)
    output.write(rstStr)
print('Task finished.')