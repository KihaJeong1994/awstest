

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
#json파일 보내기 시도
load_ting_w2v_model=joblib.load('/home/kosmo_03/notedir/tingPrj/insta.model')
load_ting_svc_model=joblib.load('/home/kosmo_03/notedir/tingPrj/svc.pkl')

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

#@csrf_protect
def classification():
    selfIntro = '저는 이벤트 하는 거 좋아하구요. 남자친구에게 많은 사랑 줄 준비 돼있어요!'
    selfIntro_noun = get_noun(selfIntro)
    # selfIntro_noun
    selfIntro_vec = to_vector(selfIntro_noun)
    # selfIntro_vec
    predict = load_ting_svc_model.predict(np.array([selfIntro_vec]))
    print(predict)
    #print(load_ting_w2v_model.wv.vocab.keys())
    #print(load_ting_svc_model)
        # pclassv = request.GET['room']
        # print(pclassv)
        # FirstClass, SecondClass, ThirdClass = 0, 0, 0
        # if pclassv == '1':
        #         FirstClass = 1
        # elif pclassv == 2:
        #         SecondClass = 1
        # else:
        #         ThirdClass = 1
        # test1 = np.array([[sexv, agev, FirstClass, SecondClass, ThirdClass]])
        # print(test1)
        # # x_test2=pd.DataFrame(test1,columns=['Sex','Age','Pclass'])
        # #scaler = StandardScaler()
        # test1 = scaler2.transform(test1)
        # #scaler.fit()
        # print('?',test1)
        # y = load_df_titanic_model.predict(test1)
        # print(y)
        # result=""
        # if y == 0:
        #         print('사망')
        #         result='사망'
        # else:
        #         print('생존')
        #         result = '생존'
        # #return render(request, 'testlogistic/result.html',{'result':result})
        # return HttpResponse(result)
classification()