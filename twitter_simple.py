#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy
import codecs
import os
import re
import sys
import datetime

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

#ツイートする間隔(分)
time = 10

# coupleクラス
class Couple():
    def __init__(self,_date,_username,_text):
        self.date     = _date;
        self.username = _username;
        self.text     = _text;
# Brokenクラス
class Broken():
  def __init__(self,_date,_username, _text):
    self.date    = _date;
    self.username= _username;
    self.text    = _text;

# 取得したデータ(Coupleクラス Brokenクラス)の配列
CoupleList = []
BrokenList = []

sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

# 検索してデータを格納
couple_keyword = u'付き合いました OR 付き合う -RT'
broken_keyword = u'別れました OR 別れた -RT' #either 別れた or 別れました RTは除く

for tweet in api.search(q=couple_keyword, count=100):
    if re.search(u'bot', tweet.user.screen_name):
        pass
    else:
        CoupleList.append(Couple(tweet.created_at, tweet.user.screen_name, tweet.text))

for tweet in api.search(q=broken_keyword, count=100):
  #print tweet.created_at, tweet.user.screen_name, tweet.text
  if re.search(u'bot', tweet.user.screen_name):  #ignore twitter bot
      pass
  else:
      BrokenList.append(Broken(tweet.created_at, tweet.user.screen_name, tweet.text))

fp_C = open('Couple_output.txt','w')
fp_B = open('Broken_output.txt','w')


# 表示
for couple in CoupleList:
    if datetime.datetime.now() - (couple.date + datetime.timedelta(hours=9)) <= datetime.timedelta(minutes=time):
        fp_C.write(couple.text.encode('euc-jp','replace').replace('\n', '') + "\n")
    else:
        fp_C.write("HERE\n")

for broken in BrokenList:
    #print (broken.date + datetime.timedelta(hours=9))
  if datetime.datetime.now() - (broken.date + datetime.timedelta(hours=9)) <= datetime.timedelta(minutes=time):
    #print broken.date, broken.username, broken.text.replace('\n', '')
    fp_B.write(broken.text.encode('euc-jp','replace').replace('\n', '') + "\n")
  else:
    fp_B.write("HERE\n")

fp_C.close()
fp_B.close()

# chasenをかける
os.system('chasen < Couple_output.txt > Couple_output.txt.chasen')
os.system('chasen < Broken_output.txt > Broken_output.txt.chasen')

#ツイートに人名があるかどうかのboolean
has_broken_name = False
has_couple_name = False
#ツイート内容に付き合ったか別れたかが含まれているかを判断するboolean
has_couple = False
has_break = False
#イニシャルを格納する配列
initial_couple = []
initial_broken = []
#付き合ったり、別れたりしたカップルの数を入れる変数
count_couple = 0
count_broken = 0

#名前からイニシャルにする関数
def NameToInitial(name,ListInitial): #（名前、イニシャルを入れる配列
    if re.search(ur"^[カキクケコ]", name):
            ListInitial.append("K")
    elif re.search(ur"^[サシスセソ]", name):
            ListInitial.append("S")
    elif re.search(ur"^[タチツテト]", name):
            ListInitial.append("T")
    elif re.search(ur"^[ナニヌネノ]", name):
            ListInitial.append("N")
    elif re.search(ur"^[ハヒヘホ]", name):
            ListInitial.append("H")
    elif re.search(ur"^[フ]", name):
            ListInitial.append("F")
    elif re.search(ur"^[マミムメモ]", name):
            ListInitial.append("M")
    elif re.search(ur"^[ヤユヨ]", name):
            ListInitial.append("Y")
    elif re.search(ur"^[ガギグゲゴ]", name):
            ListInitial.append("G")
    elif re.search(ur"^[ザジヂズヅゼゾ]", name):
            ListInitial.append("Z")
    elif re.search(ur"^[ダデド]", name):
            ListInitial.append("D")
    elif re.search(ur"^[バビブベボ]", name):
            ListInitial.append("B")
    elif re.search(ur"^[パピプペポ]", name):
            ListInitial.append("P")
    elif re.search(ur"^[ア]", name):
            ListInitial.append("A")
    elif re.search(ur"^[イ]", name):
            ListInitial.append("I")
    elif re.search(ur"^[ウ]", name):
            ListInitial.append("U")
    elif re.search(ur"^[エ]", name):
            ListInitial.append("E")
    elif re.search(ur"^[オ]", name):
            ListInitial.append("O")

