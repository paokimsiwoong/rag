import json
import os

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

    for movie in movies:
        if keyword in movie["title"]:
            results.append(movie)
            # @@@ 검색 결과 길이 제한에 맞추어 for 루프 조기 종료
            if len(results) >= limit:
                break


    return results

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