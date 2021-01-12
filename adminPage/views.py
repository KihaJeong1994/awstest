import math

from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_protect

def Client_0_list(request):

    countAll=countTable('clientinfo')[0]
    cntPerPage=10
    totalPage= math.ceil(countAll/cntPerPage)
    try:
        page = int(request.GET['page'])
    except:
        page=1
    start=(page-1)*cntPerPage+1
    end=(page)*cntPerPage
    arr=(start,end)
    result = clientInfoM(arr)
    return render(request,"adminPage/Client_0_list.html",{'result':result,'totalPage':totalPage,'page':page})

def Client_2_blacklist(request):
    countAll = countTable('blacklist')[0]
    cntPerPage = 10
    totalPage= math.ceil(countAll/cntPerPage)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    start = (page - 1) * cntPerPage + 1
    end = (page) * cntPerPage
    arr = (start, end)
    result =blackListM(arr)
    return render(request,"adminPage/Client_2_blacklist.html",{'result':result,'totalPage':totalPage})

def Client_2_replylist(request):
    countAll = countTable('replylist')[0]
    cntPerPage = 10
    totalPage= math.ceil(countAll/cntPerPage)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    start = (page - 1) * cntPerPage + 1
    end = (page) * cntPerPage
    arr = (start, end)
    result =replyListM(arr)
    return render(request,"adminPage/Client_2_replylist.html",{'result':result,'totalPage':totalPage})

def Ask_0_list(request):
    countAll = countBoardByType(0)[0]
    cntPerPage = 10
    totalPage = math.ceil(countAll / cntPerPage)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    start = (page - 1) * cntPerPage + 1
    end = (page) * cntPerPage
    arr = (start, end)
    result =AskListM(arr)
    return render(request,"adminPage/Ask_0_list.html",{'result':result,'totalPage':totalPage})

def Ask_1_detail(request):
    idx = request.GET['idx']
    result=AskDetailM(idx)
    return render(request,"adminPage/Ask_1_detail.html",{'result':result})

def Complain_1_chatlist(request):
    countAll = countBoardByType(1)[0]
    cntPerPage = 10
    totalPage = math.ceil(countAll / cntPerPage)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    start = (page - 1) * cntPerPage + 1
    end = (page) * cntPerPage
    arr = (start, end)
    result =ComplainChatlistM(arr)
    return render(request,"adminPage/Complain_1_chatlist.html",{'result':result,'totalPage':totalPage})

def Complain_1_chatDetail(request):
    idx = request.GET["idx"]
    result =ComplainChatDetailM(idx)
    return render(request,"adminPage/Complain_1_chatDetail.html",{'result':result})

def Analysis_4_customer(request):
   result1=AnalysisCustomerM1()
   result2=AnalysisCustomerM2()
   result3=AnalysisCustomerM3()
   result4=AnalysisCustomerM4()
   print(result3)
   print(result4)
   return render(request,"adminPage/Analysis_4_customer.html",{'result1':result1,'result2':result2,'result3':result3,'result4':result4})

#------여기부터 경로설정----------------------------------------------------------------------
def home(request):
    if not request.session.keys():
        return redirect('/adminPage/login')
    print("home시작")
    LoginDay = AnalysisLoginDay()
    SalesDay = AnalysisSalesDay()
    LastweekSales=LastweekSalesDay()
    SignUpDay=AnalysisSignUpDay()
    CoupleDay=AnalysisCoupleDay()
    result = TodayBoard()
    return render(request,"adminPage/index.html",{'LoginDay':LoginDay,'SalesDay':SalesDay,
                                                  'SignUpDay':SignUpDay,'CoupleDay':CoupleDay, 'LastweekSales': LastweekSales, 'result': result})

