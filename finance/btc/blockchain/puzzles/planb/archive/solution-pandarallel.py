import pandas as pd
from pandarallel import pandarallel
import itertools

pandarallel.initialize()

fname = 'data_test'

m_push_df = pd.DataFrame([],columns=['op','uid','mykey','myval'])
m_pop_df = pd.DataFrame([],columns=['op','uid','mykey'])

# transform each row
def transform_row(row):
    op_list = []

    l = row.iloc[0]
    
    v=l.strip('\n').split(" ")
    b=int(v[0])
    i=int(v[2])
    o=int(v[3])

    # to push
    for x in range(4+i,4+i+o):
        op_list.append(dict(
            op='push',
            uid=int(row.name),
            mykey=v[x],
            myval=(b,float(v[x])),
        ))

    # to pop
    for y in range(4,4+i):
        op_list.append(dict(
            op='pop',
            uid=int(row.name),
            mykey=v[y],
        ))

    return op_list

keep = 'last'
# map-reduce
def process(chunk):
    global m_push_df
    global m_pop_df

    p = chunk.parallel_apply(transform_row,axis=1)
    op_list = list(itertools.chain(*p))
    op_df=pd.DataFrame(op_list)
    
    # get then remove duplicates
    push_df = op_df[op_df.op == 'push'].copy()
    #push_df.drop_duplicates(subset=['mykey'],keep=keep,inplace=True)
    # note keep is set to `last`, repecting vanilla implementation of keeping only last val
    
    pop_df = op_df[op_df.op == 'pop'].copy()
    #pop_df.drop_duplicates(subset=['mykey'],keep=keep,inplace=True)

    # interim merge
    m_push_df = pd.concat([m_push_df,push_df])
    m_push_df.drop_duplicates(subset=['mykey'],keep=keep,inplace=True) 
    
    # interim merge
    m_pop_df = pd.concat([m_pop_df,pop_df])
    m_pop_df.drop_duplicates(subset=['mykey'],keep=keep,inplace=True)
     

chunksize = 2048
with pd.read_csv(fname, 
    chunksize=chunksize,
    header=None) as reader:
    # todo make below parallelized
    for chunk in reader:
        process(chunk)

# further reduce
df = m_push_df.merge(m_pop_df,how='left',on=['mykey'])
df['todel'] = False

def markdel(row):
    # if `pop` is found and `pop` operation occured post `push` operation, mark as delete
    if row.op_y == 'pop' and row.uid_y >= row.uid_x:
        row.todel = True
    return row

df = df.parallel_apply(markdel,axis=1)
df=df[df.todel==False]
df.sort_values(['uid_x'],axis=0,ascending=True)

d = {}
for n,row in df.iterrows():
    d.update({row['mykey']:row['myval_x']})

import hashlib
m = hashlib.sha256()
m.update(str(d).encode('utf-8'))
print(len(d))
print(m.digest().hex())
