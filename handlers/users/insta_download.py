import requests

url = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"


headers = {
	"X-RapidAPI-Key": "d7a9295da7msh823ef302ae4316ep1ffd78jsnb470f2bd6e94",
	"X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
}

def insta_download(link):
    querystring = {"url":{link}}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res=response.json()
    output={}
    output['video']=res['media']
    output['type']='video'
    if res['Type']=='Carousel':
        output['type']='Carousel'
        output['Carousel']=res['media']


    return output


