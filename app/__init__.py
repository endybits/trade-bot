import os

# from pathlib import Path
# import sys
# path_root = Path(__file__).parents[1]
# sys.path.append(path_root)
# print(sys.path)

from app.config.fconfig import get_gh_token

os.environ["GH_TOKEN"] = get_gh_token()

from app.config.fconfig import get_openai_apikey as API_KEY

os.environ["OPENAI_API_KEY"] = API_KEY()