# chasenを解析する
#couple
for line in codecs.open('Couple_output.txt.chasen','r','euc-jp'):
    line = line.rstrip('\r\n')
    if line == "EOS":
        if has_couple:
            count_couple += 1
            has_couple = False
            if has_couple_name:
                has_couple_name = False
                NameToInitial(couple_name,initial_couple)
    else:
        lis = line.split("\t")
        if re.search(ur"人名", lis[3]):
            if has_couple:
                if not has_couple_name:
                    couple_name = lis[1]
                    has_couple_name = True
            else:
                couple_name = lis[1]
                has_couple_name =True
        elif re.search(ur"付き",lis[0]):
            has_couple = True
#Broken
for line in codecs.open('Broken_output.txt.chasen','r','euc-jp'):
    line = line.rstrip('\r\n')
    if line == "EOS":
        if has_break:
            count_broken += 1 #カウンターを回す
            has_break = False 
            if has_broken_name:
                has_broken_name = False
                NameToInitial(broken_name,initial_broken)
    else:
        lis = line.split("\t")
        if re.search(ur"人名",lis[3]): #村井^Iムライ^I村井^I名詞-固有名詞-人名-姓^I^I
            if has_break:
                if not has_broken_name:
                    broken_name = lis[1]
                    has_broken_name = True
            else:
                broken_name = lis[1]
                has_broken_name = True

        elif re.search(ur"別れ",lis[0]):
            has_break = True


#ツイートする文章
if count_broken == 0: #別れた人がいない場合
    if count_couple == 0: #付き合った人もがいない場合
        text = u"この%d分で、別れたというツイートをした人も、付き合ったというツイートをした人はいません。\n\nしたがって、残念ながら新しい恋のチャンスは、誰にも訪れないでしょう。" % time 
    else: #付き合った人がいる場合
        if len(initial_couple) == 0: #イニシャルを一つも取得してない場合
            text = u"この%d分で、別れたというツイートをした人はいません。\n\nしかし、付き合ったという内容のツイートした人は、%d人います。\n\nこれにより、%d人の人の恋のチャンスが失われたと見込まれています。" %(time, count_couple,count_couple*2)
        else: #イニシャルを一つ以上取得している場合
            text = u"この%d分で、別れたというツイートをした人はいません。\n\nしかし、付き合ったという内容のツイートした人は、%d人いて、\n" %(time, count_couple)
            for i in initial_couple:
                text += i + u"さん、"
            text += u"この%d人は、確実に付き合い始めたと言えるでしょう。\n\nこれにより、%d人の人の恋のチャンスが確実になくなりました" % (len(initial_couple),len(initial_couple)+2)
