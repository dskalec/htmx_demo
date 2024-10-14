from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy

from .models import Todo


class TodoListView(ListView):
    model = Todo
    template_name = "todo/list.html"
    context_object_name = "todos"


class TodoCreateView(CreateView):
    model = Todo
    template_name = "todo/form.html"
    fields = ["title"]
    success_url = reverse_lazy("todo_list")


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = "todo/form.html"
    fields = ["title", "completed"]
    success_url = reverse_lazy("todo_list")


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "todo/confirm_delete.html"
    success_url = reverse_lazy("todo_list")
