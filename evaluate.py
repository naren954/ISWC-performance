'''
To run in the script: python evaluate.py -f '<'file_paths'>' -c <'column_names'> -r <'round_numbers'> -g<'gt_path'> -o <'output_path'>
file_paths: space seperated file names
column_names: space seperated corresponding column names
round_numbers: space seperated corresponding round numbers (ISWC challenge rounds). If using files only from one round, do not have to repeat the round numbers. (As shown in example 2 below, both files belong to round 1)
gt_path: Path to directory containing all GT's (Path to data folder)
output_path: Output directory path

Usage examples: 
python evaluate.py -f '8468806_0_4382447409703007384.csv' -c 'Name' -r '1' -g '/Users/narendivvala/ISI' -o '/Users/narendivvala/ISI/Tests'

python evaluate.py -f '8468806_0_4382447409703007384.csv /Users/narendivvala/ISI/9475172_1_1023126399856690702.csv' -c 'Name Title' -r '1' -g '/Users/narendivvala/ISI/' -o '/Users/narendivvala/ISI/Tests'
'''


import os
import requests
import pandas as pd
import csv

from argparse import ArgumentParser
from io import StringIO
from urllib.parse import unquote


def decode_url(url):
    decodedurl = unquote(url)
    return decodedurl


def evaluate(GT,submission_file,outpath):
    gt=pd.read_csv(GT,names=['File','Col','Row','URI'],dtype=object)
    filename=submission_file['File'][0]
    column=submission_file['Col'][0]
    wrong_rows=[['Col','Row','Value','Submitted URI','Correct URI\'s']]
    gt=gt[gt['File']==filename]
    current_gt=gt[gt['Col']==column]
    total_submissions=len(current_gt['Col'].tolist())
    number_submitted=len(submission_file['Col'].tolist())
    correct_count=0
    for idx,row in submission_file.iterrows():
        row_number=row['Row']
        submitted_answer=row['URI']
        if len(current_gt[current_gt['Row']==row_number]['URI'].values)==0:
            continue
        expected_answers=set(decode_url(current_gt[current_gt['Row']==row_number]['URI'].values[0]).split())
        if submitted_answer in expected_answers:
            correct_count+=1
        else:
            wrong_rows.append([column,row_number,row['Value'],submitted_answer,
                              ' '.join(list(expected_answers))])
    precision=correct_count/number_submitted
    recall=correct_count/total_submissions
    f1=((precision*recall)/(precision+recall))*2
    filepath=outpath+filename+'_{}_report.csv'.format(column)
    wrong_rows.insert(0,['F1: {0:.5f}'.format(f1),'Precision: {0:.5f}'.format(precision),'Recall: {0:.5f}'.format(recall)])
    with open(filepath, 'w', newline='') as myfile:
        for row in wrong_rows:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(row)

        
def upload_files(file_path, url, column_name,outpath):
    file_name = os.path.basename(file_path)
    payload = {
        'columns': column_name,
        'case_sensitive': 'false',
    }
    files = {
        'file': (file_name, open(file_path, mode='rb'), 'application/octet-stream')
    }
    resp = requests.post(url, data=payload, files=files)
    s = str(resp.content, 'utf-8')
    data = StringIO(s)
    df = pd.read_csv(data)  
    col_number=pd.read_csv(file_path).columns.tolist().index(column_name)    
    _o=list()
    for idx,row in df.iterrows():
        _o.append([file_name[:-4],str(col_number),str(idx+1),str(row[column_name]),row['answer_dburi']])
    newdf=pd.DataFrame(_o,columns=['File','Col','Row','Value','URI'])
    newdf.to_csv(outpath+'{}_results.csv'.format(file_name[:-4]), index=False, header=False)
    return newdf


if __name__=='__main__':
    url = "http://localhost:7805/wikify"
    outpath=''
    gpath=''
    parser = ArgumentParser()
    parser.add_argument("-f", action="store", type=str, dest="files")
    parser.add_argument("-c", action="store", type=str, dest="columns")
    parser.add_argument("-r", action="store", type=str, dest="rounds")
    parser.add_argument("-o", action="store", type=str, dest="outpath")
    parser.add_argument("-g", action="store", type=str, dest="gpath")
    args, _ = parser.parse_known_args()
    files=args.files.split()
    columns=args.columns.split()
    rounds=args.rounds.split()
    outpath=args.outpath
    gpath=args.gpath
    if outpath!='' and outpath[-1]!='/':
        outpath+='/'
    if gpath!='' and gpath[-1]!='/':
        gpath+='/'
    if len(rounds)<len(files):
        for i in range(len(files)-len(rounds)):
            rounds.append(rounds[-1])
    for f,c,r in zip(files,columns,rounds):
        answers=upload_files(f,url,c,outpath)
        gtpath='data gt/Round {}/gt/CEA_Round{}_gt.csv'.format(r,r)
        evaluate(gpath+gtpath,answers,outpath)