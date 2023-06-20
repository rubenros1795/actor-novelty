import ndjson
import numpy as np
import pandas as pd
import sys
from top2vec import Top2Vec
from tqdm import tqdm

#load model
model = Top2Vec.load('TOP2VECMODEL')

# load chronicle primitives
with open('../resources/chronicles-corpus/primitives_corrected_monthly_clean.ndjson') as f:
    data = ndjson.load(f)

# filter events longer than 50 characters, and without date
data_filtered = []
for item in data:
    if item['len_text'] > 50:
        if item['len_text'] <= 5000:
            if isinstance(item['date'],list):
                if len(item['date']) > 0:
                    data_filtered.append(item)

#select most dominant topic per primitive
rows = []

for item in tqdm(data_filtered, total=len(data_filtered)):
    d_dict = {}
    d_dict['doc_id'] = item['id']
    d_dict['clean_month'] = item['clean_month']
    d_dict['call_nr_clean'] = item['call_nr_clean']
    d_dict['topic_id'] = model.get_documents_topics([item['id']])[0][0]
    d_dict['topic_score'] = model.get_documents_topics([item['id']])[1][0]
    rows.append(d_dict)
    
dfje = pd.DataFrame(rows)

#save
with open('../resources/chronicles-corpus/primitive_topic.ndjson', 'w') as fout:
	ndjson.dump(dfje.to_dict('records'), fout)


#find and save all cossims per primitive
rows = []

for item in tqdm(data_filtered, total=len(data_filtered)):
    d_dict = {}
    d_dict['doc_id'] = item['id']
    d_dict['clean_month'] = item['clean_month']
    d_dict['call_nr_clean'] = item['call_nr_clean']
    a, b, c, d = model.get_documents_topics([d_dict['doc_id']], reduced=False, num_topics=433)
    representations = []
    for doc_topic_ids, doc_topic_vals in zip(a, b):
        sorted_topic_vals = doc_topic_vals[doc_topic_ids]
        representations.append(sorted_topic_vals)
        representations = [*representations[0]]
    d_dict['cossims'] = representations
    rows.append(d_dict)
    
df = pd.DataFrame(rows)
split_df = pd.DataFrame(df['cossims'].tolist())
df2 = pd.concat([df, split_df], axis=1).drop(columns=['cossims'])

with open('../resources/chronicles-corpus/cossims_corrected.ndjson', 'w') as fout:
	ndjson.dump(df2.to_dict('records'), fout)