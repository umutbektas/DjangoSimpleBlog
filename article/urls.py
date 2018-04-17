from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    path('', views.allArticles, name="allArticles"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('add/', views.addArticle, name="addArticle"),
    path('detail/<int:id>', views.detailArticle, name="detailArticle"),
    path('edit/<int:id>', views.editArticle, name="editArticle"),
    path('delete/<int:id>', views.deleteArticle, name="deleteArticle"),
    path('search/', views.searchArticle, name="searchArticle"),
    path('comment/<int:id>', views.commentArticle, name="commentArticle"),
]