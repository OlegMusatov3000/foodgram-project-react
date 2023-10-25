from io import BytesIO

from django.db.models import Sum
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from foodgram_backend.settings import STATIC_ROOT
from recipes.models import RecipeIngredient

pdfmetrics.registerFont(TTFont('Arial', f'{STATIC_ROOT}/font/arial.ttf'))


def generate_pdf_file(user):
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

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Arial', 12)

    p.drawString(100, 750, 'Ваш список покупок:')

    y = 700
    for line in shopping_list.split('\n'):
        p.drawString(100, y, line)
        y -= 15

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    return pdf
