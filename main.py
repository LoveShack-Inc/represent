import PyPDF2
import re
import pandas as pd
import sys

file = open('./data/2020SV-00052-R00HB06004-SV.PDF', 'rb')

fileReader = PyPDF2.PdfFileReader(file)

page = fileReader.getPage(0)
page_content = page.extractText()
page_content = page_content.replace('\n', '')
page_content += '\n'

reg_1 = re.compile('( Y | N )(.*?)(?= Y | N | \n)')
reg_result = re.findall(reg_1, page_content)
reg_2 = re.compile('[a-zA-Z .]')

date_reg = re.compile('(Taken on )(.*?)( )')
date_list = re.findall(date_reg, page_content)

num_reg = re.compile('(Vote for )(.*?)( Seq)')
num_list = re.findall(num_reg, page_content)

vote_name = sys.argv[1]

vote_list = []

for i in range(len(reg_result)):
    t1 = reg_result[i][0]
    t2 = "".join(re.findall(reg_2, reg_result[i][1])).strip()
    vote_list.append((t1, t2))

csv_file = pd.read_csv('./data/2020.csv')

csv_file['year'] = 2020
csv_file['date'] = date_list[0][1].replace('/', '_')
csv_file['bill_number'] = num_list[0][1]
csv_file['vote_name'] = vote_name
csv_file['rep_name'] = [x[1] for x in vote_list]
csv_file['rep_vote'] = [x[0] for x in vote_list]

csv_file.to_csv('2020.csv', index=False)
