# -*- coding: utf-8 -*-
"""Prediction with mapping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12Jywfp_TqTwGGM0X23UrgJkkOIOCwB9D
"""

#!pip install transformers &>/dev/null

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import sys
import os
'''py_file_location = "/content/drive/MyDrive/EdgeML_Team/bert-entity-extraction/src_atharva"
sys.path.append(os.path.abspath(py_file_location))'''

import joblib
import torch
import config
import dataset
import engine
from model import EntityModel

meta_data = joblib.load(config.META_FILE)
enc_pos = meta_data["enc_pos"]
enc_tag = meta_data["enc_tag"]
num_pos = len(list(enc_pos.classes_))
num_tag = len(list(enc_tag.classes_))

device = torch.device('cuda')
model = EntityModel(num_tag=num_tag, num_pos=num_pos)
model.load_state_dict(torch.load(config.MODEL_PATH))
model.to(device)


def get_tags(test_dataset):
  with torch.no_grad():
        data = test_dataset[0]
        # print(data)
        for k, v in data.items():
            data[k] = v.to(device).unsqueeze(0)
        tag, pos, _ = model(**data)
        return tag, pos,_

def get_tokens(tags,tokenized_sentence,tags_name):
  map_ = {}
  for i in enc_tag.classes_:
    map_[i] = []

  for i in range(256):
    if tags[i] != 16 and tokenized_sentence[i] != 101:
      map_[tags_name[i]].append(tokenized_sentence[i])
  return map_;

