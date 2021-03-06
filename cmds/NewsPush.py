import asyncio
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import time
import os
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import pymysql
pymysql.install_as_MySQLdb()

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
class NewsPush(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        dateRange = []
        info = []
        char_1 = []
        char_2 = []
        status = "有新資料"
        channel_Num = int(os.environ.get('CHANNEL_NEWSBOARD_FROM_4700'))
        while True:
            self.connect()
            channel_newsBoard = self.bot.get_channel(channel_Num)
            resultF = await self.crawler()
            if resultF is not None:
                info = resultF[0]
                char_1 = resultF[1]
                char_2 = resultF[2]
                dateRange = resultF[3]
            if len(char_1) >= 19:
                embed=discord.Embed(title="{} ~ {}".format(dateRange[0],dateRange[1]), url=info[2], description=char_1[19])
                embed.set_author(name=info[0], url=info[2])
                embed.set_image(url=char_1[0])
                #embed.set_thumbnail(url=char_1[0])
                embed.add_field(name="Lv.", value=char_1[2], inline=True)
                embed.add_field(name="HP.", value=char_1[4], inline=True)
                embed.add_field(name="ATK.", value=char_1[6], inline=True)
                embed.add_field(name="EX", value=char_1[9], inline=False)
                embed.add_field(name="S1.{}".format(char_1[7]), value=char_1[13], inline=False)
                embed.add_field(name="S2.{}".format(char_1[8]), value=char_1[14], inline=False)
                embed.add_field(name="被動1.{}".format(char_1[10]), value=char_1[16], inline=False)
                embed.add_field(name="被動2.{}".format(char_1[11]), value=char_1[17], inline=False)
                embed.add_field(name="被動3.{}".format(char_1[12]), value=char_1[18], inline=False)
                embed.set_image(url=char_1[0])
                await channel_newsBoard.send(embed=embed)
                #if msg.channel == channel_newsBoard:
                #    await msg.channel.send(embed=embed)
                if len(char_2) != 0:
                    embed=discord.Embed(title="{} ~ {}".format(dateRange[0],dateRange[1]), url=info[2], description=char_2[19])
                    embed.set_author(name=info[0], url=info[2])
                    embed.set_image(url=char_2[0])
                    #embed.set_thumbnail(url=char_1[0])
                    embed.add_field(name="Lv.", value=char_2[2], inline=True)
                    embed.add_field(name="HP.", value=char_2[4], inline=True)
                    embed.add_field(name="ATK.", value=char_2[6], inline=True)
                    embed.add_field(name="EX", value=char_2[9], inline=False)
                    embed.add_field(name="S1.{}".format(char_2[7]), value=char_2[13], inline=False)
                    embed.add_field(name="S2.{}".format(char_2[8]), value=char_2[14], inline=False)
                    embed.add_field(name="被動1.{}".format(char_2[10]), value=char_2[16], inline=False)
                    embed.add_field(name="被動2.{}".format(char_2[11]), value=char_2[17], inline=False)
                    embed.add_field(name="被動3.{}".format(char_2[12]), value=char_2[18], inline=False)
                    embed.set_image(url=char_2[0])
                    await channel_newsBoard.send(embed=embed)
    def connect(self):
        self.mydb = pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        passwd=os.environ.get('DB_PASSWD'),
        db=os.environ.get('DB_NAME')
        )
    def query(self, sql):
        try:
            cursor = self.mydb.cursor()
            cursor.execute(sql)
        except:
            self.connect()
            cursor = self.mydb.cursor()
            cursor.execute(sql)
        self.mydb.commit()
        return cursor
    async def crawler(self):
        dateRange = []
        info = []
        char_1 = []
        char_2 = []
        status = "有新資料"
        #@commands.Cog.listener()
        #async def on_message(self, msg):
        #    if ((msg.content =='最新卡池資訊') and msg.author != self.bot.user):
                #driver = webdriver.Chrome('./chromedriver')
        driver.get('https://dragalialost.com/cht/news/information/')
        await asyncio.sleep(5)
        soup = BeautifulSoup(driver.page_source,'lxml')
        #p =driver.find_element_by_id('news-list')
        cnt = 0
        info = []
        for i in soup.select('li a p.title'):
            texts = i.text.strip()
            #print(texts)
            group1 = re.search(r'(失落龍絆日|傳說召喚|精選召喚).*(舉辦公告)',texts)
            if group1:
                p=texts
                info.append(p)   #標題丟進info[0]
                #cursor = mydb.cursor()
                #cursor.execute('SELECT * FROM titletable WHERE titleName = %s',info[0])
                #result = cursor.fetchall()
                #if len(result) != 0:
                #    NewsPush.timeSleep()
                break
            cnt = cnt +1
        n=0
        for data in soup.select('li a div.time'):
            #if(n>=2):
            #    break
            if n == cnt:
                info.append(data.text.split('公告')[0].strip())
            n=n+1
        #print(info)
        cnt1 = 0
        path_ = 'https://dragalialost.com/cht/news/information/'
        for i in soup.select('div ul#news-list li a'):
            #print(i.get('href'))
            if cnt1 == cnt:
                path_ = 'https://dragalialost.com' + i.get('href')
                info.append(path_)
                tmp = path_.split('/')
                info.append(tmp[len(tmp)-1])
                break
            cnt1 = cnt1 +1
        #print(info)
        #path_ = 'https://dragalialost.com' + soup.select_one('div ul#news-list li a').get('href')
        #info.append(path_)
        #tmp = path_.split('/')
        #info.append(tmp[len(tmp)-1])
        #info
        ###driver.get('https://dragalialost.com/cht/news/detail/935')
        print('info = {}'.format(info))
        driver.get(path_)
        #driver.get(info[2])
        await asyncio.sleep(3)
        soup = BeautifulSoup(driver.page_source,'lxml')
        dateRange = []
        for date in soup.select('div span.local_date'):
            if date.text not in dateRange:
                dateRange.append(date.text)
        dateRange
        print("開始檢驗是否重複")
        try:
            titleName = info[0]
            titleTimeStart = dateRange[0]
            titleTimeEnd = dateRange[1]
        except:
            titleName = ''
            titleTimeStart = ''
            titleTimeEnd = ''
        #cursor = mydb.cursor()
        sql = "SELECT titleName FROM titletable WHERE titleName = '{}'".format(titleName)
        cursor = self.query(sql)
        #cursor.execute(sql)
        #time.sleep(1)
        result = cursor.fetchall()
        print("抓到資料庫中的 titleName = {}".format(result))
        if result is not None:
            try:
                result = "".join(result[0])
                print("抓到資料庫中的 titleName(after join) = {}".format(result))
                result = result.split('\'')[0]
            except:
                pass
            #print("抓到資料庫中的 titleName(after join) = {}".format(result))
            #result = result.split('\'')[0]
            #cursor = mydb.cursor()
            sql = "SELECT titleTimeStart FROM titletable WHERE titleName = '{}'".format(titleName)
            cursor = self.query(sql)
            #cursor.execute(sql)
            #time.sleep(1)
            resultTime = cursor.fetchall()
            if resultTime is not None:
                try:
                    resultTime = "".join(resultTime[0])
                    print("抓到資料庫中的 titleTimeStart(after join) = {}".format(resultTime))
                    resultTime = resultTime.split('\'')[0]
                except:
                    resultTime = ''
            print("抓到資料庫中的 titleTimeStart = '{}', 目前現有的 dateRange[0] = '{}', 開始進行比對".format(resultTime,titleTimeStart))
            if resultTime == titleTimeStart:
                print("等待10分鐘後重爬")
                await asyncio.sleep(592)
                print("等待10分鐘完畢,重新開始")
                status = "無新資料"
        if status == "有新資料":
            print("From NewsPush.py : 已爬到卡池資訊,未重複,開始爬資料")
            #cursor = mydb.cursor()
            sql = "INSERT INTO titletable (titleName,titleTimeStart,titleTimeEnd) VALUE ('{}','{}','{}')".format(titleName,titleTimeStart,titleTimeEnd)
            cursor = self.query(sql)
            #cursor.execute(sql)
            #sql = "UPDATE `titletable` SET titleTimeStart = '{}' WHERE titleName = '{}'".format(titleTimeStart,titleName)
            #sql = "INSERT INTO titletable (`titleTimeStart`) VALUE ('{}') WHERE `titleName` = '{}'".format(titleTimeStart,titleName)
            #cursor = self.query(sql)
            #cursor.execute(sql)
            #sql = "UPDATE `titletabl`e SET `titleTimeEnd` = '{}' WHERE `titleName` = '{}'".format(titleTimeEnd,titleName)
            #sql = "INSERT INTO titletable (`titleTimeEnd`) VALUE ('{}') WHERE `titleName` = '{}'".format(titleTimeEnd,titleName)
            #cursor = self.query(sql)
            #self.mydb.commit()
            #cursor.execute(sql)
            #result = cursor.fetchall()
            charskillTitle_1 = []
            charskillTitle_2 = []
            tmp = 0
            for skillTitle in soup.select('dl dt span'):  #技能&被動名稱
                if skillTitle.text.strip() != '':
                    if tmp < 6 :
                        charskillTitle_1.append(skillTitle.text.strip())
                    else:
                        charskillTitle_2.append(skillTitle.text.strip())
                    tmp = tmp +1
                #print(skillParam.text.strip())
            #print(charskillTitle_1)
            #print(charskillTitle_2)
            #print('\n\n')

            skillExAbility_1 = []
            skillExAbility_2 = []
            tmp = 0
            for skillParam in soup.select('dl dd div'):   #技能&ex&被動描述
                if tmp < 6 :
                    skillExAbility_1.append(skillParam.text.strip())
                else:
                    skillExAbility_2.append(skillParam.text.strip())
                tmp = tmp +1
                #print(skillParam.text.strip())
            #print(skillExAbility_1)
            #print(skillExAbility_2)
            #print('\n\n')

            charLv_1 = []
            charLv_2 = []
            tmp = 0
            for lv in soup.select('div ul li.lv'):        #等級
                a = lv.text.split('\n')[1]
                b = lv.text.split('\n')[2]
                if tmp <1 :
                    charLv_1.append(a)
                    charLv_1.append(b)
                else:
                    charLv_2.append(a)
                    charLv_2.append(b)
                tmp = tmp +1
                #print(lv.text.strip())
            #print(charLv_1)
            #print(charLv_1)
            #print('\n\n')

            charHp_1 = []
            charHp_2 = []
            tmp = 0
            for hp in soup.select('div ul li.hp'):        #hp
                a = hp.text.split('\n')[1]
                b = hp.text.split('\n')[2]
                if tmp <1 :
                    charHp_1.append(a)
                    charHp_1.append(b)
                else:
                    charHp_2.append(a)
                    charHp_2.append(b)
                tmp = tmp +1
                #print(hp.text.strip())
            #print(charHp_1)
            #print(charHp_2)
            #print('\n\n')

            charAtk_1 = []
            charAtk_2 = []
            tmp = 0
            for atk in soup.select('div ul li.atk'):        #atk
                a = atk.text.split('\n')[1]
                b = atk.text.split('\n')[2]
                if tmp <1 :
                    charAtk_1.append(a)
                    charAtk_1.append(b)
                else:
                    charAtk_2.append(a)
                    charAtk_2.append(b)
                tmp = tmp +1
                #print(hp.text.strip())
            #print(charAtk_1)
            #print(charAtk_2)
            #print('\n\n')

            charParam_1 = []
            charParam_2 = []
            tmp = 0
            for charParam in soup.select('div section div div div div div div.param ul li'): #角色介紹
                if tmp <1:
                    charParam_1.append(charParam.text.strip())
                else:
                    charParam_2.append(charParam.text.strip())
                tmp = tmp +1
            #print(charParam_1)
            #print(charParam_2)
            #print('\n\n')

            charPhoto_1 = []
            charPhoto_2 = []
            tmp = 0
            for photo in soup.select('div.mainImage img'):
                if tmp < 1:
                    charPhoto_1.append(photo.get('src'))
                else:
                    charPhoto_2.append(photo.get('src'))
                tmp = tmp +1
            driver.close()
            print(charPhoto_1)
            print(charPhoto_2)

            all_Status_1 = [charPhoto_1,charLv_1,charHp_1,charAtk_1,charskillTitle_1,skillExAbility_1,charParam_1]
            all_Status_2 = [charPhoto_2,charLv_2,charHp_2,charAtk_2,charskillTitle_2,skillExAbility_2,charParam_2]
            tmp_all = [all_Status_1,all_Status_2]
            char_1 = []
            char_2 = []
            tmp_final = [char_1,char_2]
            n=0
            for i in tmp_all:
                for q in i:
                    for p in q:
                        tmp_final[n].append(p)
                        #print(p)
                n=n+1
            #2019/11/12 14:00
            #傳說召喚「太糟糕啦☆愛之火☆乘車襲來」舉辦公告
            print(info,'\n')
            print(dateRange,'\n')
            print(char_1,'\n\n')
            print(char_2,'\n\n')

            print('角色照片:{}'.format(char_1[0]))
            print('角色介紹.{}'.format(char_1[19]))
            print('Lv.{}'.format(char_1[2]))
            print('HP.{}'.format(char_1[4]))
            print('ATK.{}'.format(char_1[6]))
            print('S1.{}'.format(char_1[7]))
            print('S1效果.{}'.format(char_1[13]))
            print('S2.{}'.format(char_1[8]))
            print('S2效果.{}'.format(char_1[14]))
            print('EX.{}'.format(char_1[9]))
            print('EX效果.{}'.format(char_1[15]))
            print('被動1.{}'.format(char_1[10]))
            print('被動1效果.{}'.format(char_1[16]))
            print('被動2.{}'.format(char_1[11]))
            print('被動2效果.{}'.format(char_1[17]))
            print('被動3.{}'.format(char_1[12]))
            print('被動3效果.{}'.format(char_1[18]))
            resultF = [info,char_1,char_2,dateRange]
            return resultF

def setup(bot):
    bot.add_cog(NewsPush(bot))
