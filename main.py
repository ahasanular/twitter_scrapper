import snscrape.modules.twitter as sntwitter
import pandas as pd

# query = "(from:elonmusk) until:2022-09-09 since:2010-01-01"
# tweets = []
# limit = 5

# for index, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
#
#     if index > limit:
#         break
#     tweets.append([tweet.url.split('/')[-1], tweet.content, pd.to_datetime(tweet.date).to_datetime64()])
#
# df = pd.DataFrame(tweets, columns=['Url', 'Text', 'Date'])
# df.to_excel('elon.xlsx')


class ScrapTwitter:
    def __init__(self, username, limit):
        self.username = username
        self.limit = limit

    query = None

    def make_query_string(self):
        return f'(from:{self.username})'

    def get_query_string(self):
        if self.query is not None:
            return self.query
        else:
            return self.make_query_string()

    def scrape_twitter_by_username(self):
        _tweet_list = []
        _error_log = []
        _query = self.get_query_string()
        for _index, _tweet in enumerate(sntwitter.TwitterSearchScraper(_query).get_items()):
            if _index > self.limit:
                break
            try:
                tw = [_tweet.url.split('/')[-1], _tweet.content, pd.to_datetime(_tweet.date).to_datetime64(), _tweet.json()]
                _tweet_list.append(tw)
                print(_index, tw)
            except Exception as ex:
                _error_log.append(f'{_index} >> {str(ex)}\n')
                continue

        return _tweet_list, _error_log

    @staticmethod
    def make_pandas_dataframe(tweet_list, *columns):
        try:
            return pd.DataFrame(tweet_list, columns=columns)
        except Exception as ex:
            return str(ex)

    @staticmethod
    def save_to_excel(df, excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True,
                      index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True,
                      encoding=None, inf_rep='inf', verbose=True, freeze_panes=None, storage_options=None):
        try:
            df.to_excel(excel_writer, sheet_name=sheet_name, na_rep=na_rep, float_format=float_format, columns=columns,
                    header=header, index=index, index_label=index_label, startrow=startrow, startcol=startcol,
                    engine=engine, merge_cells=merge_cells, encoding=encoding, inf_rep=inf_rep, verbose=verbose,
                    freeze_panes=freeze_panes, storage_options=storage_options)
            return excel_writer
        except Exception as ex:
            return str(ex)


elon = ScrapTwitter('elonmusk', 100000)
tweets, error = elon.scrape_twitter_by_username()
error_log = open('error.log', 'w')
error_log.write(''.join(error[:]))
error_log.close()
df = elon.make_pandas_dataframe(tweets, *['Url', 'Text', 'Date', 'json'])
elon.save_to_excel(df, f'{elon.username}_{elon.limit}.xlsx')
