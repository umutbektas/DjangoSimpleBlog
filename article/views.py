from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import AddArticleForm
from django.contrib import messages
from .models import Article, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def allArticles(request):
    articles = Article.objects.all()
    return render(request, "allArticles.html", {"articles":articles})

@login_required(login_url="user:loginUser")
def dashboard(request):
    articleObj = Article.objects.filter(author=request.user)
    articles = {
        "articles": articleObj
    }
    return render(request, "dashboard.html",articles)

@login_required(login_url="user:loginUser")
def addArticle(request):
    form = AddArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale başarıyla eklendi !")
        return redirect("article:dashboard")

    return render(request, "addArticle.html",{"form":form})

def detailArticle(request, id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id = id)
    comments = article.comments.all()

    return render(request, "detailArticle.html", {"article":article, "comments":comments})

@login_required(login_url="user:loginUser")
def editArticle(request, id):
    article = get_object_or_404(Article, id=id, author=request.user)
    form = AddArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale başarıyla güncellendi !")
        return redirect("article:dashboard")

    else:
        return render(request, "editArticle.html", {"form":form})

@login_required(login_url="user:loginUser")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id, author=request.user)
    article.delete()
    messages.success(request, "Makale başarıyla silindi !")
    return redirect("article:dashboard")

def searchArticle(request):
    searchkey = request.GET.get("searchkey")
    if searchkey:
        articles = Article.objects.filter(title__contains=searchkey) | Article.objects.filter(content__contains=searchkey)
        return render(request, "allArticles.html", {"articles":articles})
    else:
        return redirect("index")


def commentArticle(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        comment_author = request.user
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author=comment_author, comment_content=comment_content)
        newComment.article = article
        newComment.save()
    return redirect(reverse("article:detailArticle", kwargs={"id":id}))
