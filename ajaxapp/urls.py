from django.urls import path

from ajaxapp import views

urlpatterns = [
    path('', views.ShowItemView.as_view(), name='show_item'),
    path('get_item/', views.get_item, name='get_item'),
    path('post_update_item/', views.post_update_item, name='post_update_item'),
    path('post_delete_item/', views.post_delete_item, name='post_delete_item'),
    path('show_category/', views.show_category, name='show_category'),
    path('create_category/', views.create_category, name='create_category'),
    path('delete_category/<category_id>', views.delete_category, name='delete_category'),
]