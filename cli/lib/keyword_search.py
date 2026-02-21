import json
import os
import string

DEFAULT_SEARCH_LIMIT = 5


# print(__file__)
# /home/paokimsiwoong/workspace/github.com/paokimsiwoong/rag/cli/lib/search.py
# print(os.path.dirname(__file__))
# /home/paokimsiwoong/workspace/github.com/paokimsiwoong/rag/cli/lib
# print(os.path.dirname(os.path.dirname(__file__)))
# /home/paokimsiwoong/workspace/github.com/paokimsiwoong/rag/cli

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# print(f"==>> PROJECT_ROOT: {PROJECT_ROOT}")
# ==>> PROJECT_ROOT: /home/paokimsiwoong/workspace/github.com/paokimsiwoong/rag

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
# DATA_PATH = "/home/paokimsiwoong/workspace/github.com/paokimsiwoong/rag/data/movies.json"

def load_json(data_path: str) -> dict:
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def keyword_search(keyword: str, data: dict, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:

    results = []

    movies = data["movies"]

    # trans = str.maketrans("", "", string.punctuation)
    # str.maketrans(from, to, remove)
    # string.punctuation == '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    # string.punctuation에 속하는 글자는 지우는 translation
    # # from, to는 ""로 두어 글자 변환은 하지 않고, remove만 string.punctuation로 두어 punctuation 글자들만 지우기

    # keyword_lowered = keyword.lower()
    # keyword_remove_punc = keyword_lowered.translate(trans)

    keyword_preprocessed = preprocess_text(keyword)

    for movie in movies:
        title_preprocessed = preprocess_text(movie["title"])

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # checker = False
        #
        # for title_token in title_preprocessed:
        #     if checker:
        #         break
        #     for keyword_token in keyword_preprocessed:
        #         if keyword_token in title_token:
        #             results.append(movie)
        #             checker = True
        #             break
        # @@@ 다중 루프 한꺼번에 나오는 처리는 함수 return이 더 깔끔
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        if has_matching_token(keyword_tokens=keyword_preprocessed, title_tokens=title_preprocessed):
            results.append(movie)
        
        # @@@ 검색 결과 길이 제한에 맞추어 for 루프 조기 종료
        if len(results) >= limit:
            break


    return results


# 일부라도 일치하는 토큰이 있는지 확인하는 함수
def has_matching_token(keyword_tokens: list[str], title_tokens: list[str]) -> bool:
    for title_token in title_tokens:
        for keyword_token in keyword_tokens:
            if keyword_token in title_token:
                return True
            
    return False

# 텍스트 전처리 함수
def preprocess_text(text:str) -> list[str]:
    # string.punctuation에 속하는 글자는 지우는 translation
    trans = str.maketrans("", "", string.punctuation)
    # str.maketrans(from, to, remove)로 .translate에 쓰이는 translation 테이블 만들기
    # # string.punctuation == '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    # # from, to는 ""로 두어 글자 변환은 하지 않고, remove만 string.punctuation로 두어 punctuation 글자들만 지우기

    text_lowered = text.lower()
    text_remove_punc = text_lowered.translate(trans)

    text_split = text_remove_punc.split(" ")
    text_split = [t for t in text_split if len(t) > 0]

    return text_split



def keyword_search_command(query: str) -> list[str]:

    results = []

    data = load_json(DATA_PATH)

    search_results = keyword_search(query, data)

    search_results.sort(key=lambda x : x["id"])

    # 검색 결과 최대 5개로 제한 
    # @@@ --> keyword_search 함수 안으로 이동
    # @@@ @@@ data 전체를 for로 순회하고나서 결과를 제한하기 보다 for 루프 순회 길이를 줄이는게 더 좋음
    # search_results = search_results[:5]

    # for i, movie in enumerate(search_results):
    #     results.append(f'{i+1}. {movie["title"]}')
    # @@@ enumerate에 start 값 1로 지정 가능
    for i, movie in enumerate(search_results, 1):
        results.append(f'{i}. {movie["title"]}')

    return results