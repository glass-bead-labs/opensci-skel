#!/usr/bin/env python

'''analysis.py - intended to be run by Dexy, can also be run stand-alone'''

from analysis_support import ProcessedData

data = ProcessedData('raw-data/rts.csv')

# This is not the right way to use Jinja2, but for now it's good enough
print('### De-identified raw data\n')
print(data.df.to_html(index=False))
diff_txt = data.diff_std_err('RT')
# HTML does not care about newlines
print(diff_txt.replace('\n', '<br>'))

data.pre_post_plot('RT', 'RT_plot.png')
