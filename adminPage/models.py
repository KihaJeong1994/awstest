from django.db import models
import cx_Oracle as ora
# Create your models here.
database = 't9/1234@192.168.0.39:1521/orcl'


#관리자 로그인
def loginChk(arr):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select count(*) from clientinfo where email=:1 and password=:2"
    cursor.execute(sql,arr)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    return re

 #Client_0_list
def clientInfoM(arr):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select * from (select rownum as rownumber, tmp.* from " \
          "(select a.clientIdx,b.name,b.gender,a.email,a.phone,a.regdate from clientinfo a,clientdetailinfo b where a.clientIdx = b.clientIdx(+) order by a.regdate desc) tmp) a " \
          "where a.rownumber between :1 and :2"

    cursor.execute(sql,arr)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#client_2_blackList
def blackListM(arr):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select * from (select rownum as rownumber, tmp.* from (select a.clientIdx,c.name,b.email,a.reason, a.blackdate from blackList a,clientinfo b,clientdetailinfo c " \
          "where a.clientIdx = b.clientIdx(+) and a.clientIdx = c.clientIdx(+) order by a.blackdate desc) tmp) a where a.rownumber between :1 and :2"
    cursor.execute(sql,arr)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#client_2_blackList
def replyListM(arr):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select * from (select rownum as rownumber, tmp.* from (select a.clientIdx,c.name,b.email,a.reply, a.replydate from replylist a,clientinfo b,clientdetailinfo c " \
          "where a.clientIdx = b.clientIdx(+) and a.clientIdx = c.clientIdx(+) order by a.replydate desc) tmp) a where a.rownumber between :1 and :2"
    cursor.execute(sql,arr)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#Ask_0_list
def AskListM(arr):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select * from (select rownum as rownumber, tmp.* from (select a.boardidx,a.title,b.email,a.regdate from board a, clientinfo b " \
          "where boardtypeidx=0 and a.clientidx=b.clientidx(+)) tmp) a where a.rownumber between :1 and :2"
    cursor.execute(sql,arr)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#금일 문의 및 신고
def TodayBoard():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select a.boardidx,a.title,b.email,to_date(to_char(a.regdate,'yyyymmdd'),'yyyymmdd'),a.boardtypeidx from board a, clientinfo b where a.clientidx=b.clientidx(+) and to_date(to_char(sysdate,'yyyymmdd'),'yyyymmdd')=to_date(to_char(a.regdate,'yyyymmdd'),'yyyymmdd')"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re


#Ask_1_detail
def AskDetailM(idx):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select a.boardidx,a.title,b.name,a.regdate,a.content,c.email from board a " \
          "left outer join clientdetailinfo b on  a.clientidx=b.clientidx  " \
          "left outer join clientinfo c on  a.clientidx=c.clientidx  where a.boardidx=:idx"
    cursor.execute(sql,idx=idx)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#Complain_1_chatlist
def ComplainChatlistM(arr):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select * from (select rownum as rownumber, tmp.* from (select a.boardidx,a.title,b.name,a.regdate from board a, clientdetailinfo b " \
          "where boardtypeidx=1 and a.clientidx=b.clientidx(+)) tmp) a where a.rownumber between :1 and :2"
    cursor.execute(sql,arr)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#Complain_1_chatDetail
def ComplainChatDetailM(idx):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select a.boardidx,a.title,b.name,a.regdate,a.content, c.email sued from board a, clientdetailinfo b, tingboard t, clientinfo c " \
          "where boardtypeidx=1 and a.clientidx=b.clientidx(+) and a.boardidx=:idx and t.boardidx=a.tingidx and t.clientidx=c.clientidx"
    cursor.execute(sql,idx=idx)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#여기부터 분석파트--------------------------------------------------------------------------------------------------------------
#Complain_1_chatDetail(성별 분석)
def AnalysisCustomerM1():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select gender,count(*) as count from clientdetailinfo group by gender"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#Complain_1_chatDetail(연령별 분석)
def AnalysisCustomerM2():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "SELECT CASE WHEN age <= 20 THEN '1-20' WHEN age <= 30 THEN '21-30' WHEN age <= 40 THEN '31-40' WHEN age <= 50 THEN '41-50' ELSE '51+' END AS age, COUNT(*) AS n " \
          "FROM clientDetailInfo GROUP BY CASE WHEN age <= 20 THEN '1-20' WHEN age <= 30 THEN '21-30' WHEN age <= 40 THEN '31-40' WHEN age <= 50 THEN '41-50' ELSE '51+' END " \
          "order by 1"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

