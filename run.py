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
regular = ttfonts.TTFont('regular', os.path.join(fonts_dir, 'OpenSans-Bold.ttf'))
bold = ttfonts.TTFont('bold', os.path.join(fonts_dir, 'OpenSans-Regular.ttf'))
registerFont(regular), registerFont(bold)

# setting canvas and constants
c = canvas.Canvas("barcodes.pdf")
width_page = 50
height_page = 70
indent_percent_vertical = 10
indent_percent_horizontal = 5
left_indent = width_page * indent_percent_horizontal / 100
right_indent = width_page * indent_percent_horizontal / 100
top_indent = height_page * indent_percent_vertical / 100
bottom_indent = height_page * indent_percent_vertical / 100
space_vertical_default = 5
space_horizontal_default = 2
font_size = 5
font_size_default = 2
fontSize_barcode = 3
barHeight_barcode = 10
barWidth_barcode = 0.45
c.setPageSize((width_page, height_page))
c.setFont('bold', font_size)


def generate_text_strings_top(height_page: int, font_size: int, space_vertical: int, text_values: list):
    """
    to put values into label string by string with auto-stretching
    """
    for text, i in zip(text_values, range(len(text_values))):
        # auto-stretching by finding right font_size depending of width text-string
        current_font_size = font_size
        while stringWidth(text, 'bold', current_font_size, encoding='utf8') > width_page:
            current_font_size -= 0.5
        string_width = stringWidth(text, 'bold', current_font_size, encoding='utf8')
        x = (width_page - string_width) / 2
        y = height_page - font_size * i - space_vertical - top_indent
        c.setFont('bold', current_font_size)
        c.drawString(x, y, text)
    return y


def generate_text_strings_middle(height_page: int, font_size: int, space_vertical: int, text_values2: list,
                                 start_height_position):
    """
    to put values into label string by string with auto-stretching
    """
    for text, i in zip(text_values2, range(len(text_values2))):
        # auto-stretching by finding right font_size depending of width text-string
        current_font_size = font_size
        while stringWidth(text, 'bold', current_font_size, encoding='utf8') > width_page:
            current_font_size -= 0.5
        string_width = stringWidth(text, 'bold', current_font_size, encoding='utf8')
        x = (width_page - string_width) / 2
        y = start_height_position - font_size * i - font_size - space_vertical
        c.setFont('bold', current_font_size)
        c.drawString(x, y, text)
    return y


def generate_text_strings_bottom(height_page: int, font_size: int, space_vertical: int, text_values3: dict,
                                 start_height_position):
    """
    to put values into label string by string with auto-stretching
    """
    for i, k in text_values3.items():
        print(i, k)
    print(len(text_values3.items()))
    for (key, value), i in zip(text_values3.items(), range(len(text_values3.items()))):

        # auto-stretching by finding right font_size depending of width text-string
        current_font_size = font_size
        key_width = stringWidth(key, 'bold', font_size_default, encoding='utf8')

        while stringWidth(value, 'bold', current_font_size, encoding='utf8') > (width_page - key_width):
            current_font_size -= 0.01

        x_key = space_horizontal_default
        x_value = key_width + space_horizontal_default + 1
        y_key = y_value = start_height_position - font_size - font_size * i - space_vertical
        c.setFont('bold', font_size_default)
        c.drawString(x_key, y_key, key)
        c.setFont('bold', current_font_size)
        c.drawString(x_value, y_value, value)
    return None


def createBarCodes():
    """
    Create barcode examples and embed in a PDF
    """
    text_values = ['ELENA CHEZELLE',
                   'Свадебное платье']

    text_values2 = ['NP100062LX-142C']

    text_values3 = {'Арт.:': 'Светло-бежевый',
                    'Разм.': '40'}

    y = generate_text_strings_top(height_page, font_size, space_vertical_default, text_values)
    y = generate_text_strings_middle(height_page, font_size, space_vertical_default, text_values2, y)
    generate_text_strings_bottom(height_page, font_size, space_vertical_default, text_values3, y)

    barcode_value = "1234567890"
    barcode_eanbc13 = eanbc.Ean13BarcodeWidget(barcode_value)
    barcode_eanbc13.fontSize = fontSize_barcode
    barcode_eanbc13.barHeight = barHeight_barcode
    barcode_eanbc13.barWidth = barWidth_barcode
    d = Drawing()
    d.add(barcode_eanbc13)
    renderPDF.draw(d, c, 0, bottom_indent)
    c.save()


if __name__ == '__main__':
    createBarCodes()
