from langchain_openai import ChatOpenAI
from zhipuai import ZhipuAI
from pprint import pprint
import json
import logging
import time

glm = ChatOpenAI(
    temperature=0.1,
    # model="glm-3-turbo",
    model="glm-4",
    openai_api_key="",
    openai_api_base=""
)



client = ZhipuAI(api_key="")