final_info = {"Account_no" : [], "Admit_Date" : [], "MR_Number" : [], "Patient_Name" : [],  "Social_Security_no" : [], "Age" : [], "DOB" : [], "Patient_Phone_no" : [], "Admitting_Disease" : [], "Admitting_Physician" : [], "Primary_Insurance_Policy" : []}
def get_mapping(sentence):
    extracted_info = {"Account_no" : [], "Admit_Date" : [], "MR_Number" : [], "Patient_Name" : [],  "Social_Security_no" : [], "Age" : [], "DOB" : [], "Patient_Phone_no" : [], "Admitting_Disease" : [], "Admitting_Physician" : [], "Primary_Insurance_Policy" : []}
    tokenized_sentence = config.TOKENIZER.encode(sentence)
    sentence = sentence.split()
    test_dataset = dataset.EntityDataset(
            texts=[sentence], 
            pos=[[0] * len(sentence)], 
            tags=[[0] * len(sentence)]
    )
    tag,pos,_ = get_tags(test_dataset)

    tags = tag.argmax(2).cpu().numpy().reshape(-1)

    tags_name = enc_tag.inverse_transform(
                    tag.argmax(2).cpu().numpy().reshape(-1)
                )[:len(tokenized_sentence)]
    #print(len(tokenized_sentence))
    map_ = get_tokens(tags,tokenized_sentence,tags_name)

    for i in map_:
        #print(i,"-->",config.TOKENIZER.decode(map_[i]))
        if i == "B-ACCOUNT #":
          extracted_info['Account_no'].append(config.TOKENIZER.decode(map_[i]))
          final_info['Account_no'].append(extracted_info['Account_no'][0])

        if i == "B-ADMIT DATE":
          extracted_info['Admit_Date'].append(config.TOKENIZER.decode(map_[i]))
          final_info['Admit_Date'].append(extracted_info['Admit_Date'][0])

        if i == "B-ADMITTING DIAGNOSIS":
          extracted_info['Admitting_Disease'].append(config.TOKENIZER.decode(map_[i]))
          extracted_info['Admitting_Disease'][0] = extracted_info['Admitting_Disease'][0].split()[0]
        if i == "I-ADMITTING DIAGNOSIS":
          extracted_info['Admitting_Disease'].append(config.TOKENIZER.decode(map_[i]))
          extracted_info['Admitting_Disease'][0] =' '.join(extracted_info['Admitting_Disease'])
          extracted_info['Admitting_Disease'].pop()
          final_info['Admitting_Disease'].append(extracted_info['Admitting_Disease'][0])

        if i == "B-ADMITTING PHYSICIAN":
          extracted_info['Admitting_Physician'].append(config.TOKENIZER.decode(map_[i]))
          extracted_info['Admitting_Physician'][0] = extracted_info['Admitting_Physician'][0].split()[0]
        if i == "I-ADMITTING PHYSICIAN":
          extracted_info['Admitting_Physician'].append(config.TOKENIZER.decode(map_[i]))
          extracted_info['Admitting_Physician'][0] =' '.join(extracted_info['Admitting_Physician'])
          extracted_info['Admitting_Physician'].pop()
          final_info['Admitting_Physician'].append(extracted_info['Admitting_Physician'][0])

        if i == "B-AGE":
          extracted_info['Age'].append(config.TOKENIZER.decode(map_[i]))
          final_info['Age'].append(extracted_info['Age'][0])

        if i == "B-BIRTH DATE":
          extracted_info['DOB'].append(config.TOKENIZER.decode(map_[i]))
          final_info['DOB'].append(extracted_info['DOB'][0])

        if i == "B-MR NUMBER":
          extracted_info['MR_Number'].append(config.TOKENIZER.decode(map_[i]))
          extracted_info['MR_Number'][0] = extracted_info['MR_Number'][0].replace(" ", "")
          extracted_info['MR_Number'][0] = extracted_info['MR_Number'][0][:8]
          final_info['MR_Number'].append(extracted_info['MR_Number'][0])

        if i == "B-PATIENT NAME":
          extracted_info['Patient_Name'].append(config.TOKENIZER.decode(map_[i]))
          extracted_info['Patient_Name'][0] = extracted_info['Patient_Name'][0].split()[0]
        if i == "I-PATIENT NAME":
          extracted_info['Patient_Name'].append(config.TOKENIZER.decode(map_[i]))
          extracted_info['Patient_Name'][0] =' '.join(extracted_info['Patient_Name'])
          extracted_info['Patient_Name'].pop()
          final_info['Patient_Name'].append(extracted_info['Patient_Name'][0])

        if i == "B-PATIENT PHONE #":
          extracted_info['Patient_Phone_no'].append(config.TOKENIZER.decode(map_[i]))
          extracted_info['Patient_Phone_no'][0] = extracted_info['Patient_Phone_no'][0].replace("(", "")
          extracted_info['Patient_Phone_no'][0] = extracted_info['Patient_Phone_no'][0].replace(")", "")
          extracted_info['Patient_Phone_no'][0] = extracted_info['Patient_Phone_no'][0].replace(".", "")
          extracted_info['Patient_Phone_no'][0] = extracted_info['Patient_Phone_no'][0].replace(" ", "")
          extracted_info['Patient_Phone_no'][0] = extracted_info['Patient_Phone_no'][0].replace("-", "")
          extracted_info['Patient_Phone_no'][0] = extracted_info['Patient_Phone_no'][0][:10]
          final_info['Patient_Phone_no'].append(extracted_info['Patient_Phone_no'][0])

        if i == "B-PRIMARY INSURANCE PLAN":
          extracted_info['Primary_Insurance_Policy'].append(config.TOKENIZER.decode(map_[i]))
          if extracted_info['Primary_Insurance_Policy'] == "":
            extracted_info['Primary_Insurance_Policy'] = "-"
            extracted_info['Primary_Insurance_Policy'][0] = extracted_info['Primary_Insurance_Policy'][0].split()[0]
        if i == "I-PRIMARY INSURANCE PLAN":
          extracted_info['Primary_Insurance_Policy'].append(config.TOKENIZER.decode(map_[i]))
          if extracted_info['Primary_Insurance_Policy'][1] == "":
            extracted_info['Primary_Insurance_Policy'][1] = "-"
          extracted_info['Primary_Insurance_Policy'][0] =' '.join(extracted_info['Primary_Insurance_Policy'])
          extracted_info['Primary_Insurance_Policy'].pop()

          final_info['Primary_Insurance_Policy'].append(extracted_info['Primary_Insurance_Policy'][0])

        if i == "B-SOCIAL SECURITY #":
          extracted_info['Social_Security_no'].append(config.TOKENIZER.decode(map_[i]))
        if i == "I-SOCIAL SECURITY #":
          extracted_info['Social_Security_no'].append(config.TOKENIZER.decode(map_[i]))
          extracted_info['Social_Security_no'][0] =' '.join(extracted_info['Social_Security_no'])
          extracted_info['Social_Security_no'].pop()

          extracted_info['Social_Security_no'][0] = extracted_info['Social_Security_no'][0].replace(" ", "")
          extracted_info['Social_Security_no'][0] = extracted_info['Social_Security_no'][0].replace("-", "")
          extracted_info['Social_Security_no'][0] = extracted_info['Social_Security_no'][0].replace("(", "")
          extracted_info['Social_Security_no'][0] = extracted_info['Social_Security_no'][0].replace(")", "")
          extracted_info['Social_Security_no'][0] = extracted_info['Social_Security_no'][0][:9]
          #extracted_info['Social_Security_no'][0] = int(extracted_info['Social_Security_no'][0])
          final_info['Social_Security_no'].append(extracted_info['Social_Security_no'][0])

import glob

for i in glob.glob(config.TEXT_FILE_PATH):

  f = open(i, "r")

  sentence = f.read();

  #print(sentence)

  get_mapping(sentence)

extracted_df = pd.DataFrame(final_info)
extracted_df.to_csv(config.EXTRACTED_FILE, header = True, index = False)