from django.http import HttpResponse, QueryDict
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


@csrf_exempt
def ajax_delete_todo_view(request, pk):
    if request.method == 'DELETE':
        try:
            todo = Todo.objects.get(pk=pk)
            todo.delete()
            return HttpResponse(status=200)  # No Content, as we just want to remove it
        except Todo.DoesNotExist:
            return HttpResponse("Todo not found", status=404)
    return HttpResponse("Invalid request", status=400)


@csrf_exempt
def ajax_edit_todo_view(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
        if request.method == 'GET':
            html = render_to_string('todo/item_edit_form.html', {'todo': todo})
            return HttpResponse(html)
        elif request.method == 'PUT':
            data = QueryDict(request.body)
            todo.title = data.get('title')
            todo.description = data.get('description')
            todo.save()
            html = render_to_string('todo/item.html', {'todo': todo})
            return HttpResponse(html)
    except Todo.DoesNotExist:
        return HttpResponse("Todo not found", status=404)
    return HttpResponse("Invalid request", status=400)

def ajax_cancel_edit_todo_view(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
        html = render_to_string('todo/item.html', {'todo': todo})
        return HttpResponse(html)
    except Todo.DoesNotExist:
        return HttpResponse("Todo not found", status=404)


def ajax_new_todo_form_view(request):
    """ Renders the new todo form for htmx """
    html = render_to_string("todo/item_new_form.html")
    return HttpResponse(html)


@csrf_exempt
def ajax_create_todo_view(request):
    """ Creates a new todo and returns the new item HTML """
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        if title:
            todo = Todo.objects.create(title=title, description=description)
            html = render_to_string("todo/item.html", {"todo": todo})
            return HttpResponse(html)

    return HttpResponse("Invalid request", status=400)


def ajax_cancel_new_todo_view(request):
    return HttpResponse("")