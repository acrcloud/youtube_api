#!/usr/bin/env python
# encoding: utf-8
# 访问 http://tool.lu/pyc/ 查看更多信息
import requests
import time
from lxml import etree

class YoutubeAPI:
    youtube_key = ''
    api_list = {
        'videos.list': 'https://www.googleapis.com/youtube/v3/videos',
        'search.list': 'https://www.googleapis.com/youtube/v3/search',
        'channels.list': 'https://www.googleapis.com/youtube/v3/channels',
        'playlists.list': 'https://www.googleapis.com/youtube/v3/playlists',
        'playlistItems.list': 'https://www.googleapis.com/youtube/v3/playlistItems',
        'activities': 'https://www.googleapis.com/youtube/v3/activities' }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36' }
    
    def __init__(self, key):
        self.youtube_key = key
        self.max_get_retries = 10

    
    def getapidata(self, url, params = None, headers = None):
        retries = self.max_get_retries
        while retries > 0:
            data = requests.get(url, params = params, headers = headers)
            retries -= 1
            if not data.status_code == 429:
                if 500 <= data.status_code:
                    pass
                data.status_code < 600
                if 1:
                    if retries < 0:
                        raise 
                    print 'retrying delay ' + str(1) + ' seconds......'
                    time.sleep(1)
                    continue
            return data
        print '*' * 50
        print 'check your network and url'
        print '*' * 50

    
    def json_list(apidata):
        json_data = apidata.json()
        if 'error' in json_data:
            msg = 'occurred an error: ' + str(json_data['error']['code']) + ' & ' + json_data['error']['message'] + ' & ' + json_data['error']['errors'][0]['reason']
            raise Exception(msg)
        if 'nextPageToken' in json_data:
            nextpagetoken = json_data['nextPageToken']
            items = json_data['items']
        else:
            nextpagetoken = ''
            items = json_data['items']
        return (items, nextpagetoken)

    json_list = staticmethod(json_list)
    
    def get_playlistid_by_channelid(self, channelid):
        api_url = self.api_list['playlists.list']
        playlist_collection = []
        params = {
            'part': 'id',
            'channelId': channelid,
            'pageToken': '',
            'key': self.youtube_key,
            'maxResults': 50 }
        apidata = self.getapidata(api_url, params)
        (items, pagetoken) = self.json_list(apidata)
        for l in items:
            play_list_id = l['id']
            playlist_collection.append(play_list_id)
        
        while pagetoken:
            params['pageToken'] = pagetoken
            apidata = self.getapidata(api_url, params)
            (items, pagetoken) = self.json_list(apidata)
            print pagetoken
            for item in items:
                play_list_id = item['id']
                playlist_collection.append(play_list_id)
            
        return playlist_collection

    
    def get_videoid_by_playlistid(self, playlistid):
        api_url = self.api_list['playlistItems.list']
        videoid_collection = []
        params = {
            'playlistId': playlistid,
            'part': 'contentDetails',
            'maxResults': 50,
            'key': self.youtube_key }
        apidata = self.getapidata(api_url, params)
        (items, pagetoken) = self.json_list(apidata)
        for l in items:
            videoid = l['contentDetails']['videoId']
            videoid_collection.append(videoid)
        
        while pagetoken:
            params['pageToken'] = pagetoken
            apidata = self.getapidata(api_url, params)
            (items, pagetoken) = self.json_list(apidata)
            print pagetoken
            for item in items:
                videoid = item['contentDetails']['videoId']
                videoid_collection.append(videoid)
            
        return videoid_collection

    
    def get_useruploadsplaylist_by_userchannelid(self, userchannelid):
        api_url = self.api_list['channels.list']
        params = {
            'part': 'contentDetails',
            'id': userchannelid,
            'key': self.youtube_key }
        apidata = self.getapidata(api_url, params)
        data_json = apidata.json()
        uploads = data_json['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return uploads

    
    def search(self, keyword = '', type = '', maxresults = 5, num = 0, region = 'US'):
        api_url = self.api_list['search.list']
        params = {
            'q': keyword,
            'part': 'id,snippet',
            'type': type,
            'regionCode': region,
            'maxResults': maxresults,
            'key': self.youtube_key }
        type_dict = {
            'channel': 'channelId',
            'video': 'videoId',
            'playlist': 'playlistId' }
        itemlist = []
        titlelist = []
        
        def get_item(items):
            for l in items:
                searchid = l['snippet'][type_dict[type]]
                searchtitle = l['snippet']['title']
                itemlist.append(searchid)
                titlelist.append(searchtitle)
            

        
        def req():
            apidata = self.getapidata(api_url, params)
            (items, pagetoken) = self.json_list(apidata)
            return (items, pagetoken)

        if num == 0:
            (items, pagetoken) = req()
            get_item(items)
            while pagetoken:
                params['pageToken'] = pagetoken
                (items, pagetoken) = req()
                get_item(items)
        else:
            (items, pagetoken) = req()
            get_item(items)
            while pagetoken and len(itemlist) < num:
                params['pageToken'] = pagetoken
                (items, pagetoken) = req()
                get_item(items)
        data = dict(zip(titlelist, itemlist))
        return data

    
    def get_channelid_by_videoid(self, videoId):
        url = 'https://www.youtube.com/watch?v=' + videoId
        req = requests.get(url, headers = self.headers)
        text = req.text
        xpath_r = u'//*[@id="watch7-user-header"]/div/a/@href'
        tree = etree.HTML(text)
        res = tree.xpath(xpath_r)
        channelid = res[0].split('/')[-1]
        return channelid

    
    def get_channelid_by_username(self, username):
        url = 'https://www.youtube.com/user/' + username
        req = requests.get(url, headers = self.headers)
        text = req.text
        xpath_r = u'/html/head/meta[38]/@content'
        tree = etree.HTML(text)
        channelid = tree.xpath(xpath_r)
        return channelid[0]

    
    def verify_channel(self, channelid):
        verify_text = 'yt-channel-title-icon-verified yt-uix-tooltip yt-sprite'
        url = 'https://www.youtube.com/channel/' + channelid
        req = requests.get(url, headers = self.headers)
        text = req.text
        xpath_r = '//*[@id="c4-primary-header-contents"]/div/div/div[1]/h1/span/a/span/@class'
        tree = etree.HTML(text)
        verify = tree.xpath(xpath_r)
        if verify[0] == verify_text:
            flag = True
        else:
            flag = False
        return flag