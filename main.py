from config import *
from passage import *
import re
import datetime

file_name = 'pattern.txt'
url = ['https://movie.douban.com/subject/5045678/reviews?start=%d' % n for n in range(0, 8000, 20)]
params = open(file_name).read().splitlines()
parser = {}
parser['pattern'] = params[0]
parser['position'] = params[1]

page_parser = {}
page_parser['pattern'] = params[2]
page_parser['position'] = params[3]

for surl in url:
    print(surl)
    page_list = Connection.xpath_parser(surl, parser)
    if page_list == []: continue
    for page in page_list:
        page['reply'] = re.sub("\D", "", page['reply'])
        print(page['passage_id'])
        detail_url = page['href']
        detail_result = Connection.bs4_parser(detail_url, page_parser)
        if detail_result != []:
            page['comment'] = detail_result[0]['comment']
            Passage.insert(page)
# tt = Connection.xpath_parser(url[0], parser)
# tt[0]['comment'] = 'xxx'
# tt[0]['reply'] = re.sub("\D", "", tt[0]['reply'])
# Passage.insert(tt[0])
# datetime('2016-07-11 10:51:06')
#print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  )
