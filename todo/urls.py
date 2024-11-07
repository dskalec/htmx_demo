from django.urls import path

from .views import (
    TodoCreateView, TodoDeleteView, TodoListView, TodoUpdateView,
    ajax_complete_todo_view, ajax_delete_todo_view, ajax_edit_todo_view, ajax_cancel_edit_todo_view,
    ajax_new_todo_form_view, ajax_create_todo_view, ajax_cancel_new_todo_view
)

urlpatterns = [
    path("", TodoListView.as_view(), name="todo_list"),
    path("add/", TodoCreateView.as_view(), name="todo_add"),
    path("edit/<int:pk>", TodoUpdateView.as_view(), name="todo_edit"),
    path("delete/<int:pk>", TodoDeleteView.as_view(), name="todo_delete"),
    path("ajax-complete/<int:pk>/", ajax_complete_todo_view, name="ajax_complete"),
    path("ajax-delete/<int:pk>/", ajax_delete_todo_view, name="ajax_delete"),
    path("ajax-edit/<int:pk>/", ajax_edit_todo_view, name="ajax_edit_todo"),
    path("ajax-cancel-edit/<int:pk>/", ajax_cancel_edit_todo_view, name="ajax_cancel_edit_todo"),
    path("ajax-new-todo-form/", ajax_new_todo_form_view, name="ajax_new_todo_form"),
    path("ajax-create-todo/", ajax_create_todo_view, name="ajax_create_todo"),
    path("ajax-cancel-new-todo/", ajax_cancel_new_todo_view, name="ajax_cancel_new_todo"),
]
