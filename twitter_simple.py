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
keywords = u'別れ(まし)*た -RT' #either 別れた or 別れました
for tweet in api.search(q=keywords, count=10):
  #tweet.created_at, tweet.user.screen_name, tweet.text
  if re.search(u'bot', tweet.user.screen_name):  #ignore tweets starting with RT @[alphanum]::: これは 検索キーワードのところで -RTを入れれば可能 or with username with bot
      pass
  else:
      BrokenList.append(Broken(tweet.created_at, tweet.user.screen_name, tweet.text))

fp = codecs.open('output.txt','w','utf-8')

# 表示
for broken in BrokenList:
    print broken.date, broken.username, broken.text
    fp.write(broken.text + "\n")

fp.close()

# 外部コマンドの実行には `os.system()` を使う
os.system('chasen < output.txt > output.txt.chasen')

# 人名の一文字目を格納する配列
has_name = False
has_break = False
initial = []
count = 0

# 練習問題3(第4回課題)を参照
for line in codecs.open('output.txt.chasen','r','utf-8'):
    line = line.rstrip('\r\n')
    if line == "EOS":
        if has_break:
            count += 1 #カウンターを回す
            has_break = False 
            if has_name:
                has_name = False
                if re.search(ur"^[カキクケコ]", name):
                        initial.append = "K"
                elif re.search(ur"^[サシスセソ]", name):
                        initial.append = "S"
                elif re.search(ur"^[タチツテト]", name):
                        initial.append = "T"
                elif re.search(ur"^[ナニヌネノ]", name):
                        initial.append = "N"
                elif re.search(ur"^[ハヒヘホ]", name):
                        initial.append = "H"
                elif re.search(ur"^[フ]", name):
                        initial.append = "F"
                elif re.search(ur"^[マミムメモ]", name):
                        initial.append = "M"
                elif re.search(ur"^[ヤユヨ]", name):
                        initial.append = "Y"
                elif re.search(ur"^[ガギグゲゴ]", name):
                        initial.append = "G"
                elif re.search(ur"^[ザジヂズヅゼゾ]", name):
                        initial.append = "Z"
                elif re.search(ur"^[ダデド]", name):
                        initial.append = "D"
                elif re.search(ur"^[バビブベボ]", name):
                        initial.append = "B"
                elif re.search(ur"^[パピプペポ]", name):
                        initial.append = "P"
                elif re.search(ur"^[ア]", name):
                        initial.append = "A"
                elif re.search(ur"^[イ]", name):
                        initial.append = "I"
                elif re.search(ur"^[ウ]", name):
                        initial.append = "U"
                elif re.search(ur"^[エ]", name):
                        initial.append = "E"
                elif re.search(ur"^[オ]", name):
                        initial.append = "O"
    else:
        lis = line.split("\t")
        if re.search(ur"人名",lis[3]): #村井^Iムライ^I村井^I名詞-固有名詞-人名-姓^I^I
            name = lis[1]
            has_name = True
        elif re.search(ur"別れ",lis[0]):
            has_break = True

#ツイートする文章
if count == 0:
    text = u"この30分で、破局したカップルはいません。したがって、残念ながら新しいチャンスは、誰にも訪れないでしょう。"
else:
    if len(initial) == 0:
        text = u"この30分で、破局したカップルの数は%dです。これにより、%d人の人に新しいチャンスが訪れるでしょう" %(count, count*2)
    else:
        text = u"この30分で、"
    
        for str in initial:
            text += initial + u"さん、"

        text += u"が別れました。この３０分で破局したカップルの数は%dです。これにより、%d人の人に新しいチャンスが訪れるでしょう" %(count, count*2)

print text


# 一旦false
if False:
    # ツイートを送信
    try:
        api.update_status(status=text)
        count = 0
    except tweepy.TweepError as e:
        print e
