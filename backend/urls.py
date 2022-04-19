from django.conf.urls import url, include
from django.urls import path
from django.views.generic import TemplateView

from backend.views import site_views, setting_views

from backend.routes import operators, card_logs

urlpatterns = [

    # site
    url(r'^site/contact/$', site_views.contact, name='site_contact'),

    # settings
    url(r'^settings/$', setting_views.index, name='settings_index'),
    url(r'^settings/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
    # file upload
    url(r'^settings/upload/$', setting_views.temp_upload, name='temp_upload'),
    # qr code
    url(r'^settings/qrcode/(?P<size>\d+)/(?P<text>.+)/$',
        setting_views.get_qr_code_image, name='get_qr_code_image'),
    # database update
    url(r'^settings/update-database/$', setting_views.update_database,
        name='settings_update_database'),

    # upload excel
    url(r'^settings/excel-import/$', setting_views.excel_import,
        name='settings_excel_import'),
    url(r'^settings/excel-import/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    path('', include('api.urls')),
    path('api/', include('api.urls')),
]

urlpatterns += operators.urlpatterns
urlpatterns += card_logs.urlpatterns
