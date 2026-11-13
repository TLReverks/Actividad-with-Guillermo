from django.shortcuts import render
from django.http import HttpResponse
from .models import Libro

def inicio(request):
    libros = Libro.objects.all()

    return render(request, 'catalogo/inicio.html')

def listar_libros(request):
    libros = Libro.objects.all()

    contexto = {
        'libros': libros
    }

    return render(
        request,
        'catalogo/libros.html',
        contexto
    )


# Create your views here.
