from django.urls import path, include 

urlpatterns = [
    # path('admin', admin.site.urls),
    path('', include('users.urls')),
    path('', include('quizzes.urls')),
]