from django.shortcuts import render,redirect
from .models import Post
from login.models import Account
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Create your views here.

def home(request):
    post = Post.objects.all()
    context = {'post':post} 
    if request.user.is_authenticated:
        now_login = Account.objects.get(user = request.user)
        context = {'post':post,'user':now_login}
    return render(request,'home.html',context)

def post(request):
    if request.method == 'POST':
        new_post = Post()
        title = request.POST.get('title')
        content = request.POST.get('content')
        new_post.title = title
        new_post.content = content
        new_post.pub_date = timezone.datetime.now()
        new_post.save()
    return render(request, 'post.html')

def detail(request, post_id):
    post = get_object_or_404(Post,pk=post_id)
    user = request.user
    account = Account.objects.get(user=user)
    context = {'post':post, 'account':account}
    return render(request,'detail.html',context)

def update_post(request, post_id):
    post_update = Post.objects.get(id = post_id)
    context = {'post':post_update}
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        post_update.title = title
        post_update.content = content
        post_update.pub_date = timezone.datetime.now()
        post_update.save()
        context = {"post":post_update}
        return render(request,'detail.html',context)

    return render(request,'post.html',context)


def delete_post(request,post_id):
    post_delete = Post.objects.get(id=post_id)
    post_delete.delete()
    return redirect('home')

def post_like(request,post_id):
    post = get_object_or_404(Post, id= post_id)
    user = request.user
    account = Account.objects.get(user=user)

    check_like_post = account.like_post.filter(id=post_id)

    if check_like_post.exists():
        account.like_post.remove(post)
        if post.like_num == 0:
            pass
        else:
            post.like_num -= 1
            post.save()
    else:
        account.like_post.add(post)
        post.like_num += 1
        post.save()

    return redirect('detail', post_id)