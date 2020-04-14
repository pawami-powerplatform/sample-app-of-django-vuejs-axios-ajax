from django import forms

from ajaxapp.models import TodoItem, Category


class CreateItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['item', 'item_date']


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name"]
