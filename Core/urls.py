from django.urls import path
from .views import MainApiView, MainPage, MangaTitleDetailView, GoToRead, AddMangaTitle, AddMangaChapter, Update, show_title, chapter_frame, extraUpdate, update_title

urlpatterns = [
    path(r'api/v1/', MainApiView.as_view()),
    path(r'', MainPage.as_view(), name='main-page'),
    path(r'title/<int:pk>/', MangaTitleDetailView.as_view(), name='detail-page'),
    path(r'read/<int:pk>/', GoToRead, name='read'),
    path(r'add/title', AddMangaTitle.as_view(), name='add-title-page'),
    path(r'title/<int:pk>/add/chapter', AddMangaChapter.as_view(), name='add-chapter-page'),
    path(r'update/', Update, name='read'),
    path(r'title/<slug:title_slug>/', show_title, name='title'),
    path(r'title/<slug:title_slug>/update/', update_title, name='title'),
    path(r'title/frame/<int:chapter_id>', chapter_frame, name='frame'),
    path(r'extraUpdate/', extraUpdate, name="extraUpdate")
]