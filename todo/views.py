from django.views.generic import ListView

from .models import Todo


class TodoListView(ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    context_object_name = 'todos'
