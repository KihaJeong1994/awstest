from django.shortcuts import render


from django.views.decorators.csrf import csrf_protect


def home(request):
    return render(request,"adminPage/index.html")
def index(request):
    return render(request,"adminPage/index.html")
def test(request):
    return render(request,"adminPage/test.html")
def Analysis_1_inflow(request):
    return render(request,"adminPage/Analysis_1_inflow.html")
def Analysis_2_properties(request):
    return render(request,"adminPage/Analysis_2_properties.html")
def Analysis_3_match(request):
    return render(request,"adminPage/Analysis_3_match.html")
def Analysis_4_customer(request):
    return render(request,"adminPage/Analysis_4_customer.html")
def Analysis_5_complain(request):
    return render(request,"adminPage/Analysis_5_complain.html")
def Client_0_list(request):
    return render(request,"adminPage/Client_0_list.html")
def Client_2_blacklist(request):
    return render(request,"adminPage/Client_2_blacklist.html")
def Ask_0_list(request):
    return render(request,"adminPage/Ask_0_list.html")
def Ask_1_detail(request):
    return render(request,"adminPage/Ask_1_detail.html")
def Complain_1_chatlist(request):
    return render(request,"adminPage/Complain_1_chatlist.html")
def Complain_2_tingtodaylist(request):
    return render(request,"adminPage/Complain_2_tingtodaylist.html")
def Pay_0_list(request):
    return render(request,"adminPage/Pay_0_list.html")
def Pay_1_basic_report(request):
    return render(request,"adminPage/Pay_1_basic_report.html")
def Board_0_list(request):
    return render(request,"adminPage/Board_0_list.html")
def Notice_1_board(request):
    return render(request,"adminPage/Notice_1_board.html")
def Notice_2_chat(request):
    return render(request,"adminPage/Notice_2_chat.html")
def Notice_3_client(request):
    return render(request,"adminPage/Notice_3_client.html")