# We're using python 2.7, so we want to be careful...
from __future__ import division
from __future__ import print_function

import pandas as pd

# I mostly care that the data are processed in the same way...
# But this isn't very dexy-rific
# print('Python', sys.version)
# print('Pandas', pd.version.version)

# This needs to come first if we're running remotely
import matplotlib.pyplot as plt
# To implement "categorical" labels
from matplotlib.ticker import FixedLocator


class ProcessedData:
    '''A class to organize the BahavData spreadsheet from KKI'''

    # Categoricals are a mild PITA
    ordered_time = ['pre', 'post']
    dummy_time = [0, 1]

    def __init__(self, fname, **kwargs):
        '''Read and anonymize a DataFrame

        We start with potentially identifying IDs This converts to a random ID
        - but a different method must be used if we wish to be able to do joins
        between files.
        '''
        df = pd.read_csv(fname, **kwargs)

        # use strings for IDs so they won't be included in a computation
        id_map = {old: str(i) for i, old in enumerate(set(df.ID))}
        self.df = df.drop('ID', axis=1)
        self.df['AnonID'] = [id_map[old] for old in df.ID]

    def pre_post_plot(self, colname, fname=None, ylabel=None):
        '''A basic pre-post plot

        colname : string
            Column name to plot.
        ylabel : string
            Alternate label for y-axis. Otherwise, `colname`.
        '''
        if ylabel is None:
            ylabel = colname

        # Compute means across pre-post values for colname, then re-order
        # according to ordered_time
        col_means = self.df.groupby('Time')[colname].mean()[self.ordered_time]

        # Unpack a 1-item list
        lines, = plt.plot(self.dummy_time, col_means)

        # matplotlib doesn't support true categorical labels, so we fake it
        xax = lines.axes.xaxis
        xax.set_label_text('Time')
        xax.set_major_locator(FixedLocator(self.dummy_time))
        xax.set_ticklabels(self.ordered_time)

        # These look reasonable and give an implicit sense of how big the
        # changes are, but could be adjusted
        plt.xlim([self.dummy_time[0] - 0.1, self.dummy_time[1] + 0.1])
        df_min = self.df[colname].min()
        df_max = self.df[colname].max()
        space = (df_max - df_min) * 0.05
        plt.ylim([df_min - space, df_max + space])

        plt.ylabel(ylabel)
        plt.tight_layout()

        if(fname):
            plt.savefig(fname, dpi=300, bbox_inches='tight')
            plt.clf()

        return lines

    def diff_std_err(self, colname):
        # We set the index here so pandas will ensure data is compared by ID
        # (this is different semantics than you'd get with an array)
        dfs = {ind: time_df.set_index('AnonID') for ind, time_df in
               self.df.groupby('Time')['AnonID', colname] }
        # We need to use `.as_matrix()` to get pandas to ignore the index
        diffs = dfs['post'][colname] - dfs['pre'][colname]
        # We use ddof=1 to compute an unbiased std estimate (not ML). Turns out
        # that's standard in statistical practice (but not numpy?).
        return 'mean: {:.3f}\nstd err: {:.3f}'.format(
            diffs.mean(), diffs.std(ddof=1) / pd.np.sqrt(4) )
