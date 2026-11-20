from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Libro, Categoria
from django.contrib import messages


def inicio(request):
    return render(request, 'catalogo/inicio.html')


def listar_libros(request):
    libros = Libro.objects.all()

    contexto = {'libros': libros}

    return render(request, 'catalogo/libros.html', contexto)


def listar_categorias(request):

    if request.method == 'POST':

        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()

        # Validar que el nombre no esté vacío
        if not nombre:

            messages.error(
                request,
                'El nombre de la categoría es obligatorio.'
            )

        # Validar que la categoría no esté duplicada
        elif Categoria.objects.filter(nombre__iexact=nombre).exists():

            messages.error(
                request,
                'Ya existe una categoría con ese nombre.'
            )

        else:

            Categoria.objects.create(
                nombre=nombre,
                descripcion=descripcion or None
            )

            messages.success(
                request,
                'La categoría se registró correctamente.'
            )

            return redirect('listar_categorias')

    categorias = Categoria.objects.all()

    contexto = {
        'categorias': categorias
    }

    return render(request, 'catalogo/categorias.html', contexto)
