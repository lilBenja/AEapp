import pandas as pd
#import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CargaFlexitankForm, CargaFlexiramplaForm
from .models import CargaFlexitank, CargaFlexirampla, ImagenCarga
from django import forms
from django.utils.timezone import make_aware
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .decorators import solo_trabajador
from django.template.loader import get_template
from xhtml2pdf import pisa


@login_required
def menu_view(request):
    tipo_usuario = request.user.perfil.tipo_usuario if hasattr(request.user, 'perfil') else None
    return render(request, 'menu.html', {'tipo_usuario': tipo_usuario})

@login_required
#@solo_trabajador
def carga_view(request):
    return render(request, 'carga.html')

@login_required
#@solo_trabajador
def seleccionar_tipo_carga(request):
    if request.method == "POST":
        tipo_carga = request.POST.get("tipo_carga")
        request.session["tipo_carga"] = tipo_carga  # Guardamos la selección en la sesión
        return redirect("crear_carga")

    return render(request, "seleccionar_tipo_carga.html")


@login_required
#@solo_trabajador
def crear_carga(request):
    tipo_carga = request.session.get("tipo_carga", None)

    if tipo_carga == "Flexitank":
        form = CargaFlexitankForm(request.POST or None)
    else:
        form = CargaFlexiramplaForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            nueva_carga = form.save()  # Guarda la carga
            tipo = "flexitank" if tipo_carga == "Flexitank" else "flexirampla"
            return redirect("subir_imagenes", tipo=tipo, pk=nueva_carga.pk)

    return render(request, "crear_carga.html", {"form": form})

@login_required
#@solo_trabajador
def carga_flexitank_view(request):
    if request.method == "POST":
        form = CargaFlexitankForm(request.POST)
        if form.is_valid():
            nueva_carga = form.save()
            return redirect('subir_imagenes', tipo='flexitank', pk=nueva_carga.pk)
    else:
        form = CargaFlexitankForm()
    return render(request, 'carga_flexitank.html', {'form': form})

@login_required
#@solo_trabajador
def carga_flexirampla_view(request):
    if request.method == "POST":
        form = CargaFlexiramplaForm(request.POST)
        if form.is_valid():
            nueva_carga = form.save()
            return redirect('subir_imagenes', tipo='flexirampla', pk=nueva_carga.pk)
    else:
        form = CargaFlexiramplaForm()
    return render(request, 'carga_flexirampla.html', {'form': form})

@login_required
def ver_cargas(request):
    tipo = request.GET.get('tipo')
    empresa = request.GET.get('empresa')
    fecha = request.GET.get('fecha')

    flexitanks = CargaFlexitank.objects.filter(finalizar=False)
    flexiramplas = CargaFlexirampla.objects.filter(finalizar=False)

    # Aplicar filtros si están presentes
    if empresa:
        flexitanks = flexitanks.filter(empresa=empresa)
        flexiramplas = flexiramplas.filter(empresa=empresa)
    
    if fecha:
        flexitanks = flexitanks.filter(fecha_armado=fecha)
        flexiramplas = flexiramplas.filter(fecha_armado=fecha)

    # Filtro por tipo de carga
    if tipo == 'Flexitank':
        flexiramplas = []
    elif tipo == 'Flexirampla':
        flexitanks = []

    return render(request, 'ver_cargas.html', {
        'flexitanks': flexitanks,
        'flexiramplas': flexiramplas,
    })

class FinalizarCargaForm(forms.ModelForm):
    class Meta:
        model = CargaFlexitank  # se sobreescribe dinámicamente
        fields = ['comentarios', 'finalizar']
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 4}),
        }

@login_required
#@solo_trabajador
def finalizar_carga(request, tipo, pk):
    modelo = CargaFlexitank if tipo == 'flexitank' else CargaFlexirampla
    carga = get_object_or_404(modelo, pk=pk)

    if request.method == 'POST':
        form = FinalizarCargaForm(request.POST, instance=carga)
        if form.is_valid():
            form.save()
            return redirect('ver_cargas')
    else:
        form = FinalizarCargaForm(instance=carga)

    return render(request, 'finalizar_carga.html', {
        'form': form,
        'tipo': tipo,
        'carga': carga
    })

