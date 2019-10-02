from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    url(r'^$',views.home, name = "home"),
    url(r'login/', views.login_user, name = 'login'),
    url(r'^logout/$', views.logout_user, name= "logout"),

    #----------------------------------------------------------------------------
    url(r'^profile/(?P<user_name>\w+)/$', views.profile_user, name= "profile"),
    #---------------------------------------------------------------------------
    url(r'^register/$', views.register_user, name= "register"),
    url(r'^edit_profile/$', views.edit_profile, name = "edit_profile"),
    url(r'^dashboard/(?P<user_name>\w+)/$', views.dashboard, name = "dashboard"),
    
    #Password Change URL............
    url(r'^change_password/$', views.change_password, name = "change_password"),

    #password Reset URLS...........
    path('password_reset/', PasswordResetView.as_view(), name='password_reset' ),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #Email Confirm URLs.....
    
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<id>\d+)/$',views.activateinform, name='activate'),

    #Contact Us Page ...
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^search/$', views.search, name="search"),
    url(r'^information/$', views.InformationView, name="information"),
    url(r'^informationedit/(?P<id>\d+)/$', views.InformationViewEdit, name='informationedit'),
    url(r'^informationedit1/(?P<id>\d+)/$', views.InformationViewEdit1, name='informationedit1'),


]