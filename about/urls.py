from django.urls import path
from .views import about, add_section, edit_section, delete_section

urlpatterns = [
    path('', about, name='about'),
    path(
        'add_section/',
        add_section,
        name='add_section'
    ),
    path(
        'edit_section/<int:section_id>/',
        edit_section,
        name='edit_section'
    ),
    path(
        'delete_section/<int:section_id>/',
        delete_section,
        name='delete_section'
    ),
]
