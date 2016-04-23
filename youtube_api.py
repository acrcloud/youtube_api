#!/usr/bin/env python
# coding:utf-8
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)

import requests
import time
from lxml import etree


class YoutubeAPI:
    youtube_key = ''
    api_list = {
        'search.list': 'https://www.googleapis.com/youtube/v3/search',
        'channels.list': 'https://www.googleapis.com/youtube/v3/channels',
        'playlists.list': 'https://www.googleapis.com/youtube/v3/playlists',
        'playlistItems.list': 'https://www.googleapis.com/youtube/v3/playlistItems',
    }

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
    
    def __init__(self, key):
        self.youtube_key = key
        self.max_get_retries = 10

    def getapidata(self, url, params=None, headers=None):
        # request data
        retries = self.max_get_retries
        print url
        while retries > 0:
            data = requests.get(url, params=params, headers=headers)
            retries -= 1
            if data.status_code == 429 or (500 <= data.status_code < 600):
                if retries < 0:
                    raise
                else:
                    print ('retrying delay ' + '1' + ' seconds......')
                    time.sleep(1)
        print '*' * 50
        print 'check your network and url'
        print '*' * 50

    @staticmethod
    def json_list(apidata):
        # Converting data to JSON and handle exceptions
        json_data = apidata.json()
        if 'error' in json_data:
            msg = 'occurred an error: ' + str(json_data['error']['code']) + ' & '+\
                  json_data['error']['message'] + ' & ' + json_data['error']['errors'][0]['reason']
            raise Exception(msg)
        if 'nextPageToken' in json_data:
            nextpagetoken = json_data['nextPageToken']
            items = json_data['items']
        else:
            nextpagetoken = ''
            items = json_data['items']

        return items, nextpagetoken

    def get_playlistid_by_channelid(self, channelid):
        # get playlistid by channelid
        api_url = self.api_list['playlists.list']
        playlist_collection = []
        params = {
            'part': 'id',
            'channelId': channelid,
            'pageToken': '',
            'key': self.youtube_key,
            'maxResults': 50,
        }
        apidata = self.getapidata(api_url, params)
        items, pagetoken = self.json_list(apidata)
        for l in items:
            play_list_id = l['id']
            playlist_collection.append(play_list_id)
        while pagetoken:
            params['pageToken'] = pagetoken
            apidata = self.getapidata(api_url, params)
            items, pagetoken = self.json_list(apidata)
            print pagetoken
            for item in items:
                play_list_id = item['id']
                playlist_collection.append(play_list_id)
            
        return playlist_collection

    def get_videoid_by_playlistid(self, playlistid):
        # get videoid by playlistid
        api_url = self.api_list['playlistItems.list']
        videoid_collection = []
        params = {
            'playlistId': playlistid,
            'part': 'contentDetails',
            'maxResults': 50,
            'key': self.youtube_key
        }
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
        # get user's uploads playlist by user's channelid
        api_url = self.api_list['channels.list']
        params = {
            'part': 'contentDetails',
            'id': userchannelid,
            'key': self.youtube_key,
        }
        apidata = self.getapidata(api_url, params)
        data_json = apidata.json()
        uploads = data_json['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        return uploads

    def search(self, keyword='', type='', maxresults=50, num=0, region='US'):
        # type: the type of result
        # maxresults: the maximum number of items that should be returned in the result set
        # num: number of you need
        # region: reguion code , default is US
        api_url = self.api_list['search.list']
        params = {
            'q': keyword,
            'part': 'id,snippet',
            'type': type,
            'regionCode': region,
            'maxResults': maxresults,
            'key': self.youtube_key,
        }
        type_dict = {
            'channel': 'channelId',
            'video': 'videoId',
            'playlist': 'playlistId',
        }
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
            items, pagetoken = self.json_list(apidata)

            return items, pagetoken

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

    def get_channelid_by_videoid(self, videoid):
        # get channelid by videoid
        url = 'https://www.youtube.com/watch?v=' + videoid
        req = requests.get(url, headers = self.headers)
        text = req.text
        xpath_r = u'//*[@id="watch7-user-header"]/div/a/@href'
        tree = etree.HTML(text)
        res = tree.xpath(xpath_r)
        channelid = res[0].split('/')[-1]

        return channelid

    def get_channelid_by_username(self, username):
        # get channelid by username
        url = 'https://www.youtube.com/user/' + username
        req = requests.get(url, headers=self.headers)
        text = req.text
        xpath_r = u'/html/head/meta[38]/@content'
        tree = etree.HTML(text)
        channelid = tree.xpath(xpath_r)

        return channelid[0]

    def verify_channel(self, channelid):
        # Determine whether the channel is Verified
        verify_text = 'yt-channel-title-icon-verified yt-uix-tooltip yt-sprite'
        url = 'https://www.youtube.com/channel/' + channelid
        req = requests.get(url, headers=self.headers)
        text = req.text
        xpath_r = '//*[@id="c4-primary-header-contents"]/div/div/div[1]/h1/span/a/span/@class'
        tree = etree.HTML(text)
        verify = tree.xpath(xpath_r)
        if verify[0] == verify_text:
            flag = True
        else:
            flag = False

        return flag
