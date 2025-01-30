from newsapi import NewsApiClient
import pandas as pd
# Init
newsapi = NewsApiClient(api_key='e4efc08d206a4eae828feeea9d62dceb')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='deepseek')
                                          # sources='bbc-news,the-verge',
                                          # category='business',
                                          # language='en',
                                          # country='us')

# # /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      # from_param='2017-12-01',
                                      # to='2017-12-12',
                                      language='en',
                                      # sort_by='relevancy',
                                      # page=2)
                                      )
# df = pd.DataFrame(top_headlines, columns=['title', 'url'])
# /v2/top-headlines/sources
sources = newsapi.get_sources()

articles = top_headlines['articles']
disc = articles[0]
print()