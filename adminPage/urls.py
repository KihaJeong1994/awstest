from django.urls import path

from adminPage import views
#여기가 컨트롤러 역할
urlpatterns=[
    path("",views.home),
    path("index",views.index),
    path("Analysis_1_inflow",views.Analysis_1_inflow),
    path("Analysis_2_properties",views.Analysis_2_properties),
    path("Analysis_3_match",views.Analysis_3_match),
    path("Analysis_4_customer",views.Analysis_4_customer),
    path("Analysis_5_complain",views.Analysis_5_complain),
    path("Analysis_6_login",views.Analysis_6_login),
    path("Client_0_list",views.Client_0_list),
    path("Client_2_blacklist",views.Client_2_blacklist),
    path("Ask_0_list",views.Ask_0_list),
    path("Ask_1_detail",views.Ask_1_detail),
    path("Complain_1_chatlist",views.Complain_1_chatlist),
    path("Complain_1_chatDetail",views.Complain_1_chatDetail),
    path("Complain_2_tingtodaylist",views.Complain_2_tingtodaylist),
    path("Pay_0_list",views.Pay_0_list),
    path("Pay_1_basic_report",views.Pay_1_basic_report),
    path("Board_0_list",views.Board_0_list),
    path("Notice_1_board",views.Notice_1_board),
    path("Notice_2_chat",views.Notice_2_chat),
    path("Notice_3_client",views.Notice_3_client),
    path("classification",views.classification),
    path("blackList_1_insert",views.blackList_1_insert),
    path("insertBlacklist",views.insertBlacklist),
    path("login",views.login),
    path("loginCheck",views.loginCheck),
    path("qna_reply",views.qna_reply),
    path("insertreply",views.insertreply),
    path("Client_2_replylist",views.Client_2_replylist),

]