import scipy
from django.db import models
import cx_Oracle as ora
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# Create your models here.

database = 't9/1234@192.168.0.39:1521/orcl'

#회원 상세정보에서 데이터 가져오
def clientDetailInfoAll():
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

#좋아요 보낸 사람들 idx 목록 끌어오기
def LikeSendList(clientIdx):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select recommendedpeopleidx from idealrecommendation where clientidx=:clientIdx and sendornot=1"
    cursor.execute(sql, clientIdx=clientIdx)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

#이미 추천해준 목록
def RecommendedList(clientIdx):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select recommendedpeopleidx from idealrecommendation where clientidx=:clientIdx"
    cursor.execute(sql, clientIdx=clientIdx)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result




#유사도가 가장 높은 2명 추천
def most3_sim(df,row,dataf):
    clientIdx=[row.clientidx for _ in range(len(df))]
    matf=scipy.sparse.csr_matrix(np.array([dataf[2:10]]))
    recommendedIdx=[]
    cos_sim=[]
    df_idx=df['clientidx']
    #df2=df[['age','religion','education','height','bodyshape','drink','smoke']]
    for n,data in zip(df_idx,df.itertuples()):
        matf2=scipy.sparse.csr_matrix(np.array([data[3:10]]))
        cs=cosine_similarity(matf,matf2)
        recommendedIdx.append(n)
        cos_sim.append(cs[0][0])
    df_cos_sim=pd.DataFrame([clientIdx,recommendedIdx,cos_sim]).T
    df_cos_sim.columns=['clientIdx','recommendedIdx','cos_sim']
    #print(df_cos_sim)
    df_cos_sim=df_cos_sim.sort_values(by=['cos_sim'], axis=0,ascending=False)
    df_cos_sim3=df_cos_sim[0:2]
    return df_cos_sim3

def most3_sim2(df,dataf):
    #print(type(dataf))
    clientIdx=[dataf.clientidx for _ in range(len(df))]
    #print(clientIdx)
    matf=scipy.sparse.csr_matrix(np.array([dataf[3:10]]))
    recommendedIdx=[]
    cos_sim=[]
    df_idx=df['clientidx']
    #df2=df[['age','religion','education','height','bodyshape','drink','smoke']]
    for n,data in zip(df_idx,df.itertuples()):
        matf2=scipy.sparse.csr_matrix(np.array([data[3:10]]))
        cs=cosine_similarity(matf,matf2)
        recommendedIdx.append(n)
        cos_sim.append(cs[0][0])
    df_cos_sim=pd.DataFrame([clientIdx,recommendedIdx,cos_sim]).T
    df_cos_sim.columns=['clientIdx','recommendedIdx','cos_sim']
    df_cos_sim=df_cos_sim.sort_values(by=['cos_sim'], axis=0,ascending=False)
    df_cos_sim3=df_cos_sim[0:2]
    return df_cos_sim3

#추천 이상형 db저장
def idealRecommendation_insert(sim):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into idealRecommendation (recommendationIdx,clientIdx,recommendedPeopleIdx,similarity,recommendationDate) values(recommendationIdx_seq.nextVal,:1,:2,:3,sysdate)"
    #1: clientIdx 2: recommendPeopleIdx
    data=[int(sim[1]),int(sim[2]),round(float(sim[3])*100,2)]
    print(data)
    cursor.execute(sql,data)
    cursor.close()
    conn.commit()
    conn.close()

#추천 이상형 db저장
def idealRecommendation_insert2(data):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into idealRecommendation (recommendationIdx,clientIdx,recommendedPeopleIdx,similarity,recommendationDate,recommendtype) values(recommendationIdx_seq.nextVal,:1,:2,:3,sysdate,1)"
    #1: clientIdx 2: recommendPeopleIdx
    cursor.execute(sql,data)
    cursor.close()
    conn.commit()
    conn.close()

#같은 타입 이상형 추천
def idealRecommendation_sametypeIdx(clientIdx):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select tmp.clientidx  " \
          "from((select * from clientdetailinfo c where c.clientIdx not in " \
          "(select i.recommendedpeopleidx from idealrecommendation i where clientidx=:clientIdx) " \
          "and c.clientidx!=:clientIdx and c.gender!=(select gender from clientdetailinfo where clientidx=:clientIdx)" \
          " and c.character=(select character from clientdetailinfo where clientidx=:clientIdx)) tmp) where rownum=1"
    #1: clientIdx 2: recommendPeopleIdx
    cursor.execute(sql,clientIdx=clientIdx)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


#minmaxScaler
def minMaxScaler(Series):
    series_scaled=(Series-Series.min())/(Series.max()-Series.min())
    return series_scaled

