#!/usr/bin/env python3

import argparse

from lib.search import keyword_search_command

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands") # dest로 지정한 이름으로(args.이름) 서브커맨드 접근 가능 
    # @@@ subparser를 쓰는 이유 @@@
    # 명령(서브커맨드)마다 다른 인자 세트를 깔끔하게 분리해서 정의하고, CLI를 git, docker처럼 서브커맨드 기반 구조로 만든다
    # subparser를 쓰지 않으면 parser.add_argument로 추가된 모든 인자가 하나의 명령에 속한 것처럼 동작 (ex: uv run main.py --index-path ... --rebuild-index ... --server-port ...)
    # # 서로 용도가 다른 기능들(검색, 인덱스 빌드, 서버 실행 등) 이 한 명령에 뒤섞이고 어떤 인자가 언제 필요한지, 조합이 어떻게 유효한지 표현하기 어렵다
    # # 추가로 --help 출력도 한 페이지에 다 섞여 나와 가독성이 떨어진다
    # subparser를 쓰면 cli argument 입력 최상위에 구분된 명령 이름(ex: search, status, index, ...)을 두고 
    # 각 명령 전용 parser에 .add_argument로 argument들을 추가해서 명령 별 argument들을 분리 가능
    # # 분리를 하게 되면 추가로 uv run main.py search -h, uv run main.py index -h 같이 명령별 도움말을 자동으로 분리해 보여줄 수 있다

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    # search 서브커맨드 추가
    search_parser.add_argument("query", type=str, help="Search query")
    # search 서브 커맨드만의 argument인 query 추가

    args = parser.parse_args()

    match args.command:
        case "search":
            # print the search query here

            query = args.query

            print(f'Searching for: {query}')

            for r in keyword_search_command(query=query):
                print(r)

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()