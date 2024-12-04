from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.urls import views as auth_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')), 
    path('admin-dj/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('user.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('api_blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
