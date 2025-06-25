from django.urls import path
from .views import (
    menu_view, carga_view, carga_flexitank_view, carga_flexirampla_view,
    ver_cargas, finalizar_carga, ver_cargas_finalizadas,
    subir_imagenes_view, detalle_flexirampla, detalle_flexitank,
    exportar_cargas_excel, descargar_carga_pdf
)
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect  # ✅ necesario para la redirección inicial

urlpatterns = [
    # ✅ redirige raíz a login
    path('', lambda request: redirect('login')),

    # ✅ vistas protegidas
    path('menu/', login_required(menu_view), name='menu'),
    path('carga/', login_required(carga_view), name='carga'),
    path('carga/flexitank/', login_required(carga_flexitank_view), name='carga_flexitank'),
    path('carga/flexirampla/', login_required(carga_flexirampla_view), name='carga_flexirampla'),
    path('cargas/', login_required(ver_cargas), name='ver_cargas'),
    path('cargas/finalizar/<str:tipo>/<int:pk>/', login_required(finalizar_carga), name='finalizar_carga'),
    path('cargas-finalizadas/', login_required(ver_cargas_finalizadas), name='ver_cargas_finalizadas'),
    path('subir-imagenes/<str:tipo>/<int:pk>/', login_required(subir_imagenes_view), name='subir_imagenes'),
    path('detalle/flexitank/<int:id>/', login_required(detalle_flexitank), name='detalle_flexitank'),
    path('detalle/flexirampla/<int:id>/', login_required(detalle_flexirampla), name='detalle_flexirampla'),
    path('exportar/cargas/', login_required(exportar_cargas_excel), name='exportar_cargas'),
    path('exportar/cargas/finalizadas/', login_required(lambda req: exportar_cargas_excel(req, finalizadas=True)), name='exportar_cargas_finalizadas'),
    path('<str:tipo>/<int:pk>/descargar_pdf/', login_required(descargar_carga_pdf), name='descargar_carga_pdf'),

    # ✅ login y logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
