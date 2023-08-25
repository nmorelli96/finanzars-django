from django.shortcuts import render

tasas = {
    "inflacion": 6.3,
    "mercadopago": 86.2,
    "plazofijo": 118,
}

def cuotas(request):
    
    context = {
        'tasas': tasas
    }

    return render(request, "cuotas.html", context)

def prestamos(request):
    
    context = {
        'tasas': tasas
    }

    return render(request, "prestamos.html", context)