else: #別れた人がいる場合
    if count_couple ==0: #付き合った人がいない場合
        if len(initial_broken) == 0: #イニシャルを一つも取得してない場合
            text = u"この%d分で、別れたというツイートをした人は%d人です。\n\nまた、付き合ったというような内容のツイートをした人はいません。\n\nこれにより、%d人の人に新しい恋のチャンスが訪れるかもしれません。" %(time, count_broken, count_broken*2)
        else: #イニシャルを一つ以上取得している場合
            text = u"この%d分で、別れたというツイートをした人は%d人で、付き合ったというような内容のツイートをした人はいません。\n\nまた、" %(time, count_broken)
            for i in initial_broken:
                text += i + u"さん、"
            text += u"この%d人は、失恋をしただろうと断言できます。\n\nしたがって、%d人の人に新しい恋のチャンスが確実に訪れます" %(len(initial_broken), len(initial_broken)*2)
    else: #付き合った人がいる場合
        if len(initial_broken) == 0: #別れた人のイニシャルを一つも取得してない場合
            if len(initial_couple) == 0: #付き合った人のイニシャルを一つも取得してない場合
                text = u"この%d分で、%d人の人が付き合ったというようなツイートをし、%d人の人が別れたという内容のツイートをしました。\n\nしたがって、" %(time, count_couple, count_broken)
                if count_couple > count_broken: #付き合った人がわかれた人より多い場合
                    text += u"%d人の人の恋のチャンスがなくなりました" %(count_couple - count_broken)*2
                elif count_broken > count_couple: #別れた人が付き合った人より多い場合
                    text += u"%d人の人に新しい恋のチャンスが訪れるかもしれません" %(count_broken - count_couple)*2
                elif count_broken == count_couple: #わかれた人数と付き合った人数が同じ場合
                    text += u"誰にも恋のチャンスは訪れません"
            else: #付き合った人のイニシャルを取得している場合
                text = u"この%d分で、%d人の人が付き合ったというようなツイートをし、%d人の人が別れたというようなツイートをしました。\n\nこれより、" %(time, count_couple, count_broken)
                if count_couple > count_broken: #付き合った人がわかれた人より多い場合
                    text += u"%d人の人は恋のチャンスがなくなったと思われます。\n\nただ、" %(count_couple - count_broken)*2
                elif count_broken > count_couple: #別れた人が付き合った人より多い場合
                    text += u"%d人の人に新しい恋のチャンスが訪れるかもしれません。\n\nただ、" %(count_broken - count_couple)*2
                elif count_broken == count_couple: #わかれた人数と付き合った人数が同じ場合
                    text += u"誰にも恋のチャンスは訪れません。\n\nただ、"
                for i in initial_couple:
                    text += i + u"さん、"
                text += u"この%d人は、確実に付き合い始めたと言えます。\n\nしたがって、残念ながら%d人の人は確実に恋のチャンスがなくなりました。" %(len(initial_couple), len(initial_couple)*2)
        else: #別れた人のイニシャルを一つ以上取得してい場合
            text = u"この%d分で、%d人の人が付き合ったというようなツイートをし、%d人の人が別れたというようなツイートをしました。\n\nよって、" %(time, count_couple, count_broken)
            if len(initial_couple) == 0: #付き合った人のイニシャルを一つも取得していない場合
                if count_couple > count_broken: #付き合った人がわかれた人より多い場合
                    text += u"%d人の人の恋のチャンスがなくなったと思われます。\n\nただ、" %(count_couple - count_broken)*2
                elif count_broken > count_couple: #別れた人が付き合った人より多い場合
                    text += u"%d人の人に新しい恋のチャンスが訪れるかもしれません。\n\nただ、" %(count_broken - count_couple)*2
                elif count_broken == count_couple: #わかれた人数と付き合った人数が同じ場合
                    text += u"誰にも恋のチャンスは訪れないでしょう。\n\nただ、"
                or i in initial_broken:
                    text += i + u"さん、"
                text += u"この%d人は、確実に破局してます。\n\nしたがって、幸運なことに%d人の人には確実に新しい恋のチャンスがやってきます。" %(len(initial_broken),len(initial_broken)*2)
            else: #付き合った人のイニシャルを一つ以上取得している場合
                for i in initial_couple:
                    text += i + u"さん、"
                text += u"この%d人は、確実に付き合い始めたと言えるでしょう。\n\nそして、" %len(initial_couple)
                for i in initial_broken:
                    text += i + u"さん、"
                text += u"この%d人は、確実に破局したと言えるでしょう。\n\nしたがって、" %len(initial_broken)
                if count_couple > count_broken: #付き合った人がわかれた人より多い場合
                    text += u"%d人の人の恋のチャンスがなくなりました" %(count_couple - count_broken)*2
                elif count_broken > count_couple: #別れた人が付き合った人より多い場合
                    text += u"%d人の人に新しい恋のチャンスが訪れるかもしれません" %(count_broken - count_couple)*2
                    text += "done"
                elif count_broken == count_couple: #わかれた人数と付き合った人数が同じ場合
                    text += u"誰にも恋のチャンスは訪れません"

print text


# 一旦false
if False:
    # ツイートを送信
    try:
        api.update_status(status=text)
        count_broken = 0
        count_couple = 0
    except tweepy.TweepError as e:
        print e
