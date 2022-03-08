from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>",views.entry_page_view, name="entry_page"),
    path("search", views.search, name="search"),
    path("create_page", views.create_page_view, name="create_page"),
    path("edit/<str:title>", views.edit_view, name="edit"),
    path("update", views.update_view, name="update_page"),
    path("random", views.random_view, name="random"),
]