def index(request):
    if not request.session.keys():
        return redirect('/adminPage/login')
    print("home시작")
    LoginDay = AnalysisLoginDay()
    SalesDay = AnalysisSalesDay()
    LastweekSales=LastweekSalesDay()
    SignUpDay = AnalysisSignUpDay()
    CoupleDay = AnalysisCoupleDay()
    result = TodayBoard()
    return render(request, "adminPage/index.html", {'LoginDay': LoginDay, 'SalesDay': SalesDay,
                                                    'SignUpDay': SignUpDay, 'CoupleDay': CoupleDay,
                                                    'LastweekSales': LastweekSales, 'result': result})
def test(request):
    return render(request,"adminPage/test.html")
def Analysis_1_inflow(request):
    result=AnalysisSignUpGender()
    print(result)
    return render(request,"adminPage/Analysis_1_inflow.html",{'result':result})
def Analysis_2_properties(request):
    return render(request,"adminPage/Analysis_2_properties.html")


#-----------------------------------------------------------------------------------------------
#매칭 분석
def education_num(kind,education):
    return education.tolist().index(kind)/len(education)
    #return education.index(kind)/len(education)
def bodyshape_num(kind,bodyshape):
    return bodyshape.tolist().index(kind)/len(bodyshape)
    #return bodyshape.index(kind)/len(bodyshape)

def drink_num(kind,drink):
    return drink.tolist().index(kind)/len(drink)
    #return drink.index(kind)/len(drink)
def smoke_num(kind,smoke):
    return smoke.tolist().index(kind)/len(smoke)
    #return smoke.index(kind)/len(smoke)

def Analysis_3_match(request):
    df = pd.DataFrame(clientDetailInfoAll(),
                      columns=['clientidx', 'gender', 'age', 'religion', 'education', 'height', 'bodyshape', 'drink',
                               'smoke'])
    education = np.sort(df['education'].unique())
    bodyshape = np.sort(df['bodyshape'].unique())
    drink = np.sort(df['drink'].unique())
    smoke = np.sort(df['smoke'].unique())
    # education = ['고등학교','전문대','대학교','석사','박사','기타']
    # bodyshape = ['마름','슬림','보통','다소 볼륨','다소 근육','글래머','근육질','통통','우람']
    # drink = ['안 마심','1병 이하','1병-2병','2병 초과']
    # smoke = ['비흡연','가끔','종종','매일']

    likereceive=likereceivePeople()
    notlikereceive=notlikereceivePeople()
    likereceive = pd.DataFrame(likereceive,
                      columns=['age', 'education', 'height', 'bodyshape', 'drink',
                               'smoke'])
    notlikereceive = pd.DataFrame(notlikereceive,
                               columns=['age', 'education', 'height', 'bodyshape', 'drink',
                                        'smoke'])
    print('좋아요 받은 구성원',len(likereceive))
    print('좋아요 받은 구성원',len(notlikereceive))
    likereceiveRatio=len(likereceive)*100/(len(likereceive)+len(notlikereceive))
    notlikereceiveRatio=len(notlikereceive)*100/(len(likereceive)+len(notlikereceive))
    likereceiveRatio=math.floor(likereceiveRatio)
    notlikereceiveRatio=math.floor(notlikereceiveRatio)


    agemax=max([likereceive['age'].max(),notlikereceive['age'].max()])
    heightmax=max([likereceive['height'].max(),notlikereceive['height'].max()])
    likereceive['age'] = likereceive['age']/agemax
    likereceive['height'] = likereceive['height'] / heightmax
    likereceive['education'] = likereceive['education'].apply(lambda x: education_num(x, education))
    likereceive['bodyshape'] = likereceive['bodyshape'].apply(lambda x: bodyshape_num(x, bodyshape))
    likereceive['drink'] = likereceive['drink'].apply(lambda x: drink_num(x, drink))
    likereceive['smoke'] = likereceive['smoke'].apply(lambda x: smoke_num(x, smoke))

    notlikereceive['age'] = notlikereceive['age'] / agemax
    notlikereceive['height'] = notlikereceive['height'] / heightmax
    notlikereceive['education'] = notlikereceive['education'].apply(lambda x: education_num(x, education))
    notlikereceive['bodyshape'] = notlikereceive['bodyshape'].apply(lambda x: bodyshape_num(x, bodyshape))
    notlikereceive['drink'] = notlikereceive['drink'].apply(lambda x: drink_num(x, drink))
    notlikereceive['smoke'] = notlikereceive['smoke'].apply(lambda x: smoke_num(x, smoke))
    print(likereceive.mean())
    print(notlikereceive.mean())
    likereceiveMean=likereceive.mean()
    print(type(likereceiveMean))
    notlikereceiveMean=notlikereceive.mean()
    return render(request,"adminPage/Analysis_3_match.html",{'likereceiveMean':likereceiveMean,'notlikereceiveMean':notlikereceiveMean,'notlikereceiveRatio':notlikereceiveRatio,'likereceiveRatio':likereceiveRatio})
