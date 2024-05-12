# LIBRARIES FOR REGEX
import re

# LIBRARIES FOR ROOTS
from pathlib import Path
from decouple import config

# LIBRARIES FOR PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# DATE MODULE
from datetime import date

# LIBRARIES FOR SENDING EMAILS
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders

class Formulario():

    errors          = []
    reclamo_fecha   = str(date.today())
    reclamo_pdf     = None

    def __init__(self,id,reclamante_nombre,reclamante_domicilio,reclamante_tipo_documento,reclamante_numero_documento,reclamante_correo,reclamante_telefono_celular,reclamante_menor_edad,apoderado_nombre, apoderado_domicilio, apoderado_correo,apoderado_telefono_celular,bien_tipo,bien_monto,bien_descripcion,reclamo_tipo,reclamo_descripcion,reclamo_pedido) -> None:

        self.id                          = id 
        self.reclamante_nombre           = reclamante_nombre
        self.reclamante_domicilio        = reclamante_domicilio
        self.reclamante_tipo_documento   = reclamante_tipo_documento
        self.reclamante_numero_documento = reclamante_numero_documento
        self.reclamante_correo           = reclamante_correo
        self.reclamante_telefono_celular = reclamante_telefono_celular
        self.reclamante_menor_edad       = reclamante_menor_edad or "mayor"
        self.apoderado_nombre            = apoderado_nombre or ""
        self.apoderado_domicilio         = apoderado_domicilio or ""
        self.apoderado_correo            = apoderado_correo or ""
        self.apoderado_telefono_celular  = apoderado_telefono_celular or ""
        self.bien_tipo                   = bien_tipo
        self.bien_monto                  = bien_monto
        self.bien_descripcion            = bien_descripcion
        self.reclamo_tipo                = reclamo_tipo
        self.reclamo_descripcion         = reclamo_descripcion
        self.reclamo_pedido              = reclamo_pedido

    def __valid_claimant_name(self):
        
        # no number 
        lendata = len(re.findall("[0-9]",  self.reclamante_nombre)) 
        if lendata != 0 :

            self.errors.append("Numero en el nombre del reclamante")
            return False
        
        # no special characters
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:.]')
        if regex.search(self.reclamante_nombre) != None:

            self.errors.append("Caracter especial en el nombre del reclamante")
            return False
        
        return True

    def __valid_claimant_adress(self):

        # no special characters
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')            
        if regex.search(self.reclamante_domicilio) != None:

            self.errors.append("Caracter especial en el nombre del reclamante")
            return False
        
        return True
    
    def __valid_type_document(self):

        if self.reclamante_tipo_documento == "":

            self.errors.append("Tipo de documento no seleccionado")
            return False

        return True

    def __valid_claimant_document(self):

        # length
        lendata = len(self.reclamante_numero_documento)

        # dni
        if lendata == 8:

            # no letter 
            lendata = len(re.findall("[a-z]",  self.reclamante_numero_documento)) #[...]
            if lendata != 0 :

                self.errors.append("Letra en el DNI")
                return False
            
        # no special characters
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:.]')
        if regex.search(self.reclamante_numero_documento) != None:

            self.errors.append("Caracter especial en el nombre del reclamante")
            return False
        
        return True

    def __valid_claimant_number(self):

        # no decimal format
        if "." in self.reclamante_telefono_celular:

            self.errors.append("Punto decimal en Número de celular")
            return False
        
        return True

    def __valid_father_name(self):

        # no number 
        lendata = len(re.findall("[0-9]", self.apoderado_nombre)) 
        if lendata != 0 :

            self.errors.append("Numero en el nombre del apoderado")
            return False
        
        # no special characters
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:.]')
        if regex.search(self.apoderado_nombre) != None:

            self.errors.append("Caracter especial en el nombre del reclamante")
            return False
        
        return True

    def __valid_father_adress(self):

        # no special characters
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if regex.search(self.apoderado_domicilio) != None:

            self.errors.append("Caracter especial en el nombre del domicilio") 
            return False
        
        return True
    
    def __valid_father_number(self):

        # no decimal format
        if "." in self.apoderado_telefono_celular:

            self.errors.append("Punto el el numero de telefono del apoderado")
            return False
        
        return True

    def __valid_money(self):

        if "." in self.bien_monto:

            place_point    = self.bien_monto.find(".")
            decimal_items  = len(self.bien_monto[place_point:]) - 1

            if decimal_items == 1 or decimal_items == 2:
                return True
            
        self.errors.append("Incorrecta cantidad de decimales")
        return False

    def apply_filters(self):
          
        if not self.__valid_claimant_name():
            return False
  
        if not self.__valid_claimant_adress():
            return False
          
        if not self.__valid_type_document():
            return False
  
        if not self.__valid_claimant_document():
            return False
  
        if not self.__valid_claimant_number():
            return False
        
        if self.reclamante_menor_edad == "menor":
 
            if not self.__valid_father_name():
                return False
 
            if not self.__valid_father_adress():
                return False
 
            if not self.__valid_father_number():
                return False
  
        if  not self.__valid_money():
            return False 

        return True

    def __divide_long_text(self, text):

        """DIVIDING LONS STRING TO FIT IN A4 FORMAT"""

        len_text    = len(text)
        lines       = []
        
        if len_text < 90 :

            lines.append(text)
        
        elif len_text < 180 :

            lines.append(text[0:90])
            lines.append(text[90:180])

        else :

            lines.append(text[0:90])
            lines.append(text[90:180]) 
            lines.append(text[180:])

        return lines

    def __create_text_object(self, canvas,text,x,y, fontsize):

        """TEXT OBJECT FOR LONG TEXTS"""

        canvas.setFontSize(fontsize)
        text_object = canvas.beginText(x,y)
        lines       = self.__divide_long_text(text)
        for line in lines:
            text_object.textLine(line)

        return text_object

    def create_pdf(self):

        """CREATING PDF (DATA - FORMAT)"""

        try:

            # GENERAL VARIABLES
            file_name           = f"reclamo_virtual_{self.id}.pdf"
            file_format         = "A4"
            file_title          = f"Reclamo N°{self.id}"
            file_restaurante    = "Nombre del Restaurante"
            file_ruc            = f"RUC - 12345678900"
            message_one         = '- Estimado usuario, Su solicitud está en conocimiento de las autoridades,  la cual se está analizando para emitir una respuesta y posible solución en un plazo máximo de 15 días.'
            message_two         = '- Conforme a lo establedico en el Código de Protección y Defensa del Consumidor este       establecimiento cuenta con un Libro de Reclamaciones a tu disposición.'
            file_number         = f"HOJA DE RECLAMACIÓN - N°{self.id}"
            section             = [
                'Del Reclamante',
                'Del Apoderado',
                'Del Bien',
                'Del Reclamo',
            ]
            base_dir            = Path(__file__).resolve().parent.parent

            # PDF ::::::: VARIABLES FOR SIZE
            width, height = A4
            y       = 0
            y_middle= height // 2
            y_end   = round(height)
            x       = 0
            x_middle= width // 2
            x_end   = round(width)
            tab_one = 20
            tab_two = 30
            

            # PDF ::::::: CREATING
            pdf = canvas.Canvas(
                filename=f"{base_dir}/media/reclamos/{file_name}",
                pagesize=file_format
            )

            # PDF ::::::: TITLE
            pdf.setTitle(file_title)

            # HEADER ::::: NOMBRE + RUC
            pdf.setFontSize(20)
            pdf.drawString(tab_one,y_end-80,file_restaurante)
            pdf.setFontSize(15)
            pdf.drawString(tab_one,y_end-100,file_ruc)

            # HEADER :::::: MESSAGE 1
            text = self.__create_text_object(pdf,message_one,tab_one,y_end-140,11)
            pdf.drawText(text)

            # HEADER :::::: MESSAGE 2
            text = self.__create_text_object(pdf,message_two,tab_one,y_end-170,11)
            pdf.drawText(text)

            # HEADER :::::: NUMBER OF CLAIMANT
            pdf.rect(tab_one, y_end-240, x_middle-15,30)
            pdf.setFontSize(15)
            pdf.drawString(tab_two, y_end-230, file_number)

            # BODY :::::::: USER 
            pdf.setFontSize(13)
            pdf.drawString(tab_one,y_middle+150,section[0])
            pdf.line(tab_one, y_middle+145, x_middle, y_middle+145)
            pdf.setFontSize(11)
            pdf.drawString(tab_two,y_middle+130,f'- Nombre : {self.reclamante_nombre}')
            pdf.drawString(tab_two,y_middle+115,f'- Domicilio : {self.reclamante_domicilio}')
            pdf.drawString(tab_two,y_middle+100,f'- Tipo Documento : {self.reclamante_tipo_documento}')
            pdf.drawString(tab_two,y_middle+85,f'- Numero Documento : {self.reclamante_numero_documento}')
            pdf.drawString(tab_two,y_middle+70,f'- Correo : {self.reclamante_correo}')
            pdf.drawString(tab_two,y_middle+55,f'- Telefono / Celular : {self.reclamante_telefono_celular}')
            pdf.drawString(tab_two,y_middle+40,f'- Edad : {self.reclamante_menor_edad}')

            # BODY :::::::: FATHER
            pdf.setFontSize(13)
            pdf.drawString(tab_one,y_middle+15,section[1])
            pdf.line(tab_one, y_middle+10, x_middle, y_middle+10)
            pdf.setFontSize(11)
            pdf.drawString(tab_two,y_middle-5,f'- Nombre : {self.apoderado_nombre}')
            pdf.drawString(tab_two,y_middle-20,f'- Domicilio : {self.apoderado_domicilio}')
            pdf.drawString(tab_two,y_middle-35,f'- Correo : {self.apoderado_correo}')
            pdf.drawString(tab_two,y_middle-50,f'- Telefono : {self.apoderado_telefono_celular}')

            # BODY :::::::: ITEM
            pdf.setFontSize(13)
            pdf.drawString(tab_one,y_middle-75,section[2])
            pdf.line(tab_one, y_middle-80, x_middle+15, y_middle-80)
            pdf.setFontSize(11)
            pdf.drawString(tab_two,y_middle-95,f'- Tipo : {self.bien_tipo}')
            pdf.drawString(tab_two,y_middle-110,f'- Monto : {self.bien_monto}')
            pdf.drawString(tab_two,y_middle-125,f'- Descripción : ')
            text = self.__create_text_object(pdf,self.bien_descripcion,x+105,y_middle-125,11)
            pdf.drawText(text) 

            # BODY :::::: COMPLAIMANT
            pdf.setFontSize(13)
            pdf.drawString(tab_one,y_middle-175,section[3])
            pdf.line(tab_one, y_middle-180, x_middle+15, y_middle-180)
            pdf.setFontSize(11)
            pdf.drawString(tab_two,y_middle-195,f'- Tipo : {self.reclamo_tipo}')
            pdf.drawString(tab_two,y_middle-210,f'- Descripcion : ')
            text = self.__create_text_object(pdf,self.reclamo_descripcion,x+105,y_middle-210,11)
            pdf.drawText(text) 
            pdf.drawString(tab_two,y_middle-255,f'- Pedido : ')
            text = self.__create_text_object(pdf,self.reclamo_pedido,x+80,y_middle-255,11)
            pdf.drawText(text) 

            # FOOTER :::: DATE
            pdf.setFontSize(11)
            pdf.drawString(tab_one,y+10,self.reclamo_fecha)

            # PDF :::::: SAVING
            self.reclamo_pdf = f"{base_dir}/media/reclamos/{file_name}"
            pdf.save()

            return True

        except:

            self.errors.append("No se pudo crear el documento de reclamación")
            return False  

    def send_email(self):

        try:

            # path of the file
            base_dir            = Path(__file__).resolve().parent.parent
            
            # variables for work
            email_sender    = config("email_sender")
            email_password  = config("email_password")
            email_receiver  = [self.reclamante_correo]
            if self.apoderado_correo != None: email_receiver.append(self.apoderado_correo)
            subject         = "Reporte Reclamo"
            body            = "Estimado Usuario, procedemos a generarle una copia de su reclamo"

            # Create the container email message.
            msg             = EmailMessage()
            msg['From']     = email_sender
            msg['To']       = email_receiver
            msg['Subject']  = subject
            msg.set_content(body)

            # Make the message multipart
            msg.add_alternative(body, subtype='html')

            # Attach the image file
            with open(f"{base_dir}/media/reclamos/reclamo_virtual_{self.id}.pdf", 'rb') as attachment_file:
                file_data = attachment_file.read()
                file_name = attachment_file.name.split("/")[-1]

            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file_data)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
            msg.attach(attachment)

            # add SSL (layer of security)
            context = ssl.create_default_context()

            # send email
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as s:
                s.login(email_sender,email_password)
                s.sendmail(email_sender,email_receiver,msg.as_string())

            return True

        except:

            self.errors = "No se pudo generar el email para usuario"
            return False

if __name__ == "__main__":

    queja = Formulario(
        id="50",
        reclamante_nombre = "Jose",
        reclamante_domicilio = "mi super casa 123",
        reclamante_tipo_documento = "dni",
        reclamante_numero_documento = "12345678",
        reclamante_correo  = "micorreo@correo.com",
        reclamante_telefono_celular = "123456789",
        reclamante_menor_edad = "menor",
        apoderado_nombre = "David",
        apoderado_domicilio = "la misma casa 123",
        apoderado_correo = "backendpath@gmail.com",
        apoderado_telefono_celular = "987654321",
        bien_tipo = "bien",
        bien_monto = "40.3",
        bien_descripcion = "consectetur adipiscing elit. Donec elit risus, tristi12312333",
        reclamo_tipo ="queja",
        reclamo_descripcion="Donec elit risus, tristi12312333Lorem ipsum dolor sit amet, tristi12312333Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec elit risus, tristi12312333",
        reclamo_pedido="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec elit risus, tristi12312333Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec elit risus, tristi12312333Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec elit risus, tristi12312333",   
    )

    print(queja)
    print(queja.apply_filters())
    queja.create_pdf()
    # queja.send_email()
