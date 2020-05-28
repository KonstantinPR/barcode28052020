import os
from reportlab.pdfbase import ttfonts
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
registerFont(regular)
bold = ttfonts.TTFont('bold', os.path.join(fonts_dir, 'Helvetica-Bold.ttf'))
registerFont(bold)


def createBarCodes():
    """
    Create barcode examples and embed in a PDF
    """

    c = canvas.Canvas("barcodes.pdf")
    width_page = 50
    height_page = 70
    space_vertical = 5
    font_size = 5
    c.setPageSize((width_page, height_page))

    c.setFont('bold', font_size)

    c.drawString(0, height_page - font_size - space_vertical, "Торговая марка")
    c.drawString(0, height_page - font_size * 2 - space_vertical, "Вид товара")
    c.drawString(0, height_page - font_size * 3 - space_vertical, "Артикул товара")
    c.drawString(0, height_page - font_size * 4 - space_vertical, "Цвет товара")
    c.drawString(0, height_page - font_size * 5 - space_vertical, "Размер товара")

    barcode_value = "1234567890"
    barcode_eanbc13 = eanbc.Ean13BarcodeWidget(barcode_value)

    barcode_eanbc13.fontSize = 2
    barcode_eanbc13.barHeight = 8
    barcode_eanbc13.barWidth = 0.45
    d = Drawing()
    d.add(barcode_eanbc13)
    renderPDF.draw(d, c, 0, 0)
    c.save()


createBarCodes()

if __name__ == '__main__':
    createBarCodes()
