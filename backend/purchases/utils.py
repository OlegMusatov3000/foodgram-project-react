from reportlab.pdfgen import canvas
from django.http import HttpResponse


def generate_shopping_cart_pdf(user):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shopping_cart.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Список покупок")

    p.showPage()
    p.save()

    return response
