from django.urls import path
from .views import JobList, JobDetail, JobCreate, JobDetailUpdate, JobDelete, UserLoginView, UserRegistration
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', JobList.as_view(), name='jobs'),
    path('job-detail/<int:pk>/', JobDetail.as_view(), name='job-detail'),
    path('job-create/', JobCreate.as_view(), name='job-create'),
    path('detail-update/<int:pk>/', JobDetailUpdate.as_view(), name='detail-update'),
    path('delete-job/<int:pk>/', JobDelete.as_view(), name='delete-job'),
]