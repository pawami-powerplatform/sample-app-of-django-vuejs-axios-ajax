import json

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from ajaxapp.forms import CreateCategoryForm
from ajaxapp.models import Category, TodoItem


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ShowItemView(generic.TemplateView):
    template_name = "show_todo_items.html"


def get_item(request):
    items = TodoItem.objects.filter(user=request.user).order_by("completed", "item_date", "category").values()
    item_list = list(items)
    categories = Category.objects.filter(user=request.user).values()
    category_list = list(categories)
    all_lists = {"items": item_list, "categories": category_list}
    return JsonResponse(all_lists, safe=False)


def post_update_item(request):
    if request.method == 'POST' and request.body:
        json_dict = json.loads(request.body)
        item = json_dict['item']
        item_date = json_dict['item_date']
        user = request.user
        completed = json_dict['completed']
        if not ('item_id' in json_dict.keys()):
            TodoItem.objects.create(item=item, item_date=item_date, completed=completed, user=user)
            items = TodoItem.objects.filter(user=user, item=item, item_date=item_date, completed=completed).values()
        else:
            item_id = json_dict['item_id']
            items = TodoItem.objects.get(pk=item_id)
            category_id = json_dict['category_id']
            items.item = item
            items.item_date = item_date
            items.completed = completed
            items.category_id = category_id
            items.save()
            items = TodoItem.objects.filter(pk=item_id).values()
        new_item = items[0]
        return JsonResponse(new_item)
    else:
        return HttpResponseServerError()


def post_delete_item(request):
    if request.method == 'POST' and request.body:
        json_dict = json.loads(request.body)
        item_id = json_dict['item_id']
        item = TodoItem.objects.get(pk=item_id)
        item.delete()
        return JsonResponse(json_dict)
    else:
        return HttpResponseServerError()


def show_category(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'category_setting.html', {'categories': categories})


def create_category(request):
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST or None)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, ('Created successfully!'))
        else:
            messages.success(request, ('error!'))
    return show_category(request)


def delete_category(request, category_id):
    item = Category.objects.get(pk=category_id)
    item.delete()
    messages.success(request, ('Deleted successfully!'))
    return redirect('show_category')

