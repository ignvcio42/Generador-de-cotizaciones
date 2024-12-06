import os
import tkinter as tk
from tkinter import Tk, Label, messagebox, Entry, Button, Text, END, filedialog, Frame, Scrollbar, Listbox, MULTIPLE, ttk, PhotoImage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from reportlab.platypus import Table, TableStyle
import base64
from PIL import Image
from io import BytesIO

class CotizacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Cotizaciones Carpas Guajardo")

        self.descripciones_predefinidas = [
        "Estructura Metálica (3 mts altura parejo)",
        "Estructura Metálica (4 mts altura parejo)",
        "Techo Blanco",
        "Techo negro",
        "Cubre pilares color blanco",
        "Iluminación LED decorativa",
        "Montaje y Desmontaje",
        "Iluminacion basica",
        "Cubrepiso"
    ]


        # Configure root window to be responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)

        # Center the window on screen
        self.center_window(1000, 900)  # Adjust width and height as needed

        # Use ttk for a more modern look
        style = ttk.Style()
        style.configure('TLabel', padding=5)
        style.configure('TEntry', padding=5)

        # Variables
        self.folio = ttk.Entry(root)
        self.atencion = ttk.Entry(root)
        self.empresa = ttk.Entry(root)
        self.tabla_datos = []
        self.descripcion_datos = []

        # Nuevas variables para fechas y lugar
        self.fecha_evento = ttk.Entry(root)
        self.fecha_montaje = ttk.Entry(root)
        self.fecha_desarme = ttk.Entry(root)
        self.lugar_evento = ttk.Entry(root)
        self.forma_pago = ttk.Entry(root)

        # Layout with improved spacing and alignment
        row = 0
        ttk.Label(root, text="Folio:").grid(row=row, column=0, sticky="e", padx=10, pady=5)
        self.folio.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

        ttk.Label(root, text="Atención:").grid(row=row, column=0, sticky="e", padx=10, pady=5)
        self.atencion.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

        ttk.Label(root, text="Empresa:").grid(row=row, column=0, sticky="e", padx=10, pady=5)
        self.empresa.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

        # Tabla de Detalles
        ttk.Label(root, text="Detalles:").grid(row=row, column=0, sticky="ne", padx=10, pady=5)
        self.tabla_frame = ttk.Frame(root)
        self.tabla_frame.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        

        # Encabezados para los campos
        headers = ["Detalle", "Largo", "Alto", "Total Mts", "Valor M2", "Total"]
        for i, header in enumerate(headers):
            ttk.Label(self.tabla_frame, text=header, anchor="center").grid(row=0, column=i, sticky="ew")

        # Campos de entrada para los detalles
        self.detalle_entry = Entry(self.tabla_frame, width=15)
        self.detalle_entry.grid(row=1, column=0)
        self.largo_entry = Entry(self.tabla_frame, width=5)
        self.largo_entry.grid(row=1, column=1)
        self.alto_entry = Entry(self.tabla_frame, width=5)
        self.alto_entry.grid(row=1, column=2)
        self.total_mts_entry = Entry(self.tabla_frame, width=10)
        self.total_mts_entry.grid(row=1, column=3)
        self.valor_m2_entry = Entry(self.tabla_frame, width=10)  # New entry
        self.valor_m2_entry.grid(row=1, column=4)
        self.total_entry = Entry(self.tabla_frame, width=10)
        self.total_entry.grid(row=1, column=5)

        # Añadir evento para calcular automáticamente el total de metros cuadrados
        self.largo_entry.bind("<KeyRelease>", self.calcular_total_mts)  # Changed back to original method name
        self.alto_entry.bind("<KeyRelease>", self.calcular_total_mts)
        self.valor_m2_entry.bind("<KeyRelease>", self.calcular_total_mts)

        # Botón Añadir con estilo
        ttk.Button(self.tabla_frame, text="Añadir", command=self.agregar_detalle).grid(row=2, column=0, columnspan=6, sticky="ew", padx=10, pady=5)

        # Listbox para mostrar detalles
        self.tabla_listbox = Listbox(self.tabla_frame, width=80, height=5)
        self.tabla_listbox.grid(row=3, column=0, columnspan=6, sticky="ew", padx=10, pady=5)

         # Resto de los campos (Neto, IVA, Bruto)
        row += 1
        neto_labels = ["Neto:", "IVA:", "Bruto:"]
        self.neto = ttk.Entry(root)
        self.iva = ttk.Entry(root)
        self.bruto = ttk.Entry(root)
        
        for i, (label_text, entry) in enumerate(zip(neto_labels, [self.neto, self.iva, self.bruto])):
            ttk.Label(root, text=label_text).grid(row=row+i, column=0, sticky="e", padx=10, pady=5)
            entry.grid(row=row+i, column=1, sticky="ew", padx=10, pady=5)

       # Descripción de la carpa
        Label(root, text="").grid(row=9, column=0, sticky="ne")
        self.descripcion_frame = Frame(root)
        self.descripcion_frame.grid(row=7, column=1, sticky="w")

        # Encabezados
        headers = ["Descripción"]
        for i, header in enumerate(headers):
            ttk.Label(self.descripcion_frame, text=header, anchor="center").grid(row=0, column=i, sticky="ew")

        # Campo de entrada para la descripción
        self.descripcion_entry = Entry(self.descripcion_frame, width=50)
        self.descripcion_entry.grid(row=1, column=0)

        # Botón Añadir con estilo
        ttk.Button(self.descripcion_frame, text="Añadir", command=self.agregar_descripcion).grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Listbox para mostrar descripciones
        self.descripcion_listbox = Listbox(self.descripcion_frame, width=60, height=5)
        self.descripcion_listbox.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # Etiqueta para el Combobox de descripciones predefinidas
        ttk.Label(self.descripcion_frame, text="Selecciona descripción predefinida:").grid(row=0, column=1, padx=5, pady=5)

        # Combobox para descripciones predefinidas
        self.descripcion_combobox = ttk.Combobox(self.descripcion_frame, values=self.descripciones_predefinidas, width=50)
        self.descripcion_combobox.grid(row=1, column=1, padx=5)

        # Botón para añadir la descripción seleccionada del Combobox
        ttk.Button(self.descripcion_frame, text="Añadir Predefinida", command=self.agregar_descripcion_predefinida).grid(row=2, column=1, sticky="ew", padx=10, pady=5)


        # Fechas y lugar del evento
        row = 8  # Comenzamos desde la fila 8 para mantener la continuidad

        ttk.Label(root, text="Fecha Evento:").grid(row=row, column=0, sticky="e", padx=10, pady=5)
        self.fecha_evento.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

        ttk.Label(root, text="Fecha Montaje:").grid(row=row, column=0, sticky="e", padx=10, pady=5)
        self.fecha_montaje.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

        ttk.Label(root, text="Fecha Desarme:").grid(row=row, column=0, sticky="e", padx=10, pady=5)
        self.fecha_desarme.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

        ttk.Label(root, text="Lugar Evento:").grid(row=row, column=0, sticky="e", padx=10, pady=5)
        self.lugar_evento.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

        ttk.Label(root, text="Forma de pago:").grid(row=row, column=0, sticky="e", padx=10, pady=5)
        self.forma_pago.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

       # Frame para los botones de acción
        self.botones_frame = Frame(root)
        self.botones_frame.grid(row=13, column=0, columnspan=2, pady=10)

        # Botón para generar PDF
        Button(self.botones_frame, text="Generar PDF", command=self.generar_pdf).grid(row=0, column=0, padx=10)

        # Botón para limpiar datos
        Button(self.botones_frame, text="Limpiar Datos", command=self.limpiar_datos).grid(row=0, column=1, padx=10)

    def agregar_descripcion_predefinida(self):
        descripcion = self.descripcion_combobox.get()
        if descripcion:
            self.descripcion_datos.append(descripcion)
            self.descripcion_listbox.insert(END, descripcion)
            self.descripcion_combobox.set("")  # Limpiar selección después de añadir

    
    def center_window(self, width, height):
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def calcular_total_mts(self, event=None):
        try:
            largo = float(self.largo_entry.get() or 0)
            alto = float(self.alto_entry.get() or 0)
            valor_m2 = float(self.valor_m2_entry.get() or 0)
            
            total_mts = largo * alto
            self.total_mts_entry.delete(0, END)
            self.total_mts_entry.insert(0, str(total_mts))
            
            total = total_mts * valor_m2
            self.total_entry.delete(0, END)
            self.total_entry.insert(0, str(int(total)))
        except ValueError:
            self.total_mts_entry.delete(0, END)
            self.total_entry.delete(0, END)

    def agregar_detalle(self):
        detalle = self.detalle_entry.get()
        largo = self.largo_entry.get()
        alto = self.alto_entry.get()
        total_mts = self.total_mts_entry.get()
        valor_m2 = self.valor_m2_entry.get()
        total = self.total_entry.get()

        if detalle and largo and alto and total_mts and valor_m2 and total:
            self.tabla_datos.append((detalle, largo, alto, total_mts, valor_m2, total))
            self.tabla_listbox.insert(END, f"{detalle} - {largo}x{alto}, {total_mts} mts, Valor M2: ${self.formatear_dinero(valor_m2)}, Total: ${self.formatear_dinero(total)}")

            self.detalle_entry.delete(0, END)
            self.largo_entry.delete(0, END)
            self.alto_entry.delete(0, END)
            self.total_mts_entry.delete(0, END)
            self.valor_m2_entry.delete(0, END)
            self.total_entry.delete(0, END)

            self.calcular_totales()

    def calcular_totales(self):
        # Calcular el total neto sumando todos los totales de los detalles
        neto = sum(int(total.replace('.', '')) for _, _, _, _, _, total in self.tabla_datos)
        
        # Calcular el IVA como 19% del total neto
        iva = int(neto * 0.19)
        
        # Calcular el total bruto sumando neto e IVA
        bruto = neto + iva

        # Limpiar y mostrar los campos de neto, IVA y bruto
        self.neto.delete(0, END)
        self.neto.insert(0, f"${self.formatear_dinero(neto)}")

        self.iva.delete(0, END)
        self.iva.insert(0, f"${self.formatear_dinero(iva)}")

        self.bruto.delete(0, END)
        self.bruto.insert(0, f"${self.formatear_dinero(bruto)}")

    def agregar_descripcion(self):
        descripcion = self.descripcion_entry.get()
        if descripcion:
            self.descripcion_datos.append(descripcion)
            self.descripcion_listbox.insert(END, descripcion)
            self.descripcion_entry.delete(0, END)

    def formatear_dinero(self, valor):
        return "{:,}".format(int(valor)).replace(",", ".")
    
    # Limpia todos los campos y listas de la aplicación.
    def limpiar_datos(self):
       
        # Limpiar campos de entrada
        self.folio.delete(0, END)
        self.atencion.delete(0, END)
        self.empresa.delete(0, END)
        self.detalle_entry.delete(0, END)
        self.largo_entry.delete(0, END)
        self.alto_entry.delete(0, END)
        self.total_mts_entry.delete(0, END)
        self.total_entry.delete(0, END)
        self.neto.delete(0, END)
        self.iva.delete(0, END)
        self.bruto.delete(0, END)
        self.fecha_evento.delete(0, END)
        self.fecha_montaje.delete(0, END)
        self.fecha_desarme.delete(0, END)
        self.lugar_evento.delete(0, END)
        self.forma_pago.delete(0, END)

        # Limpiar listas
        self.tabla_datos.clear()
        self.descripcion_datos.clear()
        self.tabla_listbox.delete(0, END)
        self.descripcion_listbox.delete(0, END)

    def generar_pdf(self):
        
        # Validar que el folio esté completo
        folio = self.folio.get()
        if not folio.strip():  # Verifica si está vacío o contiene solo espacios
            messagebox.showerror("Error", "No se puede generar el PDF sin rellenar el folio.")
            return

        # Obtener datos del formulario
        folio = self.folio.get()
        atencion = self.atencion.get()
        empresa = self.empresa.get()
        neto = self.neto.get()
        iva = self.iva.get()
        bruto = self.bruto.get()
        fecha_evento = self.fecha_evento.get()
        fecha_montaje = self.fecha_montaje.get()
        fecha_desarme = self.fecha_desarme.get()
        lugar_evento = self.lugar_evento.get()
        forma_pago = self.forma_pago.get()
        fecha_actual = datetime.now().strftime("%d / %m / %Y")

        # Seleccionar ubicación para guardar el PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        # Crear el PDF
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Times-Roman", 20)

        # Encabezado
        c.drawString(70, 750, "CARPAS GUAJARDO PROD. SPA")
        c.setFont("Times-Roman", 11)
        c.drawString(70, 735, "Rut: 77.011.105-6")
        c.drawString(70, 720, "Isla Decelt N°8774")
        c.drawString(70, 705, "Pudahuel")
        c.drawString(70, 690, "cel: +569 45121257")

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
        formatted_tabla_datos = [(detalle, largo, alto, total_mts, f"${self.formatear_dinero(valor_m2)}", f"${self.formatear_dinero(total)}") 
                                  for detalle, largo, alto, total_mts, valor_m2, total in self.tabla_datos]

        # Tabla de detalles
        table_data = [["Detalle", "Largo", "Alto", "Total Mts", "Valor M2", "Total"]] + formatted_tabla_datos + [
            ["Total Neto", "", "", "", "", neto],
            ["IVA", "", "", "", "", iva],
            ["Total Bruto", "", "", "", "", bruto]
        ]

        # Crear la tabla con los datos
        table = Table(table_data, colWidths=[70, 40, 40, 50, 50, 70])

        # Configuración del estilo de la tabla
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
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
        messagebox.showinfo("Cotización Generada", "La cotización se generó exitosamente.")

# Ejecutar la aplicación
if __name__ == "__main__":

    # Tu cadena base64 de la imagen (pon aquí tu base64)
    logo_base64 = '''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'''

    # Decodificar la cadena base64
    image_data = base64.b64decode(logo_base64)

    # Convertir los datos en una imagen
    image = Image.open(BytesIO(image_data))

    root = Tk()
    app = CotizacionApp(root)
    root.mainloop()
