import os
from reportlab.pdfbase import ttfonts
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.graphics.barcode import eanbc
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF

current_dir = os.path.dirname(os.path.realpath(__file__))

# fonts
fonts_dir = os.path.join(current_dir, 'fonts')
regular = ttfonts.TTFont('regular', os.path.join(fonts_dir, 'Helvetica.ttf'))
bold = ttfonts.TTFont('bold', os.path.join(fonts_dir, 'Helvetica-Bold.ttf'))
registerFont(regular), registerFont(bold)

# setting canvas and constants
c = canvas.Canvas("barcodes.pdf")
width_page = 50
height_page = 70
space_vertical = 5
font_size = 5
c.setPageSize((width_page, height_page))
c.setFont('bold', font_size)


def generate_text_strings(height_page: int, font_size: int, space_vertical: int, text_values: list):
    """
    to put values into label string by string with auto-stretching
    """
    for text, i in zip(text_values, range(len(text_values))):
        current_font_size = font_size
        # auto-stretching by finding right font_size depenging of width text-string
        while stringWidth(text, 'bold', current_font_size, encoding='utf8') > width_page:
            current_font_size -= 1
        c.setFont('bold', current_font_size)
        c.drawString(0, height_page - font_size * i - space_vertical, text)
    return None


def createBarCodes():
    """
    Create barcode examples and embed in a PDF
    """
    text_values = ['Торговая марка',
                   'Вид товара',
                   'Артикул товара',
                   'Цвет товара',
                   'Размер товара неуютный',
                   'Морда слона',
                   'Соломенная смола из воска']

    generate_text_strings(height_page, font_size, space_vertical, text_values)

    barcode_value = "1234567890"
    barcode_eanbc13 = eanbc.Ean13BarcodeWidget(barcode_value)

    barcode_eanbc13.fontSize = 3
    barcode_eanbc13.barHeight = 8
    barcode_eanbc13.barWidth = 0.45
    d = Drawing()
    d.add(barcode_eanbc13)
    renderPDF.draw(d, c, 0, 0)
    c.save()


if __name__ == '__main__':
    createBarCodes()
