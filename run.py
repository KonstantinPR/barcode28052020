import os
from reportlab.pdfbase import ttfonts
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.graphics.barcode import eanbc
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
import pandas as pd

current_dir = os.path.dirname(os.path.realpath(__file__))

# fonts
fonts_dir = os.path.join(current_dir, 'fonts')
regular = ttfonts.TTFont('bold', os.path.join(fonts_dir, 'OpenSans-Bold.ttf'))
bold = ttfonts.TTFont('regular', os.path.join(fonts_dir, 'OpenSans-Regular.ttf'))
registerFont(regular), registerFont(bold)

# setting canvas and constants

width_canvas = 50
height_canvas = 70
width_page = width_canvas * 0.98
height_page = height_canvas * 0.99
indent_percent_horizontal = 5
indent_percent_vertical = 10
left_indent = width_page * indent_percent_horizontal / 100
right_indent = width_page * indent_percent_horizontal / 100
top_indent = height_page * indent_percent_vertical / 100
bottom_indent = height_page * indent_percent_vertical / 100
space_vertical_default = 5
space_horizontal_default = 2
font_size = 6
font_size_default = 2
fontSize_barcode = 3
barHeight_barcode = 10
barWidth_barcode = 0.45

header_info = ["Торговая марка", "Вид"]
middle_art = ["Арт.:"]
middle_info = ["Цвет:", "Разм:"]
barcode_info = ["Штрихкод"]


def createBarCodes():
    """
    Create barcode examples and embed in a PDF
    """

    len_row_table, header_info_values, middle_art_values, middle_info_values, barcode_info_values = \
        loading_table('E:/python/env/barcode28052020/example.xlsx',
                      header_info,
                      middle_art,
                      middle_info,
                      barcode_info)

    print(middle_info_values)

    for i in range(len_row_table):
        c = canvas.Canvas(f"barcodes{i}.pdf")
        c.setPageSize((width_canvas, height_canvas))
        c.setFont('bold', font_size)

        header_info_values = header_info_values
        middle_art_values = middle_art_values
        middle_info_values = middle_info_values


        y, c = generate_text_strings_top(height_page, font_size, space_vertical_default, header_info_values[i], c)
        y, c = generate_text_strings_middle(height_page, font_size, space_vertical_default, middle_art_values[i], y, c)
        c = generate_text_strings_bottom(height_page, font_size, space_vertical_default, middle_info_values[i], y, c)
        barcode_value = barcode_info_values[i][0]
        print(barcode_info_values[i][0])
        barcode_eanbc13 = eanbc.Ean13BarcodeWidget(barcode_value)
        barcode_eanbc13.fontSize = fontSize_barcode
        barcode_eanbc13.barHeight = barHeight_barcode
        barcode_eanbc13.barWidth = barWidth_barcode
        d = Drawing()
        d.add(barcode_eanbc13)
        renderPDF.draw(d, c, 0, bottom_indent)

        c.save()


def loading_table(path, header_info: list, middle_art: list, middle_info: list, barcode_info: list):
    df = pd.read_excel(path)
    len_row_table = len(df.index)
    header_info_values = df[header_info].values.tolist()
    middle_art_values = df[middle_art].values.tolist()
    middle_info_values_list = df[middle_info].values.tolist()
    middle_info_values = []
    for i in range(len_row_table):
        middle_info_values.append(dict(zip(middle_info, middle_info_values_list[i])))
    barcode_info_values = df[barcode_info].values.tolist()
    return len_row_table, header_info_values, middle_art_values, middle_info_values, barcode_info_values


def generate_text_strings_top(height_page: float, font_size: int, space_vertical: int, text_values: list, c):
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
    return y, c


def generate_text_strings_middle(height_page: float, font_size: int, space_vertical: int, text_values2: list,
                                 start_height_position, c):
    """
    to put values into label string by string with auto-stretching
    """
    for text, i in zip(text_values2, range(len(text_values2))):
        # auto-stretching by finding right font_size depending of width text-string
        current_font_size = font_size
        while stringWidth(text, 'bold', current_font_size, encoding='utf8') > width_page - left_indent:
            current_font_size -= 0.1
        string_width = stringWidth(text, 'bold', current_font_size, encoding='utf8')
        x = (width_page - string_width) / 2
        y = start_height_position - font_size * i - font_size - space_vertical
        c.setFont('regular', current_font_size)
        c.drawString(x, y, text)
    return y, c


def generate_text_strings_bottom(height_page: float, font_size: int, space_vertical: int, text_values3: dict,
                                 start_height_position, c):
    """
    to put values into label string by string with auto-stretching
    """
    for (key, value), i in zip(text_values3.items(), range(len(text_values3.items()))):
        key, value = str(key), str(value)

        # auto-stretching by finding right font_size depending of width text-string
        current_font_size = font_size
        if i == 0:
            key_width = stringWidth(key, 'bold', font_size_default, encoding='utf8')
        while stringWidth(value, 'bold', current_font_size, encoding='utf8') > \
                (width_page - key_width - left_indent * 2):
            current_font_size -= 0.1

        x_key = space_horizontal_default
        x_value = key_width + space_horizontal_default + 1
        y_key = y_value = start_height_position - font_size - font_size * i - space_vertical
        c.setFont('regular', font_size_default)
        c.drawString(x_key, y_key, key)
        c.setFont('bold', current_font_size)
        c.drawString(x_value, y_value, value)
    return c


if __name__ == '__main__':
    createBarCodes()
