from django.http import HttpResponse

def saludo(request) -> HttpResponse:
    return HttpResponse("¡Hola, mundo!")

def saludo_personalizado(request) -> HttpResponse:
    nombre = input("Ingrese tu nombre: ")
    return HttpResponse(f"¡Hola, <h1>{nombre}</h1>")

# Ahora una vista que recibe un parámetro de URL
def saludo_con_parametro(request, nombre: str) -> HttpResponse:
    return HttpResponse(f"¡Hola, <h1>{nombre}</h1>!")

# Lanzamiento del dado
# Si sale 6 !Felicitaciones, sino volver a tirar

def dado(request):
    from random import randint
    lanzamiento = randint(1,6)
    if lanzamiento == 6:
        return HttpResponse(f'Felicitaciones, obtuviste el numero {lanzamiento}')
    else:
        return HttpResponse(f'Has tirado el dado: {lanzamiento}, vuelve a intentar')
        
        
