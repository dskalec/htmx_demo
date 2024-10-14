from django.urls import path

from .views import TodoCreateView, TodoDeleteView, TodoListView, TodoUpdateView

urlpatterns = [
    path("", TodoListView.as_view(), name="todo_list"),
    path("add/", TodoCreateView.as_view(), name="todo_add"),
    path("edit/<int:pk>", TodoUpdateView.as_view(), name="todo_edit"),
    path("delete/<int:pk>", TodoDeleteView.as_view(), name="todo_delete")
]
