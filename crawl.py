import http
import json
import requests

from bs4 import BeautifulSoup
from jamo import h2j, j2hcj


def parse_word(item):
    word_origin = item.a.text.strip()
    word = word_origin[1:] if check_validation(word_origin) else None
    word_desc = item.findAll(text=True, recursive=False)[1].replace(':\n', '').strip()
    word_desc = word_desc if word else None
    word_set = {'word': word, 'desc': word_desc}
    if word and ('코' == word_origin[0]):
        word_set['postposition'] = '이랑' if len(j2hcj(h2j(word[-1]))) == 3 else '랑'
    return word_set

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

co_url = 'https://wordrow.kr/시작하는-말/코/모든 글자/?쪽={}'
mu_url = 'https://wordrow.kr/시작하는-말/무/모든 글자/?쪽={}'

co_words = [w for w in parse(co_url,22) if w['word']]
mu_words = [w for w in parse(mu_url,69) if w['word']]

with open('assets/co.json', 'w', encoding='UTF-8') as f:
    f.write(json.dumps(co_words, ensure_ascii=False, indent=4))
with open('assets/mu.json', 'w', encoding='UTF-8') as f:
    f.write(json.dumps(mu_words, ensure_ascii=False, indent=4))
