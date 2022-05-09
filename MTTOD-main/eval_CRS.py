'''
written by qgf 2022/4/22
'''
import os
import spacy
import math
import tqdm
import argparse
import logging
from types import SimpleNamespace
from collections import Counter, OrderedDict
from nltk.util import ngrams
from config import CONFIGURATION_FILE_NAME
from reader import MultiWOZReader
from utils import definitions
import json
from utils.io_utils import get_or_create_logger, load_json
from utils.clean_dataset import clean_slot_values
from collections import Counter
from nltk.translate import bleu_score
from nltk.translate.bleu_score import SmoothingFunction
import numpy as np
import pickle as pkl
'''
     "rec_61": [
        {
            "turn_num": 0,
            "turn_domain": [
                "[recommend]"
            ],
            "user": "<bos_user> hello ! have you seen either of these ? avengers: infinity war (2018) or thor_(comics) thor: ragnarok (2017) , omg yes ! i really like them do you have something else for me a superhero movie would be great ! maybe an older superman_(1978_film) movie <eos_user>",
            "usdx": "<bos_user> hello! have you seen either of these? @205163 or @108934 @169419, omg yes! i really like them do you have something else for me a superhero movie would be great! maybe an older @108195 movie <eos_user>",
            "resp": "<bos_resp> have you seen batman_(1989_film_series) <eos_resp>",
            "redx": "<bos_resp> have you seen batman_(1989_film_series) <eos_resp>",
            "match": 47016,
            "bspn": "<bos_belief> [recommend] [value_entity] thor_(comics) superhero_movie superman_(1978_film) <eos_belief>",
            "aspn": "<bos_act> [recommend] [recommend_act] recommend <eos_act>",
            "dbpn": "<bos_db> [db_recommend] spider-man_(2002_film) x-men_(film) ant-man_(film) batman_(1989_film_series) thor_(comics) i_am_thor superman_(1978_film) deadpool_(film) iron_man_(2008_film) the_incredible_hulk_(film) <eos_db>",
            "user_span": {},
            "resp_span": {},
            "bspn_gen": "<bos_belief> [recommend] [value_entity] thor_(comics) superhero_movie superman_(1978_film) <eos_belief>",
            "span": [],
            "bspn_gen_with_span": "<bos_belief> [recommend] [value_entity] thor_(comics) superhero_movie superman_(1978_film) <eos_belief>",
            "dbpn_gen": "<bos_db> [db_recommend] Deadpool_(film) Superman_(1978_film) Iron_Man_(2008_film) The_Incredible_Hulk_(film) The_Avengers_(2012_film) Thor_(comics) X-Men_(film) Spider-Man_(2002_film) Ant-Man_(film) Watchmen_(film) <eos_db>",
            "aspn_gen": "<bos_act> [recommend] [recommend_act] recommend <eos_act>",
            "resp_gen": "<bos_resp> i have n't seen either of those . i would recommend batman_(1989_film_series) and thor: ragnarok (2017) . i have n't seen either of those . <eos_resp>"
        },
'''
entity2entityid = pkl.load(open("./data/CRS/ReDial/entity2entityId.pkl", "rb"))

def id2movie(v):
    for key, value in entity2entityid.items():
        if value == v:
            return key[29:-1]
    return ""

def recall(data):
    count=0
    recall_1=0
    for dial_id, dial in tqdm.tqdm(data.items()):
        for turn in dial:
            if turn["match"]:
                count=count+1
                gold=id2movie(turn["match"])
                gold=gold.lower()
                if gold=="":
                    continue
                if gold in turn["resp_gen"]:
                    recall_1=recall_1+1
    print("匹配到的 "+str(recall_1))
    print("总数 "+str(count))
    return recall_1/count

crs=load_json("./MUL_5.6/ckpt-epoch5/CRS_goal")
print(recall(crs))







