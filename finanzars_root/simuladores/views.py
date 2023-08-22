from django.shortcuts import render


def cuotas(request):
    tasas = {
        "inflacion": 6.3,
        "mercadopago": 86.2,
        "plazofijo": 118,
    }

    context = {
        'tasas': tasas
    }

    return render(request, "cuotas.html", context)
