#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy

consumer_key        = 'tMW349UNzlmIRztNIyp8coJSa'
consumer_secret     = '3h5sUb2WJC1jaGflGPvuvxJ0vGh5VYXq4qmoyAmTQdD5sRraGI'
access_token        = '4620166219-RfRL8kwOJbQ9tuHZLWhDYTP5CoufZ1joUJWFkXd'
access_token_secret = 'B7CD5FxXwoeiTNXWbOrklmUWacfwFOE8yFm6Qe98LunTp'

# Twitter OAuth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

# Twitter API
api = tweepy.API(auth)

# Mentionの取得
# 自分宛てのツイートを取得して表示
#mentions = api.home_timeline(count=10)
#for tweet in mentions:
#    print tweet.user.screen_name, tweet.text

# 検索して表示する
keywords = u'別れました'
for tweet in api.search(q=keywords, count=10):
    print tweet.created_at, tweet.user.screen_name, tweet.text

if False:
    # ツイートを送信
    try:
        api.update_status(status='Hello, world!')
        # api.update_status(status=u'こんにちは世界さん')
    except tweepy.TweepError as e:
        print e
