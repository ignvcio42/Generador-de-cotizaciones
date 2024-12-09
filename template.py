from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from datetime import datetime



def generar_pdf(file_path="cotizacion.pdf"):
    # Datos de ejemplo (puedes modificarlos para probar)
    folio = "2875"
    atencion = "Priscila Meza"
    empresa = "Corporación Belén Educa"
    fecha_evento = "29 de Noviembre"
    fecha_montaje = "28 de Noviembre"
    fecha_desarme = "02 de Dic"
    lugar_evento = "Colegio Quilicura"
    neto = "450.000"
    iva = "85.500"
    bruto = "535.500"
    fecha_actual = datetime.now().strftime("%d / %m / %Y")
    forma_de_pago = "Efectivo"
    
    # Datos dinámicos
    tabla_datos = [
        ["Carpa", "13", "4", "52", "450.000"],  # Puedes agregar más filas aquí
        ["Carpa", "13", "4", "52", "450.000"]  # Puedes agregar más filas aquí
    ]
    descripcion_datos = [
        "Estructura Metálica (4 Mts altura desde el piso)",
        "Cierre Blanco",
        "Cortina Fondo",
        "Decoración color Rojo",
        "Cubrepilares"
    ]

    # Crear el PDF
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Times-Roman", 20)

    # Encabezado
    c.drawString(70, 750, "CARPAS GUAJARDO PROD. SPA")
    c.setFont("Times-Roman", 11)
    c.drawString(70, 735, "Rut: 77.011.105-6")
    c.drawString(70, 720, "Isla Decelt N8974")
    c.drawString(70, 705, "Pudahuel")
    c.drawString(70, 690, "Fono: 22749 98 14")

    # Fecha y Folio
    c.drawString(460, 690, f"FECHA: {fecha_actual}")
    c.drawString(460, 675, f"FOLIO : N° {self.formatear_dinero(folio)}")

    # Título
    c.setFont("Times-Roman", 18)
    c.drawString(250, 650, "COTIZACIÓN")
    c.setLineWidth(0.3)
    c.line(250, 645, 360, 645)  # Subrayar el título

    # Información del cliente
    c.setFont("Times-Roman", 12)
    c.drawString(70, 630, "CLIENTE:")
    c.line(70, 628, 125, 628)  # Subrayar la palabra CLIENTE
    c.drawString(70, 615, "ATENCION:")
    c.setFont("Times-Roman", 12)
    c.drawString(170, 615, atencion)
    c.line(170, 613, 360, 613)  # Subrayar la palabra ATENCION
    c.drawString(70, 600, "EMPRESA:")
    c.drawString(170, 600, empresa)
    c.line(170, 598, 360, 598)  # Subrayar la palabra EMPRESA
    
    # Título de la tabla
    c.setFont("Times-Bold", 12)
    c.drawString(70, 570, "CUADRO DETALLE ARRIENDO CARPA ESCENARIO:")
    c.line(70, 568, 370, 568)  # Subrayar el título
    
    # Formatear los totales con el símbolo de dinero
    formatted_tabla_datos = [(detalle, largo, alto, total_mts, f"${self.formatear_dinero(total)}") for detalle, largo, alto, total_mts, total in self.tabla_datos]

    # Tabla de detalles
    table_data = [["Detalle", "Largo", "Alto", "Total Mts", "Total"]] + formatted_tabla_datos + [
        ["Total Neto", "", "", "", neto],
        ["IVA", "", "", "", iva],
        ["Total Bruto", "", "", "", bruto]
]

    # Crear la tabla con los datos
    table = Table(table_data, colWidths=[70, 40, 40, 50, 70])

    # Configuración del estilo de la tabla
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),        # Líneas de la tabla
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),              # Alinear los números a la derecha
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),            # Centrar verticalmente dentro de las celdas
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),       # Fuente en negrita para el encabezado
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),     # Fuente normal para los datos
        ('FONTNAME', (0, -3), (-1, -1), 'Times-Bold'),     # Fuente en negrita para Neto, IVA y Bruto
        ('SPAN', (0, -3), (-2, -3)),                       # Combinar celdas de Neto
        ('SPAN', (0, -2), (-2, -2)),                       # Combinar celdas de IVA
        ('SPAN', (0, -1), (-2, -1)),                       # Combinar celdas de Bruto
        ('ALIGN', (0, -3), (0, -1), 'LEFT'),               # Alinear títulos Neto, IVA, Bruto a la izquierda
        ('ALIGN', (-1, -3), (-1, -1), 'RIGHT')             # Mantener los valores del Total a la derecha
    ]))

    # Altura estimada de la tabla
    table_height = 15 * len(table_data)  # Estimar altura (15 unidades por fila)

    # Ajustar posición y dibujar la tabla en el lienzo
    table.wrapOn(c, 70, 550 - table_height - 20)  # Ajustar posición
    table.drawOn(c, 70, 550 - table_height - 20)  # Dibujar la tabla

    # Descripción de la carpa
    y = 550 - table_height - 40  # Adjust y position based on table height with additional margin
    c.setFont("Times-Bold", 12)
    c.drawString(70, y, "Descripción Carpa:")
    c.setFont("Times-Roman", 12)
    y -= 15
    for descripcion in self.descripcion_datos:
        c.drawString(80, y, f"• {descripcion}")
        y -= 15

    # Adjust the y position for the following sections based on the number of descriptions
    y -= 5

    # Fechas y lugar
    c.setFont("Times-Roman", 12)
    c.drawString(70, y - 10, "Fecha Evento:")
    c.drawString(170, y - 10, fecha_evento)
    c.drawString(70, y - 25, "Fecha Montaje:")
    c.drawString(170, y - 25, fecha_montaje)
    c.drawString(70, y - 40, "Fecha Desarme:")
    c.drawString(170, y - 40, fecha_desarme)
    c.drawString(70, y - 55, "Lugar Evento:")
    c.drawString(170, y - 55, lugar_evento)
    c.drawString(70, y - 70, "Forma de Pago:")
    c.drawString(170, y - 70, forma_pago)

    # Título de la tabla
    c.setFont("Times-Roman", 12)

    # Título de la tabla de fechas y lugar
    c.drawString(70, y - 90, "Esperando que este servicio sea de su interés, le saluda atentamente,")
    
    # Firma y pie de página
    firma_y = 150
    pie_y = 50

    if y - 80 < firma_y + 20:  # Check if there's enough space for the signature and footer
        c.showPage()  # Create a new page
        y = 750  # Reset y position for the new page

    # Firma
    c.setFont("Times-Roman", 12)
    c.drawCentredString(300, firma_y, "Ariel Guajardo V.")
    c.line(255, firma_y - 2, 343, firma_y - 2)  # Subrayar el nombre
    c.setFont("Times-Italic", 12)
    c.drawCentredString(300, firma_y - 15, "Carpas Guajardo Prod. Spa")
    c.drawCentredString(300, firma_y - 30, "Fono: +56963436322 - +56945121257")

    # Pie de página
    c.setFont("Times-Roman", 10)
    c.drawCentredString(300, pie_y, "Carpas Guajardo")
    c.drawCentredString(300, pie_y - 15, "Fono: +56945121257 - Cel. +56963436322")

    c.save()
    print(f"PDF generado correctamente en {file_path}")

# Llama a la función para generar el PDF
if __name__ == "__main__":
    generar_pdf("cotizacion_prueba.pdf")

    def formatear_dinero(self, valor):
        return "{:,}".format(int(valor)).replace(",", ".")
