#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy
import codecs
import os
import re
import sys

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

# Brokenクラス
class Broken():
  def __init__(self,_date,_username, _text):
    self.date    = _date;
    self.username= _username;
    self.text    = _text;

# 取得したデータ(Brokenクラス)の配列
BrokenList = []

sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

# 検索してデータを格納
keywords = u'別れ(まし)*た' #either 別れた or 別れました
for tweet in api.search(q=keywords, count=10):
  # print 'aaa'
  print tweet.created_at, tweet.user.screen_name, tweet.text
  BrokenList.append(Broken(tweet.created_at, tweet.user.screen_name, tweet.text))

print BrokenList

fp = codecs.open('output.txt','w','utf-8')

#一日に別れたカップルの数を格納する変数
count = 0

# 表示
for broken in BrokenList:
  if re.search(u'^RT @[a-zA-Z0-9_]*:', broken.text):  #ignore tweets starting with RT @[alphanum]:
   pass
  else:
    print broken.date, broken.username, broken.text
    # print 'aaa'
    fp.write(broken.text + "\n")
    count += 1
	
fp.close()

# 外部コマンドの実行には `os.system()` を使う
os.system('chasen < output.txt > output.txt.chasen')

# 人名を格納する配列
names = []

# 練習問題3(第4回課題)を参照
for line in codecs.open("output.txt.chasen","r","utf-8"):
  line = line.rstrip('\r\n')
  if line == "EOS":
    print names
    names = []
  else:
    lis = line.split("\t")
    if re.search(ur"人名",lis[3]):  #村井^Iムライ^I村井^I名詞-固有名詞-人名-姓^I^I
      names[line] = lis[0]

#tweetする文章
#どんな感じの文章がいいんでしょうか。。。
#text = u"【速報】先ほど%dさんが破局しました！" % (name) 
#text = u"この１時間で、%d個のカップルが破局しました。これにより、%d人の人に新しいチャンスが訪れることになります" %(count, count*2)


# 一旦false
if False:
  # ツイートを送信
    try:
      api.update_status(status=text)
      count = 0 #変数をリセット
    except tweepy.TweepError as e:
      print e
