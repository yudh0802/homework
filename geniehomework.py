import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')



# BeautifulSoup은 select와 select_one 함수만 잘 쓰면 된다
musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
#순위
# #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
#곡
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#가수
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis



for music in musics:
    music_rank = music.select_one('td.number').text
    music_title = music.select_one('td.info > a.title.ellipsis').text
    music_artist = music.select_one('td.info > a.artist.ellipsis').text



    rank = music_rank.split()
    title = music_title.strip()
    artist = music_artist

    info = {
        'rank' : rank[0],
        'title' : title,
        'artist' : artist
    }

    db.musicinfo.insert_one(info)