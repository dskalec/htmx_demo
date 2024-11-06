from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from django.utils.timezone import now

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
            completed = request.POST.get('completed') == 'true'
            todo.completed = completed
            todo.completed_at = now() if completed else None
            todo.save()
            return JsonResponse(
                {
                    'status': 'ok',
                    'completed': todo.completed,
                    'completed_at': todo.completed_at.strftime('%Y-%m-%d %H:%M:%S') if todo.completed_at else ''
                }
            )
        except Todo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Todo not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
