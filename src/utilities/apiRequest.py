
import logger.logger as logger

import requests


def apiRequest(APIUrl,headers,query):

    logger.apiRequest(APIUrl,None)

    try:
        if query != None:
            response = requests.get(APIUrl, headers=headers, params=query)
        else:
            response = requests.get(APIUrl, headers=headers)

        return response.json()

    except Exception:
        logger.apiRequest(APIUrl,Exception)


TIKTOK_QUALITY = "hdplay" # default value (play,wmplay,hdplay)
# DA SPOSTARE IN .env

#DA SPOSTARE TUTTE RISPOSTE DI DEFUALT (USATE PER TESTING)

def TiktokAPIRequest(TIKTOK_API_TOKEN,url):

    APIUrl = "https://tiktok-download-without-watermark.p.rapidapi.com/analysis"

    headers = {
        "x-rapidapi-key": TIKTOK_API_TOKEN,
        "x-rapidapi-host": "tiktok-download-without-watermark.p.rapidapi.com"
    }

    querystring = {"url":url,"hd":"1"}


    jsonTik = apiRequest(APIUrl,headers,querystring)
    return jsonTik["data"][TIKTOK_QUALITY]
    
def TweetAPIRequest(TWITTER_API_TOKEN,url):
    
    APIUrl = "https://twitter-downloader-download-twitter-videos-gifs-and-images.p.rapidapi.com/status"

    headers = {
        "x-rapidapi-key": TWITTER_API_TOKEN,
        "x-rapidapi-host": "twitter-downloader-download-twitter-videos-gifs-and-images.p.rapidapi.com"
    }

    querystring = {"url":url}


    jsonTweet = apiRequest(APIUrl,headers,querystring)

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
    url += reel_id

    headers = {
        "x-rapidapi-key": INSTAGRAM_API_TOKEN,
        "x-rapidapi-host": "instagram-bulk-scraper-latest.p.rapidapi.com"
    }

    jsonReel = apiRequest(url,headers,None)

    #jsonReel = {"data":{"main_media_hd":"https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft51.2885-15%2F355082415_6523841574363449_2233309310238247341_n.webp%3Fstp%3Ddst-jpg_e35%26_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D105%26_nc_ohc%3DR8H_y80NGf8AX_dHbwG%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfCIH2lGmC5crljjXjZoZPrF2ARWddJLMp0e4CTmc2axXg%26oe%3D64C160ED%26_nc_sid%3D2999b8","main_media_type":"image","child_medias_hd":[{"url":"https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft51.2885-15%2F355082415_6523841574363449_2233309310238247341_n.webp%3Fstp%3Ddst-jpg_e35%26_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D105%26_nc_ohc%3DR8H_y80NGf8AX_dHbwG%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfCIH2lGmC5crljjXjZoZPrF2ARWddJLMp0e4CTmc2axXg%26oe%3D64C160ED%26_nc_sid%3D2999b8","type":"image"},{"url":"https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft50.2886-16%2F355571876_5866232603480685_7138929381412628278_n.mp4%3F_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D109%26_nc_ohc%3DOGxgwkyIdssAX8cMO8F%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfCihIu0xGMAuQn6C8LzqRiS3XeTmC0I7t18PfG_kzw3Wg%26oe%3D64BF1608%26_nc_sid%3D2999b8","type":"video"},{"url":"https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-2.cdninstagram.com%2Fv%2Ft50.2886-16%2F355041704_254430960541883_8391784064570592876_n.mp4%3F_nc_ht%3Dscontent-lax3-2.cdninstagram.com%26_nc_cat%3D111%26_nc_ohc%3DF-hcsVl3mdAAX-c5Siw%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfCNPsE6CK5IxZRhNcVErvr7w34rFZ4XA7s6vtn2uMh1vQ%26oe%3D64BF0D70%26_nc_sid%3D2999b8","type":"video"},{"url":"https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-2.cdninstagram.com%2Fv%2Ft50.2886-16%2F355827672_916681516097739_3237313159534597864_n.mp4%3F_nc_ht%3Dscontent-lax3-2.cdninstagram.com%26_nc_cat%3D103%26_nc_ohc%3DynhcD8JDJNsAX8GKTKT%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfB4VUt4ov7BSePRRnSZlI8-CPcDdmJ9U_6Xl7QVQcISBg%26oe%3D64BEDA5F%26_nc_sid%3D2999b8","type":"video"},{"url":"https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft50.2886-16%2F352873298_1237884630200685_3166460357904713208_n.mp4%3F_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D109%26_nc_ohc%3DrmGyaENKf_MAX_D-Z2E%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfA_5p6ShJwhOHBJbLXgmZfBa3eDnIXWEgExk8eq0t5FyQ%26oe%3D64BF2E01%26_nc_sid%3D2999b8","type":"video"},{"url":"https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft50.2886-16%2F354303573_1463476857755224_2847621435452663161_n.mp4%3F_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D104%26_nc_ohc%3D0TMC6KJ3LisAX_YQh3-%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfBimQZ5_eMRbjdGX4JKSqK33l2WyusL1vD1ocrAEiIBZA%26oe%3D64BF5E20%26_nc_sid%3D2999b8","type":"video"},{"url":"https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft50.2886-16%2F355808245_1601943133643500_101188079259405607_n.mp4%3F_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D104%26_nc_ohc%3DXMb_95E4jNMAX9Pbt7n%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfBgqfNjdYGuqUnL4Qzpf7q5mZktljsso5OhleV6-NCFWg%26oe%3D64BF1A25%26_nc_sid%3D2999b8","type":"video"}],"caption":"It just became easier for that trip to finally make it out of the group chat. Scroll ▶️ to see a round-up of Shopping, Search and Maps features that can help you plan, travel and shop and tap the link in our bio to learn more.","owner":{"id":"1067259270","is_verified":True,"profile_pic_url":"https://phosphor.utils.elfsightcdn.com/?url=https%3A%2F%2Fscontent-lax3-1.cdninstagram.com%2Fv%2Ft51.2885-19%2F126151620_3420222801423283_6498777152086077438_n.jpg%3Fstp%3Ddst-jpg_s150x150%26_nc_ht%3Dscontent-lax3-1.cdninstagram.com%26_nc_cat%3D1%26_nc_ohc%3Danwz586pUygAX_8p3ba%26edm%3DAP_V10EBAAAA%26ccb%3D7-5%26oh%3D00_AfDqW3twdW-IfVw97xucPk8KmDauX7smKnq-jfcrTa_dag%26oe%3D64C1B544%26_nc_sid%3D2999b8","username":"google","blocked_by_viewer":False,"followed_by_viewer":False,"full_name":"Google","has_blocked_viewer":False,"is_private":False,"is_unpublished":False,"requested_by_viewer":False}},"status":"ok","message":None}
    #jsonReel = {'data': {'main_media_hd': 'https://phosphor.ivanenko.workers.dev/?url=https%3A%2F%2Fscontent-yyz1-1.cdninstagram.com%2Fo1%2Fv%2Ft16%2Ff1%2Fm86%2FE44D8CB2E71F31D7E8F41A98A5B7619E_video_dashinit.mp4%3Fstp%3Ddst-mp4%26efg%3DeyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuNzIwLmJhc2VsaW5lIn0%26_nc_cat%3D109%26vs%3D561091433057206_56612145%26_nc_vs%3DHBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC9FNDREOENCMkU3MUYzMUQ3RThGNDFBOThBNUI3NjE5RV92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dNVVFqUnMwd0FmLUZaVUVBRjRyWGIyLUxRRXNicV9FQUFBRhUCAsgBACgAGAAbABUAACbklcyF1vKIQBUCKAJDMywXQDXu2RaHKwIYEmRhc2hfYmFzZWxpbmVfMV92MREAdf4HAA%253D%253D%26_nc_rid%3D647d47c10d%26ccb%3D9-4%26oh%3D00_AYAhVG1BXUJfUc1o0UbPQJZhqKWilFdv1KS5Xm8fu16Baw%26oe%3D67193C3D%26_nc_sid%3Dd885a2', 'main_media_type': 'video', 'caption': 'Honey, help me cover the sun. Thank you.🥰🥰🥰#fy #fyp #trending #cute #adorable #redpanda #Iove', 'owner': {'id': '54585580804', 'username': 'littlepanda6487', 'is_verified': False, 'profile_pic_url': 'https://phosphor.ivanenko.workers.dev/?url=https%3A%2F%2Fscontent-yyz1-1.cdninstagram.com%2Fv%2Ft51.2885-19%2F298304797_446720757168732_8924819246119094721_n.jpg%3Fstp%3Ddst-jpg_e0_s150x150%26_nc_ht%3Dscontent-yyz1-1.cdninstagram.com%26_nc_cat%3D1%26_nc_ohc%3DSD7dqcseJ84Q7kNvgE9Cr1Y%26_nc_gid%3D647d431f59894e51aebc02733b8ea8f4%26edm%3DANTKIIoBAAAA%26ccb%3D7-5%26oh%3D00_AYAUXP4bwDYDsJDr0RmlAplwWq7tKZbt2DXV5CD0JMFSiA%26oe%3D671D3F14%26_nc_sid%3Dd885a2', 'blocked_by_viewer': False, 'restricted_by_viewer': None, 'followed_by_viewer': False, 'full_name': 'Lily Sepation', 'has_blocked_viewer': False, 'is_embeds_disabled': False, 'is_private': False, 'is_unpublished': False, 'requested_by_viewer': False, 'pass_tiering_recommendation': True, 'edge_owner_to_timeline_media': {'count': 2728}, 'edge_followed_by': {'count': 388902}}}, 'status': 'ok', 'message': None}

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
    try:
        child_medias_hd = jsonReel['data']['child_medias_hd']

        if child_medias_hd != None:
            for item in child_medias_hd: 
                type = item["type"]
                url = item["url"]
                if type == "image":
                    images.append(url)
                if type == "video":
                    videos.append(url)
    except:
        pass

    post = [jsonReel['data']['caption'],images,videos]

    return post