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

def InstaAPIRequest(INSTAGRAM_API_TOKEN,reel_id):

    url = "https://instagram-bulk-scraper-latest.p.rapidapi.com/media_download_by_shortcode/"

    headers = {
        "x-rapidapi-key": INSTAGRAM_API_TOKEN,
        "x-rapidapi-host": "instagram-bulk-scraper-latest.p.rapidapi.com"
    }

    url += reel_id

    #response = requests.get(url, headers=headers)

    #jsonReel = response.json()

    jsonReel = '{
  "data": {
    "main_media_hd": "https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft51.2885-15%2F355082415_6523841574363449_2233309310238247341_n.webp%3Fstp%3Ddst-jpg_e35%26_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D105%26_nc_ohc%3DR8H_y80NGf8AX_dHbwG%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfCIH2lGmC5crljjXjZoZPrF2ARWddJLMp0e4CTmc2axXg%26oe%3D64C160ED%26_nc_sid%3D2999b8",
    "main_media_type": "image",
    "child_medias_hd": [
      {
        "url": "https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft51.2885-15%2F355082415_6523841574363449_2233309310238247341_n.webp%3Fstp%3Ddst-jpg_e35%26_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D105%26_nc_ohc%3DR8H_y80NGf8AX_dHbwG%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfCIH2lGmC5crljjXjZoZPrF2ARWddJLMp0e4CTmc2axXg%26oe%3D64C160ED%26_nc_sid%3D2999b8",
        "type": "image"
      },
      {
        "url": "https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft50.2886-16%2F355571876_5866232603480685_7138929381412628278_n.mp4%3F_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D109%26_nc_ohc%3DOGxgwkyIdssAX8cMO8F%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfCihIu0xGMAuQn6C8LzqRiS3XeTmC0I7t18PfG_kzw3Wg%26oe%3D64BF1608%26_nc_sid%3D2999b8",
        "type": "video"
      },
      {
        "url": "https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-2.cdninstagram.com%2Fv%2Ft50.2886-16%2F355041704_254430960541883_8391784064570592876_n.mp4%3F_nc_ht%3Dscontent-lax3-2.cdninstagram.com%26_nc_cat%3D111%26_nc_ohc%3DF-hcsVl3mdAAX-c5Siw%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfCNPsE6CK5IxZRhNcVErvr7w34rFZ4XA7s6vtn2uMh1vQ%26oe%3D64BF0D70%26_nc_sid%3D2999b8",
        "type": "video"
      },
      {
        "url": "https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-2.cdninstagram.com%2Fv%2Ft50.2886-16%2F355827672_916681516097739_3237313159534597864_n.mp4%3F_nc_ht%3Dscontent-lax3-2.cdninstagram.com%26_nc_cat%3D103%26_nc_ohc%3DynhcD8JDJNsAX8GKTKT%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfB4VUt4ov7BSePRRnSZlI8-CPcDdmJ9U_6Xl7QVQcISBg%26oe%3D64BEDA5F%26_nc_sid%3D2999b8",
        "type": "video"
      },
      {
        "url": "https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft50.2886-16%2F352873298_1237884630200685_3166460357904713208_n.mp4%3F_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D109%26_nc_ohc%3DrmGyaENKf_MAX_D-Z2E%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfA_5p6ShJwhOHBJbLXgmZfBa3eDnIXWEgExk8eq0t5FyQ%26oe%3D64BF2E01%26_nc_sid%3D2999b8",
        "type": "video"
      },
      {
        "url": "https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft50.2886-16%2F354303573_1463476857755224_2847621435452663161_n.mp4%3F_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D104%26_nc_ohc%3D0TMC6KJ3LisAX_YQh3-%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfBimQZ5_eMRbjdGX4JKSqK33l2WyusL1vD1ocrAEiIBZA%26oe%3D64BF5E20%26_nc_sid%3D2999b8",
        "type": "video"
      },
      {
        "url": "https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft50.2886-16%2F355808245_1601943133643500_101188079259405607_n.mp4%3F_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D104%26_nc_ohc%3DXMb_95E4jNMAX9Pbt7n%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfBgqfNjdYGuqUnL4Qzpf7q5mZktljsso5OhleV6-NCFWg%26oe%3D64BF1A25%26_nc_sid%3D2999b8",
        "type": "video"
      }
    ],
    "caption": "It just became easier for that trip to finally make it out of the group chat. Scroll ▶️ to see a round-up of Shopping, Search and Maps features that can help you plan, travel and shop and tap the link in our bio to learn more.",
    "owner": {
      "id": "1067259270",
      "is_verified": true,
      "profile_pic_url": "https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft51.2885-19%2F126151620_3420222801423283_6498777152086077438_n.jpg%3Fstp%3Ddst-jpg_s150x150%26_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D1%26_nc_ohc%3Danwz586pUygAX_8p3ba%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfDqW3twdW-IfVw97xucPk8KmDauX7smKnq-jfcrTa_dag%26oe%3D64C1B544%26_nc_sid%3D2999b8",
      "username": "google",
      "blocked_by_viewer": false,
      "followed_by_viewer": false,
      "full_name": "Google",
      "has_blocked_viewer": false,
      "is_private": false,
      "is_unpublished": false,
      "requested_by_viewer": false
    }
  },
  "status": "ok",
  "message": null
}'

# json object contain a main media and an array of secondary media (all of them has a type [image,video])

    images = []
    videos = []

    ### get main media
    
    main_media = jsonReel['data']['main_media_hd'] 
    main_media_type = jsonReel['data']['main_media_type']

    if main_media_type == "image":
        images.append(main_media)
    if main_media_type == "video":
        videos.append(main_media)

    ### get secondary media
    
    child_medias_hd = jsonReel['data']['child_medias_hd']

    if data != None:
        for item in data: 
            type = item["type"]
            url = item["url"]
            if type == "image":
                images.append(url)
            if type == "video":
                videos.append(url)

    post = [jsonReel['data']['caption'],images,videos]