# def Analysis_4_customer(request):
#     return render(request,"adminPage/Analysis_4_customer.html")
def Analysis_5_complain(request):
    return render(request,"adminPage/Analysis_5_complain.html")
#----------------------------------------------------------------------------------
#접속 분석
def Analysis_6_login(request):
    resultDay=AnalysisLoginDay()
    resultMonth=AnalysisLoginMonth()
    resultYear=AnalysisLoginYear()
    return render(request,"adminPage/Analysis_6_login.html",{'resultDay':resultDay,'resultMonth':resultMonth,'resultYear':resultYear})
#--------------------------------------------------------------------------------------
def Complain_2_tingtodaylist(request):
    return render(request,"adminPage/Complain_2_tingtodaylist.html")
def Pay_0_list(request):
    countAll = countTable('payment')[0]
    cntPerPage = 10
    totalPage = int(countAll / cntPerPage) + 1
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    start = (page - 1) * cntPerPage + 1
    end = (page) * cntPerPage
    print('시작', start)
    print('끝', end)
    arr = (start, end)
    salesList=SalesList(arr)
    print(salesList)
    return render(request,"adminPage/Pay_0_list.html",{'salesList':salesList,'totalPage':totalPage,'page':page})

#------------------------------------------------------------------------------------
def Pay_1_basic_report(request):
    resultDay=AnalysisSalesDay()
    resultMonth=AnalysisSalesMonth()
    resultYear=AnalysisSalesYear()
    print(resultMonth)
    return render(request,"adminPage/Pay_1_basic_report.html",{'resultDay':resultDay,'resultMonth':resultMonth,'resultYear':resultYear})
#------------------------------------------------------------------------------------------
def Board_0_list(request):
    return render(request,"adminPage/Board_0_list.html")
def Notice_1_board(request):
    return render(request,"adminPage/Notice_1_board.html")
def Notice_2_chat(request):
    return render(request,"adminPage/Notice_2_chat.html")
def Notice_3_client(request):
    return render(request,"adminPage/Notice_3_client.html")

#blacklist 추가페이지
def blackList_1_insert(request):
    email=request.GET['email']
    return render(request,"adminPage/blackList_1_insert.html",{'email':email})

#blacklist 추가페이지
def qna_reply(request):
    email=request.GET['email']
    return render(request,"adminPage/qna_reply.html",{'email':email})

@csrf_protect
def insertBlacklist(request):
    email=request.POST['email']
    clientidx=getIdx(email)
    reason=request.POST['reason']
    blacklistinfo=(clientidx[0],reason)
    blacklist_insert(blacklistinfo)
    return redirect('/adminPage/Client_2_blacklist')

@csrf_protect
def insertreply(request):
    email=request.POST['email']
    clientidx=getIdx(email)
    reply=request.POST['reply']
    replyinfo=(clientidx[0],reply)
    reply_insert(replyinfo)
    return redirect('/adminPage/Client_2_replylist')
#___________________________________________________________________________________

from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.shortcuts import render
import pickle
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from collections import Counter
import matplotlib.pyplot as plt
#from gensim.models.word2vec import Word2Vec
import json
from collections import OrderedDict

