from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Account

# Create your views here.
def signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2') 
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')

        if user_id == ""or nickname =="" or email == "" or pw1 == "" or pw2 == "":
            messages.info(request,"모든 항목을 채워주세요.")
            return redirect('signup')
        
                # 비밀번호가 다를 때
        if not pw1 == pw2:
            messages.info(request, "비밀번호가 다릅니다.")
            return redirect('signup')

        
        user = User.objects.create_user(username=user_id, password=pw1)
        user.save()
        account = Account(user=user, email=email, nickname=nickname)
        account.save()
        return redirect('login')
    else:
        return render(request, 'signup.html')
    return render(request,'signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST['id']
        password = request.POST["password"]
        
        #사용자가 입력한 정보에 따라 인증 과정
        user = auth.authenticate(request, username=username, password=password)

        # 유저 정보를 확인한 경우
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
        # 확인된 회원 정보가 없을 경우
            messages.info(request, "회원정보가 일치하지 않습니다.")
            return redirect('login')
    else:
        return render(request, 'login.html')
    return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')

def modify_user(request):
    now_user = Account.objects.get(user = request.user)
    context = {'account':now_user}
    if request.method == 'POST':
        user_id = request.POST.get('id')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2') 
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')

        if user_id == ""or nickname =="" or email == "" or pw1 == "" or pw2 == "":
            messages.info(request,"모든 항목을 채워주세요.")
            return redirect('signup')
        
                # 비밀번호가 다를 때
        if not pw1 == pw2:
            messages.info(request, "비밀번호가 다릅니다.")
            return redirect('signup')

        
        user = now_user.user
        user.username = user_id
        user.password = pw1
        user.save()
        account = Account(user=user, email=email, nickname=nickname)
        account.save()
        return redirect('home')
    else:
        return render(request, 'modify.html',context)
    return render(request,'modify.html',context)