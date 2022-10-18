from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from .views import print_category
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('subcategory/<str:cat>/', views.HomeView.as_view(), name='subcategory'),
    path('postdetail/<int:id>/', views.postDetail, name='postdetail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('search/', views.search, name='search'),
    path('account_verify/<slug:token>', views.account_verify, name='account_verify'),
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'login'), name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name = 'blog_app/passwordchange.html', form_class = MyPasswordChangeForm, success_url = '/profile/', extra_context = {'ctgry':print_category()}), name='passwordchange'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'blog_app/password_reset.html', form_class = MyPasswordResetForm, extra_context = {'ctgry':print_category()}), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='blog_app/password_reset_done.html', extra_context = {'ctgry':print_category()}), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'blog_app/password_reset_confirm.html', form_class=MySetPasswordForm, extra_context = {'ctgry':print_category()}), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'blog_app/password_reset_complete.html', extra_context = {'ctgry':print_category()}), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
