from django.shortcuts import render

tasas = {
    "inflacion": 12.8,
    "mercadopago": 95,
    "plazofijo": 110,
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
