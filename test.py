import python_youtube_api
youtube = python_youtube_api.YoutubeAPI('XXXXXXX')
data = youtube.search('vevo', 'channel', 5, 5)
print data
