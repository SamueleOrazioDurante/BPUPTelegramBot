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
    
    APIUrl = "https://tweetpik.com/api/v2/images"

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'{TWITTER_API_TOKEN}',
    }

    json_data = {
        'url': f'{url}',
    }

    response = requests.post(APIUrl, headers=headers, json=json_data)
    
    jsonTweet = response.json()
    return jsonTweet['url']