def AnalysisCustomerM3():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "SELECT CASE WHEN age <= 20 THEN '1-20' WHEN age <= 30 THEN '21-30' WHEN age <= 40 THEN '31-40' WHEN age <= 50 THEN '41-50' ELSE '51+' END AS age, COUNT(*) AS n " \
          "FROM clientDetailInfo  where gender='남성' GROUP BY CASE WHEN age <= 20 THEN '1-20' WHEN age <= 30 THEN '21-30' WHEN age <= 40 THEN '31-40' WHEN age <= 50 THEN '41-50' ELSE '51+' END " \
          "order by 1"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

def AnalysisCustomerM4():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "SELECT CASE WHEN age <= 20 THEN '1-20' WHEN age <= 30 THEN '21-30' WHEN age <= 40 THEN '31-40' WHEN age <= 50 THEN '41-50' ELSE '51+' END AS age, COUNT(*) AS n " \
          "FROM clientDetailInfo  where gender='여성' GROUP BY CASE WHEN age <= 20 THEN '1-20' WHEN age <= 30 THEN '21-30' WHEN age <= 40 THEN '31-40' WHEN age <= 50 THEN '41-50' ELSE '51+' END " \
          "order by 1"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#----------------------------------------------------------------------------------
#결제 리스트
def SalesList(arr):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select * from (select rownum as rownumber, tmp.* from (select c.email,g.goodname,when,method,g.price from payment p, clientinfo c, goods g " \
          "where p.clientidx=c.clientidx and p.goodidx=g.goodidx order by when desc) tmp) a where a.rownumber between :1 and :2"
    cursor.execute(sql,arr)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re


#일 매출 데이터
def AnalysisSalesDay():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(p.when,'yyyymmdd') day,sum(g.price) daysales from payment p left outer join goods g on p.goodidx=g.goodidx where sysdate-p.when<=7 " \
          "group by to_char(p.when,'yyyymmdd') order by day"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

def LastweekSalesDay():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(p.when,'yyyymmdd') day,sum(g.price) daysales from payment p left outer join goods g on p.goodidx=g.goodidx " \
          "where sysdate-p.when>7  and sysdate-p.when<=14group by to_char(p.when,'yyyymmdd') order by day"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#월 매출 데이터
def AnalysisSalesMonth():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(p.when,'yyyymm') month,sum(g.price) monthsales from payment p left outer join goods g on p.goodidx=g.goodidx " \
          "where sysdate-p.when<365 group by to_char(p.when,'yyyymm') order by month"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#연 매출 데이터
def AnalysisSalesYear():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(p.when,'yyyy') year,sum(g.price) yearsales from payment p left outer join goods g on p.goodidx=g.goodidx " \
          "group by to_char(p.when,'yyyy') order by year"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re
#---------------------------------------------------------------------------------------------------------------

#일 접속 데이터
def AnalysisLoginDay():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(sstime,'yyyymmdd') day,count(idxn) loginuser from loginlog where status='login' and sysdate-sstime<7 " \
          "group by to_char(sstime,'yyyymmdd') order by day"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#월 접속 데이터
def AnalysisLoginMonth():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(sstime,'yyyymm') month,count(idxn) loginuser from loginlog where status='login' and sysdate-sstime<365 group by to_char(sstime,'yyyymm') order by month"

    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#연 접속 데이터
def AnalysisLoginYear():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(sstime,'yyyy') year,count(idxn) loginuser from loginlog where status='login' group by to_char(sstime,'yyyy') order by year"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#캐릭터 별 이름, 설명, 사진 가져오기
def character_info(character_type):
    conn = ora.connect(database)
    cursor = conn.cursor()
    print('캐릭터',character_type)
    sql = "select character_name,character_explanation,character_photo from character where character_type=:character_type"
    cursor.execute(sql,character_type=character_type)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

#--------------------------------------------------------------------------------------------------
#일 회원가입 데이터
def AnalysisSignUpDay():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(regdate,'yyyymmdd') day,count(clientIdx) signup from clientinfo where sysdate-regdate<7 " \
          "group by to_char(regdate,'yyyymmdd') order by day"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#회원가입 분석
def AnalysisSignUpGender():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(c.regdate,'yyyymm') month,count(*) cnt,ch.gender from clientinfo c, clientdetailinfo ch where c.clientidx=ch.clientidx group by to_char(c.regdate,'yyyymm'),ch.gender"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#--------------------------------------------------------------------------------------------------
#일 커플 성사 데이터
def AnalysisCoupleDay():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(decisiontime,'yyyymmdd') day,count(clientIdx) couple from coupledecision " \
          "where sysdate-decisiontime<7 group by to_char(decisiontime,'yyyymmdd') order by day"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#--------------------------------------------------------------------------------------------
#email에 해당하는 clientidx 찾기
def getIdx(email):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select clientidx from clientinfo where email=:email"
    cursor.execute(sql,email=email)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def blacklist_insert(blacklistinfo):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into blacklist values(blackList_seq.nextval,:1,:2,sysdate)"
    cursor.execute(sql,blacklistinfo)
    cursor.close()
    conn.commit()
    conn.close()

