import requests

TIKTOK_QUALITY = "hdplay" # default value (play,wmplay,hdplay)

def TiktokAPIRequest(TIKTOK_API_TOKEN,url):

    APIUrl = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"url\"\r\n\r\n"+url+"\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"hd\"\r\n\r\n1\r\n-----011000010111000001101001--\r\n\r\n"
    headers = {
        "x-rapidapi-key": TIKTOK_API_TOKEN,
        "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com",
        "Content-Type": "multipart/form-data; boundary=---011000010111000001101001"
    }
    response = requests.post(APIUrl, data=payload, headers=headers)

### TEMPLATE RESPONSE
#    file = open("JSONDefaultResponse", "r")
#    jsonTik = json.loads(file.read())
#    file.close()

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