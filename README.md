# Bilispider_barrage
利用xml解析对bilibili网站内对应oid的视频弹幕进行爬取，并记录词频，生成词云。

## 使用方法：

在本地建立文件夹，文件夹中建立以下文件：

```
barrages.txt
bilibili.py
bilibili.xml
```
其中```barrages.txt```存放本视频所有弹幕词频
```bilibili.xml```存放从网站中下载的弹幕xml文件
```bilibili.py```存放程序文件

程序运行后文件夹内会生成```image.jpg```即词云图片。

oid在浏览器的Network里面的GET信息里找，然后字体文件的地址需要更改。

## 实现方法：

封装一个类，在类内进行设置headers，url，发出requests，xml文件下载，分词，弹幕查重等操作。

## 带解决问题：

词频排序

## 效果：

对于老番茄🍅的这个视频为例：~~史上最骚杀手~~

https://www.bilibili.com/video/BV1eK4y1n755?spm_id_from=333.851.b_7265636f6d6d656e64.1

oid为296516805。

词频：

![](https://raw.githubusercontent.com/hhy-huang/Image/main/22.png)

云图：

![](https://raw.githubusercontent.com/hhy-huang/Image/main/luo.jpg)
