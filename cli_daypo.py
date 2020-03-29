# 
# 
# 
# 
# 
# 
# 
# 
import requests
import json
from bs4 import BeautifulSoup
import argparse


foo = requests.get("http://redoc.live/19-20/db.js") #Make date a variable - argparse
bar = json.loads(foo.text[foo.text.find("{"):])
print(bar.keys())