import scipy
from django.db import models
import cx_Oracle as ora
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# Create your models here.

database = 'kosmorpa/test00@192.168.0.39:1521/orcl'

#회원 상세정보에서 데이터 가져오
def clientDetailInfo():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select clientidx,gender,age,religion,education,height,bodyshape,drink,smoke from clientdetailinfo"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


#print(gender)
def gender_num(kind,gender):
    return gender.tolist().index(kind)
def religion_num(kind,religion):
    return religion.tolist().index(kind)
def education_num(kind,education):
    return education.tolist().index(kind)
def bodyshape_num(kind,bodyshape):
    return bodyshape.tolist().index(kind)
def drink_num(kind,drink):
    return drink.tolist().index(kind)
def smoke_num(kind,smoke):
    return smoke.tolist().index(kind)


from sklearn.preprocessing import MinMaxScaler
# scaler=MinMaxScaler()
# scaler.fit(df2)
#
# df_scaled=scaler.transform(df2) #정규화
#
# mat0=scipy.sparse.csr_matrix(df_scaled[0])
# mat1=scipy.sparse.csr_matrix(df_scaled[1])
# ss=cosine_similarity(mat0,mat1)

def most3_sim(df,dataf):
    #print(type(dataf))
    clientIdx=[dataf.clientidx for _ in range(len(df))]
    #print(clientIdx)
    matf=scipy.sparse.csr_matrix(np.array([dataf[3:10]]))
    recommendedIdx=[]
    cos_sim=[]
    df_idx=df['clientidx']
    #df2=df[['age','religion','education','height','bodyshape','drink','smoke']]
    for n,data in zip(df_idx,df.itertuples()):
        #print('n',data)
        matf2=scipy.sparse.csr_matrix(np.array([data[3:10]]))
        cs=cosine_similarity(matf,matf2)
        #print('코사인 유사도:',n,cs[0][0])
        recommendedIdx.append(n)
        cos_sim.append(cs[0][0])
    print(cos_sim)
    df_cos_sim=pd.DataFrame([clientIdx,recommendedIdx,cos_sim]).T
    df_cos_sim.columns=['clientIdx','recommendedIdx','cos_sim']
    #print(df_cos_sim)
    df_cos_sim=df_cos_sim.sort_values(by=['cos_sim'], axis=0,ascending=False)
    #print(df_cos_sim[0:3])
    df_cos_sim3=df_cos_sim[0:3]
    return df_cos_sim3

def idealRecommendation_insert(sim):
    print(sim)
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into idealRecommendation (recommendationIdx,clientIdx,recommendedPeopleIdx,recommendationDate) values(recommendationIdx_seq.nextVal,:1,:2,sysdate)"
    print(type(int(sim[1])))
    data=[int(sim[1]),int(sim[2])]
    print(data)
    cursor.execute(sql,data)
    cursor.close()
    conn.commit()
    conn.close()

def idealRecommendation():
    df = pd.DataFrame(clientDetailInfo(),
                      columns=['clientidx', 'gender', 'age', 'religion', 'education', 'height', 'bodyshape', 'drink',
                               'smoke'])
    #print(df)
    gender = np.sort(df['gender'].unique())
    religion = np.sort(df['religion'].unique())
    education = np.sort(df['education'].unique())
    bodyshape = np.sort(df['bodyshape'].unique())
    drink = np.sort(df['drink'].unique())
    smoke = np.sort(df['smoke'].unique())

    df['gender'] = df['gender'].apply(lambda x: gender_num(x,gender))
    df['religion'] = df['religion'].apply(lambda x: religion_num(x,religion))
    df['education'] = df['education'].apply(lambda x: education_num(x,education))
    df['bodyshape'] = df['bodyshape'].apply(lambda x: bodyshape_num(x,bodyshape))
    df['drink'] = df['drink'].apply(lambda x: drink_num(x,drink))
    df['smoke'] = df['smoke'].apply(lambda x: smoke_num(x,smoke))

    for row in df.itertuples():
        clientIdx=row.clientidx
        gender=row.gender
        #idx=df[df['clientidx']==clientIdx].index
        #나와 성별이 같은 사람들 제거 => 이성만 소개
        idxList=df[df['gender']==gender].index
        #print(idxList)

        df_except_same_gender=df
        for idx in idxList:
            df_except_same_gender = df_except_same_gender.drop(idx)
        #print(df_except_same_gender)

        # 3~10까지가 index, clientidx, gender 제거 및 나머지
        most_3_sim=most3_sim(df_except_same_gender, row)
        print(most_3_sim)
        for sim in most_3_sim.itertuples():
            print(sim)
            idealRecommendation_insert(sim)
#idealRecommendation()


#most3_sim(df_scaled[0])


