import requests
import time
import jieba
import numpy as np
import lxml

from lxml import etree
from PIL import Image
# 词云制作
from wordcloud import WordCloud as wc

class Bilispider:

    def __init__(self,oid):
        self.headers = {
            'Host': 'api.bilibili.com',
		    'Connection': 'keep-alive',
		    'Cache-Control': 'max-age=0',
		    'Upgrade-Insecure-Requests': '1',
		    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0',
		    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		    'Accept-Encoding': 'gzip, deflate, br',
		    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		    'Cookie': "_uuid=35E7B0BA-69FE-ABB2-2484-09AB6A5057E147342infoc; buvid3=E9ECB0A3-21CF-40D9-90E3-E0A82F4BFBD8143098infoc; sid=cv7udy2d; DedeUserID=474809224; DedeUserID__ckMd5=e9f7965db976b3e2; SESSDATA=3072fa7b%2C1620145168%2C864bf*b1; bili_jct=ac2405bdf708e86db41ad8981c7af9e7; bp_t_offset_474809224=489971655843047306; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k|kmk)Jmlu0J'uY|RlmJum); PVID=1; bp_video_offset_474809224=489987091952549959; CURRENT_QUALITY=80; fingerprint3=60b0e0473b1d22b18bf0d0e611e5d68b; fingerprint=eff003d2e768bf025357cf45b8af9494; fingerprint_s=c5007fcc54b6e52da77c959aa6c1ea77; buivd_fp=E9ECB0A3-21CF-40D9-90E3-E0A82F4BFBD8143098infoc; buvid_fp_plain=E9ECB0A3-21CF-40D9-90E3-E0A82F4BFBD8143098infoc; kfcSource=unc_0201_message; msource=unc_0201_message; deviceFingerprint=cb4384bff5a98181fb8796bdda35ab12; bsource=search_bing; bfe_id=5db70a86bd1cbe8a88817507134f7bb5"
        }
        self.url = "https://api.bilibili.com/x/v1/dm/list.so?oid=" + str(oid)
        self.barrage_reault = self.get_page()

    def get_page(self):
        try:
            time.sleep(0.5)
            response = requests.get(self.url, headers= self.headers)
        except Exception as e:
            print("获取xml失败: " + str(e))
            return False
        else:
            if response.status_code == 200: ## GET成功
                 # download xml file:
                f = open('bilibili.xml','wb')
                try:
                    f.write(response.content)
                finally:
                    f.close()
                return True;
            else:
                return False
    
    def xpa(self):
        time.sleep(1)
        if self.barrage_reault:
            html = etree.parse('bilibili.xml',etree.HTMLParser())
            results = html.xpath('//d//text()') # 返回</d>标签的文本
            return results
        
    def barrage_remove_again(self):
        # 无重复的弹幕元素
        results = []
        # 重复的弹幕元素
        again_results = []
        # 所有弹幕元素的单个元素
        all_results = set()
        # 所有元素
        all_results_c = []
        for result in self.xpa():
            all_results.add(result)
            all_results_c.append(result)
            if result not in results:
                results.append(result)
            else:
                again_results.append(result) 
        return results, again_results, all_results, all_results_c

    def make(self):
        results, again_results, all_results, all_results_c = self.barrage_remove_again()
        # 计算弹幕词频
        f = open('barrages.txt','w')
        try:
            for barrage in all_results:
                n = all_results_c.count(barrage)
                f.write(barrage + ":" + str(n) + "\n")
        finally:
            f.close()
        stop_words = ['[',']',',','.','。','?','!']
        words = []
        if results:
            for result in results:
                for stop_word in stop_words:
                    result = "".join(result.split(stop_word))
                words.append(result)
            words = ''.join(words)
            # 转化为string后用jieba进行分词
            words = jieba.cut(words)
            words = ''.join(words)
            w = wc(font_path='/System/Library/Fonts/Hiragino Sans GB.ttc',background_color='white',width=2000,height=1600,max_words=2000)
            w.generate(words)
            w.to_file('image.jpg')

print('输入视频的oid: ')
oid = 0
oid = input()
b=Bilispider(int(oid))
b.make()
