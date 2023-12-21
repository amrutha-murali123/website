
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from users.views import Custom404View
from django.contrib.staticfiles.views import serve

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include('users.urls')),
    path("", include('product.urls')),
    path("", include('shoppingcart.urls')), 
    path("rosetta/",include('rosetta.urls')),
    path("ckeditor/',",include('ckeditor_uploader.urls')),
    prefix_default_language=False
    

)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         path("__debug__/", include(debug_toolbar.urls)),
#     ]
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # urlpatterns += [
    #     re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS}),
    # ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns += [
#     re_path(r'^.*$', Custom404View.as_view(), name='custom_404'),
# ]

