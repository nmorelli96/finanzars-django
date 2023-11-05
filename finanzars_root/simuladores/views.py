from django.shortcuts import render

tasas = {
    "inflacion": 12.7,
    "mercadopago": 100,
    "plazofijo": 133,
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
