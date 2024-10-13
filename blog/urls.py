from django.urls import path
from .views import *

urlpatterns = [
    # Функции
    # path('', index, name='index'),
    # path('category/<int:pk>', category_view, name='category'),
    # path('article/<int:pk>', article_view, name='article'),
    # path('add_article/', add_article, name='add_article'),

    # Классы
    path('', ArticleListView.as_view(), name='index'),
    path('category/<int:pk>', ArticleListByCategory.as_view(), name='category'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article'),
    path('add_article/', NewArticle.as_view(), name='add_article'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='delete'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('search/', SearchResults.as_view(), name='search'),
    path('register/', register, name='register'),
    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('chg_profile/', chg_profile_view, name='chg_profile'),
    path('edit_account/', edit_account_profile, name='edit_account')


]