@login_required
def ver_cargas_finalizadas(request):
    tipo = request.GET.get('tipo')
    empresa = request.GET.get('empresa')
    fecha = request.GET.get('fecha')

    flexitanks = CargaFlexitank.objects.filter(finalizar=True)
    flexiramplas = CargaFlexirampla.objects.filter(finalizar=True)

    if empresa:
        flexitanks = flexitanks.filter(empresa=empresa)
        flexiramplas = flexiramplas.filter(empresa=empresa)

    if fecha:
        flexitanks = flexitanks.filter(fecha_armado=fecha)
        flexiramplas = flexiramplas.filter(fecha_armado=fecha)

    if tipo == 'Flexitank':
        flexiramplas = []
    elif tipo == 'Flexirampla':
        flexitanks = []

    return render(request, 'ver_cargas_finalizadas.html', {
        'flexitanks': flexitanks,
        'flexiramplas': flexiramplas,
    })


@login_required
#@solo_trabajador
def subir_imagenes_view(request, tipo, pk):
    modelo = CargaFlexitank if tipo == 'flexitank' else CargaFlexirampla
    campo_relacion = 'carga_flexitank' if tipo == 'flexitank' else 'carga_flexirampla'
    carga = get_object_or_404(modelo, pk=pk)

    if request.method == 'POST':
        for imagen in request.FILES.getlist('imagenes'):
            ImagenCarga.objects.create(
                imagen=imagen,
                **{campo_relacion: carga}
            )
        return redirect('menu')  # O redirige donde prefieras

    return render(request, 'subir_imagenes.html', {
        'tipo': tipo,
        'carga': carga
    })


@login_required
def detalle_flexitank(request, id):
    carga = get_object_or_404(CargaFlexitank, pk=id)
    context = {
        'carga': carga,
        'tipo': 'flexitank',  # <- esto es clave
    }
    return render(request, 'detalle_flexitank.html', context)

@login_required
def detalle_flexirampla(request, id):
    carga = get_object_or_404(CargaFlexirampla, pk=id)
    context = {
        'carga': carga,
        'tipo': 'flexirampla',  # <- esto es clave
    }
    return render(request, 'detalle_flexirampla.html', context)


@login_required
#@solo_trabajador
def exportar_cargas_excel(request, finalizadas=False):
    tipo = request.GET.get('tipo_carga')
    empresa = request.GET.get('empresa')
    fecha = request.GET.get('fecha')

    # Cargar ambas clases según el filtro finalizadas
    cargas_flexitank = CargaFlexitank.objects.filter(finalizar=finalizadas)
    cargas_flexirampla = CargaFlexirampla.objects.filter(finalizar=finalizadas)

    if tipo == 'Flexitank':
        cargas_flexirampla = CargaFlexirampla.objects.none()
    elif tipo == 'Flexirampla':
        cargas_flexitank = CargaFlexitank.objects.none()

    if empresa:
        cargas_flexitank = cargas_flexitank.filter(empresa=empresa)
        cargas_flexirampla = cargas_flexirampla.filter(empresa=empresa)

    if fecha:
        try:
            fecha_obj = make_aware(datetime.strptime(fecha, '%Y-%m-%d'))
            cargas_flexitank = cargas_flexitank.filter(fecha_armado=fecha_obj.date())
            cargas_flexirampla = cargas_flexirampla.filter(fecha_armado=fecha_obj.date())
        except:
            pass  # Si la fecha no es válida, ignoramos el filtro

    # Convertir a listas de diccionarios
    data_flexitank = list(cargas_flexitank.values(
        'empresa', 'numero_flexi', 'sello_flexi', 'numero_naviera',
        'fecha_armado', 'fierros_ref', 'litros_cargados', 'comentarios', 'contenedor'
    ))
    data_flexirampla = list(cargas_flexirampla.values(
        'empresa', 'numero_flexi', 'sello_flexi', 'numero_naviera',
        'fecha_armado', 'fierros_ref', 'litros_cargados', 'comentarios', 'patente_camion'
    ))

    # Añadir tipo de carga para diferenciarlos
    for item in data_flexitank:
        item['tipo'] = 'Flexitank'
    for item in data_flexirampla:
        item['tipo'] = 'Flexirampla'

    all_data = data_flexitank + data_flexirampla

    # Crear DataFrame y exportar
    df = pd.DataFrame(all_data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    nombre_archivo = "cargas_finalizadas.xlsx" if finalizadas else "cargas_pendientes.xlsx"
    response['Content-Disposition'] = f'attachment; filename={nombre_archivo}'
    df.to_excel(response, index=False)
    return response

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response

def descargar_carga_pdf(request, tipo, pk):
    if tipo == "flexitank":
        carga = CargaFlexitank.objects.get(pk=pk)
    else:
        carga = CargaFlexirampla.objects.get(pk=pk)

    return render_to_pdf('detalle_carga_pdf.html', {'carga': carga, 'tipo': tipo})