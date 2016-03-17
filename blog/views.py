from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Post #같은 앱으로 묶을때는 . 으로 시작하면 됨.
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from .models import Category
from .forms import PostForm
from .forms import PostEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import PermissionDenied


def hello(request):
    res = HttpResponse('hello world')
    return res

def hello_with_template(request):
    return render(request, 'hello.html')  #첫번째 함수로 항상 request함수를 받음.

def list_posts(request):

    all_posts = Post.objects.all()
    per_page = 2
    current_page = request.GET.get('page', 1)

    pagi = Paginator(all_posts, per_page)
    try:
        pg = pagi.page(current_page)
    except PageNotAnInteger:
        pg = pagi.page(1)
    except EmptyPage:
        pg = []

    #1대 다 경우, select_related 사용하여 한번에 데이터 긁어옴. 결과는 같으나 성능에 차이가 있음.

    return render(request, 'list_posts.html', {
        'posts' : pg,
    })

def view_post(request, pk):

    the_post = get_object_or_404(Post, pk=pk)

    return render(request, 'view_post.html', {
    'post' : the_post,
    })

@login_required
def create_post(request):
    if not request.user.is_authenticated():
        raise Exception('누구세요?')

    categories = Category.objects.all()

    if request.method =='GET':
        form = PostEditForm()
    elif request.method == 'POST':
        form = PostEditForm(request.POST)
        # 검증을 위해 메소드를 호출해 줘야 한다.
        #isValid 메서드는 한방에 해줌.
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('view_post', pk=new_post.pk)

    return render(request, 'create_post.html', {
    'categories' : categories,
    'form' : form,
    })

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        post = get_object_or_404(Post, pk=pk)
        categories = Category.objects.all()
    else:
        form = request.POST
        category = get_object_or_404(Category, pk=form['category'])
        post.title = form['title']
        post.content = form['content']
        post.category = category
        post.save()
        return redirect('view_post', pk=pk)

    return render(request, 'edit_post.html', {
    'post' : post,
    'categories' : categories,
    })

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        raise PermissionDenied
        #PermissionDenied 랑 return 리다이렉트 login 해주는거랑 뭐가 다름?
        # return redirect('login_url')

    if request.method =='POST':
        post.delete()
        return redirect('list_posts')

    return render(request, 'delete_post.html', {
    'post': post,
    })

def delete_comment(request, pk):
    comment = get_object_or_404(Post, pk=pk)
    if request.method =='POST':
        comment.delete()
        return redirect('list_post')

    return render(request, 'delete_comment.html', {
     'comment': comment,
     })
