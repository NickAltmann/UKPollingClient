import os
import urlparse
import datetime
import pandas as pd


class PollingClient(object):

    default_root = "https://ukpollingserver.scalingo.io/data/"
    local_root = "http://localhost:5000/data/"

    def __init__(self, url_root=None):
        self._url_root = url_root if url_root else self.default_root
        self._df_cache = dict()

    @property
    def parties(self):
        return self._get_df("parties")

    @property
    def leaders(self):
        return self._get_df("leaders")

    @property
    def general_elections(self):
        return self._get_df("general_elections")

    @property
    def in_power(self):
        return self._get_df("in_power")

    def get_leader_ratings(self, name):
        df = self.leaders.copy()
        df = df.loc[self.leaders.Item==name, :]
        df.loc[:, 'Net'] = df.loc[:, "Sat"] - df.loc[:, "Dis"]
        df.loc[:, 'DontKnow'] = 100 - df.loc[:, "Sat"] - df.loc[:, "Dis"]
        #df = df.set_index('Date')
        df = df[['Sat', 'Dis', 'Net', 'DontKnow']]
        return df

    def list_pollsters(self):
        return sorted(list(self.parties.Pollster.dropna().unique()))

    def list_parties(self):
        cols = set(self.parties.columns)
        s = cols.difference(set(['Pollster']))
        return sorted(list(s))

    def list_leaders(self):
        return sorted(self.leaders.Item.unique())

    def party_in_power(self, party, as_of_date):
        """Returns true if the given party was in power on the give date.  as_of_date should be a datetime object."""
        df = self.in_power
        s = df.apply(lambda x: x==1)[party]
        s = s[s.index<=as_of_date]
        return s.ix[-1]

    def compare_ratings(self, leaders, measure, trim_to_min=True):
        leader_ratings = [self._rebased_leader_rating(leader, measure) for leader in leaders]
        df = pd.concat(leader_ratings, axis=1)
        if trim_to_min:
            months = min([x.index[-1] for x in leader_ratings])
            df = df[df.index <= months]
        return df

    def monthly_average(self):
        df = self.parties.copy()
        df = df.drop(['Pollster'], axis=1)
        df = df.resample("MS").mean().dropna(how='all', axis=0)
        return df

    @staticmethod
    def _diff_month(d1, d2):
        return (d1.year - d2.year)*12 + d1.month - d2.month

    def _rebased_leader_rating(self, name, measure):
        df = self.get_leader_ratings(name)
        df = df[~df.index.duplicated(keep='first')]
        s = df[measure]
        ind = [self._diff_month(x, s.index[0]) for x in s.index]
        return pd.DataFrame(s.values, index = ind, columns=[name])


    @staticmethod
    def _full_path(root, filename):
        if os.path.isdir(root):
            path = os.path.join(root, filename + ".csv")
        else:
            path = urlparse.urljoin(root, filename)
        return path

    def _get_df(self, df_name):
        try:
            df = self._df_cache[df_name]
        except KeyError:
            path = self._full_path(self._url_root, df_name)
            df = pd.read_csv(path, parse_dates=["Date"])
            df = df.set_index("Date")
            self._df_cache[df_name] = df
        return df