#json파일 보내기 시도
load_ting_w2v_model=joblib.load('/home/kosmo_03/다운로드/tingAdmin/model/insta.model')
load_ting_svc_model=joblib.load('/home/kosmo_03/다운로드/tingAdmin/model/svc.pkl')
#load_ting_svc_model=joblib.load('../model/insta.model')
#load_ting_svc_model=joblib.load('../model/svc.pkl')

from konlpy.tag import Okt
okt=Okt()

#불용어 설정
stopwords = ['인스타그램','맞팔','팔로우','인친','럽스타그램','좋반','좋튀','술스타그램','멍스타그램','선팔하면맞팔','그램',
             '난','왜','안','은','들','는','좀','이면','잘','걍','과','도','를','으로','자','에','와','한','하다'
            ,'선팔','곧','이제','인','데','저','뭐','그램','스타','움','네','기','거','옹','이','살','때','것','도치','뒤','옆','나'
            ,'라며','때문','일이','그거','갑자기','중','더더','번','니','배송','상','슈','쇼','듯','그','로','스','디','정우'
             ,'정민','안나','트','면서','이기','부','김민우','송림로','고양동','임동혁','너','노','몇개','쟈','하려고',
            '이었는데','누가','일까','되며','여호와']

def get_noun(msg_txt):
    okt = Okt()
    nouns = list()
    if len(msg_txt) > 0:
        pos = okt.pos(msg_txt)
        #print(pos)
        for keyword, type in pos:
            # 고유명사 또는 보통명사
            #if type == "Noun":
            if type == "Noun" or type == "Adjective" or type == "Verb":
                nouns.append(keyword)
        #print(msg_txt, "->", nouns)
    nouns=list(filter(lambda x: x not in stopwords,nouns))
    print(nouns)
    return nouns

def to_vector(doc):
    """Create document vectors by averaging word vectors. Remove out-of-vocabulary words."""
    doc = [word for word in doc if word in load_ting_w2v_model.wv.vocab]
    #return doc
    return np.mean(load_ting_w2v_model[doc], axis=0)

@csrf_protect
def classification(request):
    selfIntro = request.GET['selfIntro']
    selfIntro_noun = get_noun(selfIntro)
    # selfIntro_noun
    selfIntro_vec = to_vector(selfIntro_noun)
    # selfIntro_vec
    predict = load_ting_svc_model.predict(np.array([selfIntro_vec]))
    print(predict[0])




    character_type=""

    if predict[0]=='사랑스러움':
        character_type='lovely'
    elif predict[0]=='사랑꾼':
        character_type='lover'
    elif predict[0]=='소심':
        character_type='passive'
    elif predict[0]=='장난꾸러기':
        character_type='naughty'
    elif predict[0]=='패피':
        character_type='fashion'
    elif predict[0]=='성실':
        character_type='diligent'
    elif predict[0]=='인싸':
        character_type='popular'
    else:
        character_type='naturalmeet'

    # 예측값에 해당하는 캐릭터 이름, 설명, 사진 가져오기
    character_info_arr = character_info(character_type)
    data=OrderedDict()
    data["character_type"]=character_type
    data["character_name"]=character_info_arr[0]
    data["character_explanation"]=character_info_arr[1]
    data["character_photo"]=character_info_arr[2]



    jsonp_callback = request.GET.get("callback")
    if jsonp_callback:
        response = HttpResponse("%s(%s);" % (jsonp_callback, json.dumps(data, ensure_ascii=False)))
        response["Content-type"] = "text/javascript; charset=utf-8"
    else:
        response = HttpResponse(json.dumps(data, ensure_ascii=False))
        response["Content-type"] = "application/json; charset=utf-8"
    return response



def login(request):
    return render(request,"adminPage/login.html")

@csrf_protect
def loginCheck(request):
    email=request.POST['email']
    password=request.POST['password']
    arr=(email,password)
    if loginChk(arr)[0]==1:
        request.session['email'] = email
        return redirect('/adminPage/index')
    else:
        return redirect('/adminPage/login')