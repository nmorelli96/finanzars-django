from django.shortcuts import render

tasas = {
    "inflacion": 12.7,
    "mercadopago": 95.2,
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
