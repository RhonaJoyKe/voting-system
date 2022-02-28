from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('', views.home, name='home'), 
    path('register/', views.create_user, name='register'), 
    path('login/', views.login_user, name='login'),
    path('candidate/', views.candidate, name='candidate'),
    path('position/', views.positionView, name='position'),
    path('candidate/<int:pos>/', views.candidateView, name='candidatelist'),
    path('candidate/detail/<int:id>/', views.candidate_delete, name='detail'),
    path('result/', views.resultView, name='result'),

]
if settings.DEBUG:

    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)