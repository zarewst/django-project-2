from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Category, Article
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages


# Create your views here.

# Функция для главной страницы
# def index(request):
#     articles = Article.objects.all()  # Вернётся список словарей
#     context = {
#         'title': 'Спорт Новости',
#         'articles': articles
#     }
#     return render(request, 'blog/index.html', context)
#   верни нарисуй(по запросу, куда , что отправить)

class ArticleListView(ListView):
    model = Article  # Указываем дял какой модели
    context_object_name = 'articles'  # по каким ключём передфём статьи
    template_name = 'blog/index.html'  # Говорим для какой страницы данный класс
    extra_context = {  # Отправлям не обходимое по ключами объекты
        'title': 'Спорт Новости'
    }


#  ------------------------------------------------------------------------------------------
# def category_view(request, pk):
#     articles = Article.objects.filter(category_id=pk)
#     category = Category.objects.get(pk=pk)
#     context = {
#         'title': f'Категория: {category.title}',
#         'articles': articles
#     }
#
#     return render(request, 'blog/index.html', context)


class ArticleListByCategory(ArticleListView):

    def get_queryset(self):
        articles = Article.objects.filter(category_id=self.kwargs['pk'])
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Категория: {category.title}'
        return context


#  ------------------------------------------------------------------------------------------

# def article_view(request, pk):
#     article = Article.objects.get(pk=pk)  # Получаем конкретную статью по id
#     context = {
#         'title': f'Статья: {article.title}',
#         'article': article
#     }
#     return render(request, 'blog/article_detail.html', context)


# Класс отвечает за страницу детали статьи
class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        article.views += 1
        article.save()
        context['title'] = f'Статья: {article.title}'

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        context['comments'] = Comment.objects.filter(article=article)
        return context


#  ------------------------------------------------------------------------------------------


# def add_article(request):
#     if request.method == 'POST':
#         form = ArticleForm(request.POST, request.FILES)  # Здесь получаем данные с формы ArticleForm
#         if form.is_valid():  # проверяем на валидность
#             article = Article.objects.create(**form.cleaned_data)  # В модель Article создаем новую статью
#             # метод cleaned_data распоковывает по ключам
#             article.save()
#             return redirect('article', article.pk)
#     else:
#         form = ArticleForm()
#     context = {
#         'form': form,
#         'title': 'Создание статьи'
#     }
#     return render(request, 'blog/add_article.html', context)


class NewArticle(CreateView):
    form_class = ArticleForm
    template_name = 'blog/add_article.html'
    extra_context = {
        'title': 'Создание статьи'
    }


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/add_article.html'
    extra_context = {
        'title': 'Изменить статью'
    }


class ArticleDelete(DeleteView):
    model = Article
    context_object_name = 'article'
    success_url = reverse_lazy('index')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Добро пожаловать')
                return redirect('index')
            else:
                messages.warning(request, 'Не верный логин или пароль')
                return redirect('login')
        else:
            messages.warning(request, 'Не верный логин или пароль')
            return redirect('login')

    else:
        form = LoginForm()

    context = {
        'title': 'Войти в Аккаунт',
        'form': form
    }
    return render(request, 'blog/login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Уже уходите???')
    return redirect('index')


class SearchResults(ArticleListView):
    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Article.objects.filter(title__icontains=word)
        return articles


# Функция для регистрации пользователя
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            form2 = ProfileForm(request.POST, request.FILES)
            if form2.is_valid():
                profile = form2.save(commit=False)
                profile.user = user
                profile.save()

                messages.success(request, 'Регистрация прошла успешно. Войдите в Аккаунт')
                return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
                return redirect('register')

    else:
        form = RegistrationForm()
        form2 = ProfileForm()

    context = {
        'title': 'Регистрация',
        'form': form,
        'form2': form2
    }

    return render(request, 'blog/register.html', context)


def save_comment(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = Article.objects.get(pk=pk)
        comment.user = request.user
        comment.save()
        messages.success(request, 'Ваш комментарий опубликован')
        return redirect('article', pk)


# Функция отвечающая за страницу Профиля
def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    articles = Article.objects.filter(author_id=pk)
    most_viewed = articles.order_by('-views')[:1][0]  # Получаю самую просматриваемую
    recent_articles = articles.order_by('-created_at')[:1][0]  # Получаю самую последнию

    context = {
        'profile': profile,
        'title': f'Пользователь: {profile.user.username}',
        'most_viewed': most_viewed,
        'recent_articles': recent_articles,
        'articles': articles
    }

    return render(request, 'blog/profile.html', context)




# Функция для страницы изменения данных Профиля и Аккаунта
def chg_profile_view(request):
    edit_account_form = EditAccountForm(instance=request.user if request.user.is_authenticated else None)
    edit_profile_form = ProfileForm(instance=request.user.profile if request.user.is_authenticated else None)
    context = {
        'form': edit_account_form,
        'form2': edit_profile_form,
        'title': 'Изменение данных'
    }

    return render(request, 'blog/chg_profile.html', context)


@login_required
def edit_account_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditAccountForm(request.POST, instance=request.user)
            form2 = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if form.is_valid() and form2.is_valid():
                data = form.cleaned_data
                form2.save()
                form.save()
                user = User.objects.get(id=request.user.id)
                if user.check_password(data['old_password']):
                    if data['old_password'] and data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.warning(request, 'Пароль успешно изменён')
                        return redirect('profile', user.pk)
                    else:
                        for field in form.errors:
                            messages.error(request, form.errors[field].as_text())
                            return redirect('chg_profile')
                else:
                    for field in form.errors:
                        messages.error(request, form.errors[field].as_text())
                        return redirect('chg_profile')

            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())
                    return redirect('chg_profile')
        else:
            messages.warning(request, 'Что то пошло ни так')
            return redirect('chg_profile')

        user = request.user
        return redirect('profile', user.pk)

    else:
        return redirect('login')













