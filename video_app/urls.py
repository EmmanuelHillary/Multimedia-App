from django.urls import path
from .views import index, signup, logout_user, login_user, create_media, user_media, detail_media, delete, update

urlpatterns = [
    path('', index, name="home"), 
    path('signup/', signup, name="signup"),
    path('logout/', logout_user, name="logout"),
    path('login/', login_user, name="login"),
    path('create/', create_media, name="create"),
    path('vids/', user_media, name="vids"),
    path('detail/<int:id>/', detail_media, name="detail"),
    path('delete/<int:id>/', delete, name="delete"),
    path('update/<int:id>/', update, name="update"),
]
