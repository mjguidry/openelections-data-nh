# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 17:28:03 2016

@author: mike
"""


rep_dir='../'
csvfiles=['20120911__nh__democratic__primary__executive__council__town.csv',
          '20120911__nh__democratic__primary__governor__town.csv',
          '20120911__nh__democratic__primary__house__1__town.csv',
          '20120911__nh__democratic__primary__house__2__town.csv',
          '20120911__nh__democratic__primary__state__house__town.csv',
          '20120911__nh__democratic__primary__state__senate__town.csv',
          ]

outfile=rep_dir+'20120911__nh__democratic__primary__town.csv'
o=open(outfile,'wb')

for k,f_name in enumerate(csvfiles):
    f=open(rep_dir+f_name,'rb')
    if(k==0):
        start_line=0
    else:
        start_line=1
    for l,line in enumerate(f):
        if(l>=start_line):         
            o.write(line)
    f.close()

o.close()