from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.urls import reverse_lazy

from .forms import TodoForm
from .models import Todo


class TodoListView(ListView):
    model = Todo
    template_name = "todo/list.html"
    context_object_name = "todos"


class TodoCreateView(CreateView):
    model = Todo
    form_class = TodoForm
    template_name = "todo/form.html"
    success_url = reverse_lazy("todo_list")


class TodoUpdateView(UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "todo/form.html"
    success_url = reverse_lazy("todo_list")


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "todo/confirm_delete.html"
    success_url = reverse_lazy("todo_list")


@csrf_exempt
def ajax_complete_todo_view(request, pk):
    if request.method == 'POST':
        try:
            todo = Todo.objects.get(pk=pk)
            todo.completed = not todo.completed
            todo.completed_at = now() if todo.completed else None
            todo.save()

            # Render the updated checkbox and badge
            html = render_to_string('todo/item_checkbox.html', {'todo': todo})
            return HttpResponse(html)
        except Todo.DoesNotExist:
            return HttpResponse("Todo not found", status=404)
    return HttpResponse("Invalid request", status=400)