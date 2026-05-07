from django.urls import path 

from .import views 


urlpatterns=[ 
    path('',views.home,name='home'),
    path('register',views.register,name='reg'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('fertilizer',views.fertilizer,name='fertilizer'),
    path('predict',views.fertilizer,name='fertilizer'),
    path('crop',views.crop,name='crop'),
    path('crop_predict',views.crop_predict,name='croppredict')

]