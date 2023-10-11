from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb://aji:aji@ac-iahpln9-shard-00-00.2e6qheb.mongodb.net:27017,ac-iahpln9-shard-00-01.2e6qheb.mongodb.net:27017,ac-iahpln9-shard-00-02.2e6qheb.mongodb.net:27017/?ssl=true&replicaSet=atlas-54ia0f-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbsparta

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
url = "https://www.bilibili.tv/id/anime"

data = requests.get(url=url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

anime = soup.select("li > .bstar-video-card")
print(len(anime))
for data in anime:
    title = data.select_one(".bstar-video-card__text-wrap > .bstar-video-card__text > .bstar-video-card__text-content >p").text
    view_genre = data.select_one(".bstar-video-card__text-wrap > .bstar-video-card__text > .bstar-video-card__text-content > .bstar-video-card__text-desc >p").text
    cover_tmp = data.find('img', class_='bstar-image__img')['src']
    cover = cover_tmp.split('@')[0]

    print(title,' || ',view_genre,' || ',cover)

    doc = {
        'title' : title,
        'genre' : view_genre,
        'cover' : cover
    }
    db.anime.insert_one(doc)