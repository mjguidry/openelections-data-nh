# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 19:56:36 2016

@author: mike
"""

import xlrd, re
import csv
import requests, tempfile
urls=['http://sos.nh.gov/WorkArea/DownloadAsset.aspx?id=26699',
      'http://sos.nh.gov/WorkArea/DownloadAsset.aspx?id=26700',
      'http://sos.nh.gov/WorkArea/DownloadAsset.aspx?id=26701',
      'http://sos.nh.gov/WorkArea/DownloadAsset.aspx?id=26702',
      'http://sos.nh.gov/WorkArea/DownloadAsset.aspx?id=26703',
      'http://sos.nh.gov/WorkArea/DownloadAsset.aspx?id=26704',
      'http://sos.nh.gov/WorkArea/DownloadAsset.aspx?id=26705',
      'http://sos.nh.gov/WorkArea/DownloadAsset.aspx?id=26706',
      'http://sos.nh.gov/WorkArea/DownloadAsset.aspx?id=26707'
      ]

tempdir=tempfile.tempdir
tmp_file=tempdir+'/temp_nh.xls'
rep_dir='../'

# Get town to county matchups from President run
import pickle
f=open('county.pkl','rb')
county_dict=pickle.load(f)
f.close()


results_dict=dict()
cols_dict=dict()
candidates=['Cilley','Hassan','Kennedy','Lamontagne','Smith','Tarr','Scatter']
candidate_dict={'Cilley':{'name':'Jackie Cilley' ,
                          'party':'D',
                          'winner':False},
                'Hassan' :{'name':'Maggie Hassan',
                          'party':'D',
                          'winner':True},
                'Kennedy' :{'name':'Bill Pearce Kennedy',
                            'party':'D',
                            'winner':False},
                'Lamontagne':{'name':'Ovide Lamontagne' ,
                         'party':'R',
                         'winner':False},
                'Smith' :{'name':'Kevin H. Smith',
                         'party':'R',
                         'winner':False},
                'Tarr' :{'name':'Robert M. Tarr',
                          'party':'R',
                          'winner':False},
                'Scatter' :{'name':'Scatter',
                            'party':'',
                            'winner':False}}




for url in urls:
    resp = requests.get(url)
    output = open(tmp_file, 'wb')
    output.write(resp.content)
    output.close()
    header_row=0
    wb=xlrd.open_workbook(tmp_file,formatting_info=True)
    sheets = wb.sheet_names()
    for sheet in sheets:
        start_flag=0
        stop_flag=1
        ws = wb.sheet_by_name(sheet)
        for row in range(ws.nrows):
            if(start_flag==1 and stop_flag==0):
                if('TOTALS' in ws.cell(row,0).value):
                    stop_flag=1
                else:
                    town=ws.cell(row,0).value
                    town=re.sub('\s+\Z','',town)
                    town=re.sub('\*','',town)
                    results_dict[town]=dict()
                    for col in cols_dict:
                        candidate=cols_dict[col]
                        value=ws.cell(row,col).value
                        if(value=='' or value==' '):
                            results_dict[town][candidate]=0
                        else:
                            results_dict[town][candidate]=int(value)
            try:
                if('County' in ws.cell(row,0).value):
                    value=ws.cell(row,0).value
                    start_flag=1
                    stop_flag=0
                    county=re.search('.*(?=\sCounty)',value).group(0)
                    for col in range(1,ws.ncols):
                        candidate=[x for x in candidates if x in ws.cell(row,col).value][0]
                        cols_dict[col]=candidate
            except:
                pass


# Clean up multiple wards into one set of results per town
wards=[x for x in results_dict.keys() if 'Ward' in x]
towns=set([re.search('.*(?=\sWard)',x).group(0) for x in wards])
for town in towns:
    results_dict[town]=dict()
    town_wards=[x for x in wards if town in x]
    for candidate in candidates:
        results_dict[town][candidate]=sum([results_dict[x][candidate] for x in town_wards])
    for ward in town_wards:
        del results_dict[ward]

for town in results_dict.keys():
    results_dict[town]['county']=county_dict[town]

# Debug print statements
# print 'Hassan results ', sum([results_dict[x]['Hassan'] for x in results_dict.keys()])
# print 'Cilley results ', sum([results_dict[x]['Cilley'] for x in results_dict.keys()])


csvfile=open(rep_dir+'/20120911__nh__democratic__primary__governor__town.csv','wb')
csvwriter=csv.writer(csvfile)
csvwriter.writerow(['town',
                    'county',
                    'office', 
                    'district', 
                    'party', 
                    'candidate',
                    'winner',
                    'votes'])
for candidate in candidates:
    for town in sorted(results_dict.keys()):
        csvwriter.writerow([town,
                            results_dict[town]['county'],
                            'Governor',
                            '',
                            candidate_dict[candidate]['party'],
                            candidate_dict[candidate]['name'],
                            candidate_dict[candidate]['winner'],
                            results_dict[town][candidate]
                            ])

csvfile.close()

csvfile.close()