# Youtube API


## Requirements
- Python 2.7
- requests
- lxml


## Usage:

### Search 100 channels about vevo:

```python
#!/usr/bin/env python
# coding:utf-8
# params:
# key: keywords
# type: the type of result
# maxresults: the maximum number of items that should be returned in the result set
# num: number of you need
# region: region code , default is US

import youtube_api
youtube = youtube_api.YoutubeAPI('Your api key from Google Api Console')
data = youtube.search('vevo', 'channel', 50, 100, 'US')
print data

```

### Get playlists by channel id 

```python
#!/usr/bin/env python
# coding:utf-8

import youtube_api
youtube = youtube_api.YoutubeAPI('Your api key from Google Api Console')
data = youtube.get_playlistid_by_channelid('UC-9-kyTW8ZkZNDHQJ6FgpwQ')
print data

```

### Get video id by playlist id 

```python
#!/usr/bin/env python
# coding:utf-8

import youtube_api
youtube = youtube_api.YoutubeAPI('Your api key from Google Api Console')
data = youtube.get_videoid_by_playlistid('PL976DE11BCA1AF15E')
print data
```

### Get user's uploads playlist by user's channelid

```python
#!/usr/bin/env python
# coding:utf-8

import youtube_api
youtube = youtube_api.YoutubeAPI('Your api key from Google Api Console')
data = youtube.get_useruploadsplaylist_by_userchannelid('UCANLZYMidaCbLQFWXBC95Jg')
print data
```

### Get channelid by videoid

```python
#!/usr/bin/env python
# coding:utf-8

import youtube_api
youtube = youtube_api.YoutubeAPI
data = youtube.get_channelid_by_videoid('8xg3vE8Ie_E')
print data
```

### Get channelid by username

```python
#!/usr/bin/env python
# coding:utf-8
import youtube_api
youtube = youtube_api.YoutubeAPI
data = youtube.get_channelid_by_username('TaylorSwiftVEVO')
print data
```

### Determine whether the channel is Verified

```python
#!/usr/bin/env python
# coding:utf-8
import youtube_api
youtube = youtube_api.YoutubeAPI

data = youtube.verify_channel('UCANLZYMidaCbLQFWXBC95Jg')
print data
```



## Youtube Data API v3
- [Youtube Data API v3 Doc](https://developers.google.com/youtube/v3/)
- [Obtain api key from Google API Console](https://console.developers.google.com/)

