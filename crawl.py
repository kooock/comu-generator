import http
import json
import requests

from bs4 import BeautifulSoup
from jamo import h2j, j2hcj


def parse_word(item):
    word = item.a.text.strip()
    word = word[1:] if check_validation(word) else None
    word_desc = item.findAll(text=True, recursive=False)[1].replace(':\n', '').strip()
    word_desc = word_desc if word else None
    return {'word': word, 'desc': word_desc}

def parse(url,pages):
    for p in range(1, pages+1):
        res = requests.get(url.format(p))
        assert res.status_code == http.HTTPStatus.OK
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        word_items = soup.select('div.larger > ul > li')
        for item in word_items:
            yield parse_word(item)

def check_validation(word):
    for c in word:
        jamo_str = j2hcj(h2j(c))
        if len(jamo_str) < 2:
            return False
    if word[-1] == '다':
        return False
    if ' ' in word:
        return False
    return True

co_url = 'https://wordrow.kr/%EC%8B%9C%EC%9E%91%ED%95%98%EB%8A%94-%EB%A7%90/%EC%BD%94/%EB%AA%A8%EB%93%A0%20%EA%B8%80%EC%9E%90/?%EC%AA%BD={}'
mu_url = 'https://wordrow.kr/%EC%8B%9C%EC%9E%91%ED%95%98%EB%8A%94-%EB%A7%90/%EB%AC%B4/%EB%AA%A8%EB%93%A0%20%EA%B8%80%EC%9E%90/?%EC%AA%BD={}'

co_words = [w for w in parse(co_url,22) if w['word']]
mu_words = [w for w in parse(mu_url,69) if w['word']]

with open('assets/co.json', 'w', encoding='UTF-8') as f:
    f.write(json.dumps(co_words, ensure_ascii=False, indent=4))
with open('assets/mu.json', 'w', encoding='UTF-8') as f:
    f.write(json.dumps(mu_words, ensure_ascii=False, indent=4))
