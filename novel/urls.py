from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('', views.publisher_form, name='home'),
    path('author/',views.author_form,name='author'),
    path('book/',views.book_form,name='book'),
    path('all_books/',views.all_books,name='all_books'),
    path('publisher/',views.publisher_form,name='publisher'),
    path('auth_details/',views.auth_details,name='auth_det'),
    path('pub_more_than_two/',views.auth_pub_more_than_2,name='filtered'),
    path('pub_detail/<int:id>/',views.pub_detail,name='pub_detail'),
    path('pattern_book_search/',views.pattern_book_search,name="pattern_book_search"),
    path('pub_more_than_five/',views.auth_pub_more_than_5,name='specific_filtered'),
    path('pub_filtered_datetime/',views.pub_specific_duration,name="pub_specific_duration"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)