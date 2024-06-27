import requests

TIKTOK_QUALITY = "hdplay" # default value (play,wmplay,hdplay)

def TiktokAPIRequest(TIKTOK_API_TOKEN,url):

    APIUrl = "https://tiktok-download-without-watermark.p.rapidapi.com/analysis"

    querystring = {"url":url,"hd":"1"}

    headers = {
        "x-rapidapi-key": TIKTOK_API_TOKEN,
        "x-rapidapi-host": "tiktok-download-without-watermark.p.rapidapi.com"
    }
    response = requests.get(APIUrl, headers=headers, params=querystring)

    jsonTik = response.json()
    return jsonTik["data"][TIKTOK_QUALITY]
    
def TweetAPIRequest(TWITTER_API_TOKEN,url):
    
    APIUrl = "https://twitter-downloader-download-twitter-videos-gifs-and-images.p.rapidapi.com/status"

    querystring = {"url":url}

    headers = {
        "x-rapidapi-key": TWITTER_API_TOKEN,
        "x-rapidapi-host": "twitter-downloader-download-twitter-videos-gifs-and-images.p.rapidapi.com"
    }

    response = requests.get(APIUrl, headers=headers, params=querystring)
    
    jsonTweet = response.json()

    # jsonTweet = {'created_at': 'Thu Mar 30 21:00:37 +0000 2023', 'id': 1641545992268025900, 'description': '✍️ @googledevgroups all across the globe are on the road to Google Cloud certification!\n\n#PrepWithGDG and level uup your career with Certification Study Groups, where participants can get hands on and attend instructor-led workshops → https://t.co/3cDiceXwkO https://t.co/EGwsJSx4v8', 'media': {'video': None, 'photo': [{'type': 'photo', 'url': 'https://pbs.twimg.com/media/FsfwUBoakAI25mp.jpg'}, {'type': 'photo', 'url': 'https://pbs.twimg.com/media/FsfwbZOakAoP7VC.jpg'}, {'type': 'photo', 'url': 'https://pbs.twimg.com/media/Fsfwf77akAs_ZLm.jpg'}]}, 'user': {'id': 50090898, 'id_str': '50090898', 'name': 'Google for Developers', 'screen_name': 'googledevs', 'description': 'Discover the latest developer tools, resources, events, and announcements to help you build smarter, ship faster. 🚀', 'followers_count': 2663488, 'friends_count': 309, 'listed_count': 17909, 'created_at': 'Tue Jun 23 20:25:29 +0000 2009', 'profile': 'https://pbs.twimg.com/profile_images/1804207283712200704/kBX_69dx_normal.png'}, 'retweet_count': 15, 'favorite_count': 74, 'lang': 'en'}

    # array object which contain 3 object (description,images_array,videos_array)

    ### get images
    images = []
    data = jsonTweet['media']['photo']

    if data != None:
        for item in data: 
            images.append(item["url"])

    ### get videos
    videos = []
    data = jsonTweet['media']['video']

    if data != None:
    #    for item in data: 
    #        videos.append(item["videoVariants"][0]["url"])

        videos.append(jsonTweet['media']['video']['videoVariants'][0]['url'])

    post = [jsonTweet['description'],images,videos]

    return post
