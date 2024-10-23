import requests
import re
from bs4 import BeautifulSoup


page_suffix = '&pgn='
max_pg_reviews = 10

files = ['seriesX', 'seriesS', 'oneX', 'oneS', '360']

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags=re.UNICODE)
    return(emoji_pattern.sub(r'', text)) # no emoji

def filter_a_tag(contents):
    if contents[-1] == 'Read full review...':
        contents.pop()
    return contents

for file_name in files:
    print(file_name)
    with open(file_name+".txt") as file:
        url, pg_len = file.readlines()
    pg_len = min(int(pg_len), max_pg_reviews)
    with open(file_name+"_reviews.txt", "w") as out:
        for i in range(pg_len):
            full_url = url + page_suffix + str(i+1)
            r = requests.get(full_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            s = soup.find_all('p', class_='review-item-content rvw-wrap-spaces')
            for content in s:
                combined_text_list = [remove_tags(str(text)) for text in content.contents]
                combined_text = "".join(filter_a_tag(combined_text_list))
                clean_text = remove_emojis(combined_text)
                out.write(clean_text+'\n')