# 컨텐츠 기반 필터링: 자신이 선택한 이성과 비슷한 이성 추천
def idealRecommendation():
    df = pd.DataFrame(clientDetailInfoAll(),
                      columns=['clientidx', 'gender', 'age', 'religion', 'education', 'height', 'bodyshape', 'drink',
                               'smoke'])
    # print(df)
    gender = np.sort(df['gender'].unique())
    religion = np.sort(df['religion'].unique())
    education = np.sort(df['education'].unique())
    bodyshape = np.sort(df['bodyshape'].unique())
    drink = np.sort(df['drink'].unique())
    smoke = np.sort(df['smoke'].unique())


    df['gender'] = df['gender'].apply(lambda x: gender_num(x, gender))
    df['religion'] = df['religion'].apply(lambda x: religion_num(x, religion))
    df['education'] = df['education'].apply(lambda x: education_num(x, education))
    df['bodyshape'] = df['bodyshape'].apply(lambda x: bodyshape_num(x, bodyshape))
    df['drink'] = df['drink'].apply(lambda x: drink_num(x, drink))
    df['smoke'] = df['smoke'].apply(lambda x: smoke_num(x, smoke))

    df['age'] = minMaxScaler(df['age'])
    df['religion'] = minMaxScaler(df['religion'])
    df['education'] = minMaxScaler(df['education'])
    df['height'] = minMaxScaler(df['height'])
    df['bodyshape'] = minMaxScaler(df['bodyshape'])
    df['drink'] = minMaxScaler(df['drink'])
    df['smoke'] = minMaxScaler(df['smoke'])


    for row in df.itertuples():
        clientIdx = row.clientidx
        gender = row.gender
        # idx=df[df['clientidx']==clientIdx].index

        # 좋아요 보낸 사람들 idx 목록 끌어오기
        likeSendList = LikeSendList(row.clientidx)

        # 자신과 같은 타입 소개시켜주기
        sametype_recommendIdx = idealRecommendation_sametypeIdx(clientIdx)[0]

        myinfo=df[df['clientidx']==clientIdx][['age', 'religion', 'education', 'height', 'bodyshape', 'drink',
                               'smoke']]

        sametype_recommendInfo=df[df['clientidx']==sametype_recommendIdx][['age', 'religion', 'education', 'height', 'bodyshape', 'drink',
                               'smoke']]
        matf1 = scipy.sparse.csr_matrix(np.array(myinfo))
        matf2 = scipy.sparse.csr_matrix(np.array(sametype_recommendInfo))
        cs = cosine_similarity(matf1, matf2)
        print("코사인유사도",cs[0][0])
        cs=round(float(cs[0][0])*100,2)
        print(cs)
        data_sametype = [clientIdx, sametype_recommendIdx,cs]
        idealRecommendation_insert2(data_sametype)

        # 이미 추천해줬던 사람들 리스트
        RecommendedLists = RecommendedList(row.clientidx)

        # 이미 추천해줬던 사람들 리스트 => 제거 필요
        RecommendedArr = []
        for recommended in RecommendedLists:
            RecommendedArr.append(recommended[0])
        print("이미추천한리스트", RecommendedArr)

        # 내가 추천받은 사람들 index
        idxList3 = df[df['clientidx'].isin(RecommendedArr)].index

        # 나와 성별이 같은 사람들 제거 => 이성만 소개
        idxList = df[df['gender'] == gender].index

        df_except = df
        for idx in idxList:
            df_except = df_except.drop(idx)
        for idx in idxList3:
            df_except = df_except.drop(idx)

        # 좋아요 보낸적이 있는 경우=> 좋아요 보낸 사람들의 벡터 평균에 가까운 사람 추천
        if len(likeSendList) > 0:
            likeSendArr = []
            for likeSend in likeSendList:
                likeSendArr.append(likeSend[0])

            # 내가 좋아요 보낸 사람들 index
            idxList2 = df[df['clientidx'].isin(likeSendArr)].index

            # 내가 좋아요 보낸 사람들 정보
            likeSendInfo = df[df['clientidx'].isin(likeSendArr)]
            likeSendmean = likeSendInfo.mean()

            # 3~10까지가 index, clientidx, gender 제거 및 나머지
            most_3_sim = most3_sim(df_except, row, likeSendmean)
            print(most_3_sim)
            for sim in most_3_sim.itertuples():
                print(sim)
                idealRecommendation_insert(sim)
            print('-----------------------------')

        # 좋아요 보낸적 없는 경우=> 자기 자신과 유사한 사람 일단 3명 추천
        else:
            # 3~10까지가 index, clientidx, gender 제거 및 나머지
            most_3_sim = most3_sim2(df_except, row)
            print(most_3_sim)
            for sim in most_3_sim.itertuples():
                print(sim)
                idealRecommendation_insert(sim)
            print('-----------------------------')
idealRecommendation()
#print(round(float('0.344554'),2))







#most3_sim(df_scaled[0])


