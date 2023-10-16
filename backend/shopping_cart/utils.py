from io import BytesIO

from django.db.models import Sum
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from recipes.models import RecipeIngredient

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


def generate_shopping_list(user):
    ingredients = RecipeIngredient.objects.filter(
        recipe__shopping_cart_recipe__user=user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(
        amounts=Sum('amount', distinct=True)).order_by('amounts')

    shopping_list = ''

    for ingredient in ingredients:
        shopping_list += (
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["amounts"]} '
            f'{ingredient["ingredient__measurement_unit"]}\n'
        )

    return shopping_list


def generate_shopping_cart_pdf(request, user):
    shopping_list = generate_shopping_list(user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.pdf"'
    )
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Arial', 12)

    p.drawString(100, 750, 'Ваш список покупок:')

    # Add shopping list content
    y = 700
    for line in shopping_list.split('\n'):
        p.drawString(100, y, line)
        y -= 15

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
