#!/usr/bin/env python
# coding:utf-8

import youtube_api
youtube = youtube_api.YoutubeAPI('XXXXXXX')
data = youtube.search('vevo', 'channel', 50, 100, 'US')
print data