def blacklist_insert(blacklistinfo):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into blacklist values(blackList_seq.nextval,:1,:2,sysdate)"
    cursor.execute(sql, blacklistinfo)
    cursor.close()
    conn.commit()
    conn.close()

def reply_insert(replyinfo):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into replylist values(reply_seq.nextval,:1,:2,sysdate)"
    cursor.execute(sql, replyinfo)
    cursor.close()
    conn.commit()
    conn.close()

#이미 추천해준 목록
def countTable(tableName):
    print(tableName)
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select count(*) from "+tableName
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def countBoardByType(boardtypeidx):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select count(*) from board where boardtypeidx=:boardtypeidx"
    cursor.execute(sql,boardtypeidx=boardtypeidx)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def likereceivePeople():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select age,education,height,bodyshape,drink,smoke from clientdetailinfo where clientidx in (select clientidx from likereceive)"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def notlikereceivePeople():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select age,education,height,bodyshape,drink,smoke from clientdetailinfo where clientidx not in (select clientidx from likereceive)"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

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


################################################################
#wordcnt 사진 주기적 업로드
from nltk import Text
def tingTag():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select tag from tingboard"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

def downloadWordCnt():
    taglist=tingTag()

    taglist2=[]
    for tag in taglist:
        if tag[0]:
            taglist_each=tag[0].split(" ")
            taglist2=taglist2+taglist_each

    stopword=['제','정','수','관','때','.',',','-','를','위','바','및','입','그','이']
    taglist2_except_stopword=[]
    taglist2_except_stopword=Text([voca for voca in taglist2 if voca not in stopword])
    print(taglist2_except_stopword.vocab())

    from wordcloud import WordCloud
    from PIL import Image
    from collections import Counter
    import matplotlib.pyplot as plt
    taglist2_except_stopwordC=Counter([voca for voca in taglist2 if voca not in stopword])
    wordv_cnt_totalList=taglist2_except_stopwordC.most_common(50)
    print(wordv_cnt_totalList)
    font_location = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    wordcloudv = WordCloud(font_path=font_location, background_color='white', max_words=50, relative_scaling=0.3, width=800, height=450).generate_from_frequencies(taglist2_except_stopwordC)
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloudv)
    # 축 없애기
    plt.axis('off')
    plt.savefig('static/assets/images/wordcnt/wordcntTest.png')
    print("wordcnt 생성됨")
#downloadWordCnt()

#------------------------------------------------------------------------------
#이상형 추천
import scipy
from django.db import models
import cx_Oracle as ora
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# Create your models here.

database = 't9/1234@192.168.0.39:1521/orcl'
conn = ora.connect(database)
cursor = conn.cursor()

#회원 상세정보에서 데이터 가져오
def clientDetailInfoAll():
    #conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select clientidx,gender,age,religion,education,height,bodyshape,drink,smoke from clientdetailinfo"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    #conn.close()
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
    #conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select recommendedpeopleidx from idealrecommendation where clientidx=:clientIdx and sendornot=1"
    cursor.execute(sql, clientIdx=clientIdx)
    result = cursor.fetchall()
    cursor.close()
    #conn.close()
    return result

#이미 추천해준 목록
def RecommendedList(clientIdx):
    #conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select recommendedpeopleidx from idealrecommendation where clientidx=:clientIdx"
    cursor.execute(sql, clientIdx=clientIdx)
    result = cursor.fetchall()
    cursor.close()
    #conn.close()
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
    #conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into idealRecommendation (recommendationIdx,clientIdx,recommendedPeopleIdx,similarity,recommendationDate) values(recommendationIdx_seq.nextVal,:1,:2,:3,sysdate)"
    #1: clientIdx 2: recommendPeopleIdx
    data=[int(sim[1]),int(sim[2]),round(float(sim[3])*100,2)]
    print(data)
    cursor.execute(sql,data)
    cursor.close()
    conn.commit()
    #conn.close()

#추천 이상형 db저장
def idealRecommendation_insert2(data):
    #conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into idealRecommendation (recommendationIdx,clientIdx,recommendedPeopleIdx,similarity,recommendationDate,recommendtype) values(recommendationIdx_seq.nextVal,:1,:2,:3,sysdate,1)"
    #1: clientIdx 2: recommendPeopleIdx
    cursor.execute(sql,data)
    cursor.close()
    conn.commit()
    #conn.close()

#같은 타입 이상형 추천
def idealRecommendation_sametypeIdx(clientIdx):
    #conn = ora.connect(database)
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
    #conn.close()
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
#idealRecommendation()
#print(round(float('0.344554'),2))