import requests


url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"



headers = {
	"X-RapidAPI-Key": "d7a9295da7msh823ef302ae4316ep1ffd78jsnb470f2bd6e94",
	"X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
}





def download_tiktok(link):
	output={}
	querystring = {"url": link, "hd": "0"}
	response = requests.request("GET", url, headers=headers, params=querystring)
	res=response.json()
	if 'error' in res:
		return 'Bad'
	else:
		output['video']=res['data']['wmplay']
		output['title']=res['data']['title']
		return output
#
# print(download_tiktok("https://vt.tiktok.com/ZS8LSqA2c/"))

# def youuteb(url):
# 	y=YouTube(url).streams.first().download()
# 	return y
# print(youuteb("https://www.youtube.com/watch?v=RsYxdVIgNns"))