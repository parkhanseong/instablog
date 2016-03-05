from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Post #같은 앱으로 묶을때는 . 으로 시작하면 됨.
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from .models import Category

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

def create_post(request):
    categories = Category.objects.all()

    if request.method =='GET':
        pass
    elif request.method == 'POST':
        new_post = Post()
        new_post.title = request.POST.get('title')
        new_post.content = request.POST.get('content')

        category_pk = request.POST.get('category')
        category = get_object_or_404(Category, pk=category_pk)
        new_post.category = category
        new_post.save()

        return redirect('view_post', pk=new_post.pk)

    return render(request, 'create_post.html', {
    'categories' : categories,
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

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method =='POST':
        post.delete()
        return redirect('list_post')

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
