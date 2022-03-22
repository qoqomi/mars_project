import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.giemi.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20210829',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

movies = soup.select('#old_content > table > tbody > tr')

for movie in movies:
    rank = movie.select_one('td.title > div > a')
    if rank is not None:
        title = rank.text
        number = movie.select_one('td:nth-child(1) > img')['alt']
        star = movie.select_one('td.point').text
        doc= {
            'title':title,
            'number':number,
            'star':star
         }
        db.movies.insert_one(doc)

