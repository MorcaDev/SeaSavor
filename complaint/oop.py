# LIBRARIES FOR REGEX , MATH
import re
import math

# LIBRARIES FOR OOP
from abc import ABC, abstractmethod 

# LIBRARIES FOR ROOTS
from pathlib import Path
from decouple import config

# LIBRARIES FOR PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# LIBRARIES FOR SENDING EMAILS
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders

class Validations:

    errors = []

    def validation_no_none(self, attribute_name, attribute_value):

        if attribute_value is None:

            self.errors.append(f'{attribute_name} obligatorio')
            return False
        
        return True
    
    def validation_length_minmax(self, attribute_name, attribute_value, min, max):

        lendata = len(attribute_value)

        if lendata < min:

            self.errors.append(f'{attribute_name} muy corto')
            return False
        
        if lendata > max:

            self.errors.append(f'{attribute_name} muy largo')
            return False
        
        return True
    
    def validation_length_ab(self,attribute_name, attribute_value,a,b):

        lendata = len(attribute_value)
        if lendata == a or lendata == b:

            return True
        
        self.errors.append(f'{attribute_name} tiene una longitud no valida')
        return False

    def validation_no_number(self,attribute_name, attribute_value):

        lendata = len(re.findall("[0-9]",  attribute_value)) 
        if lendata != 0 :

            self.errors.append(f'{attribute_name} no puede contener numeros')
            return False
        
        return True

    def validation_no_letter(self,attribute_name, attribute_value):

        lendata = len(re.findall("[a-z]", attribute_value)) 
        if lendata != 0 :

            self.errors.append(f'{attribute_name} no admite letra(s)')
            return False
        
        return True

    def validation_no_special(self,attribute_name, attribute_value, extra = None):

        special_list = "@_!#$%^&*()<>?/\|}{~:" 

        if extra is not None :
            special_list += extra

        regex = re.compile(f'[{special_list}]')
        if regex.search(attribute_value) != None:

            self.errors.append(f'{attribute_name} contiene caracter(es) especial(es)')
            return False
        
        return True

    def validation_decimal_format(self,attribute_name, attribute_value):

        if not "." in attribute_value:
            return True    

        place_point    = self.bien_monto.find(".")
        decimal_items  = len(self.bien_monto[place_point:]) - 1

        if decimal_items == 1 or decimal_items == 2:
            return True
            
        self.errors.append(f'{attribute_name} tiene incorrecta cantidad de decimales')
        return False 

    def validation_list(self,attribute_name, attribute_value, list_values):

        for item in list_values:  
            if item == attribute_value:
                return True
            
        self.errors.append(f'{attribute_name} no coincide con los valores admitidos')
        return False

class Claimant(Validations):

    def __init__(self,reclamante_nombre,reclamante_domicilio,reclamante_tipo_documento,reclamante_numero_documento,reclamante_correo,reclamante_telefono_celular,reclamante_menor_edad) -> None:

        self.reclamante_nombre           = reclamante_nombre
        self.reclamante_domicilio        = reclamante_domicilio
        self.reclamante_tipo_documento   = reclamante_tipo_documento
        self.reclamante_numero_documento = reclamante_numero_documento
        self.reclamante_correo           = reclamante_correo
        self.reclamante_telefono_celular = reclamante_telefono_celular
        self.reclamante_menor_edad       = reclamante_menor_edad

    def __valid_claimant_name(self):
        
        attribute_name = "Nombre del Reclamante"
        attribute_value = self.reclamante_nombre

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False
        
        # length
        if not self.validation_length_minmax(attribute_name, attribute_value, 3,100): return False

        # no number 
        if not self.validation_no_number(attribute_name, attribute_value): return False
        
        # no special characters
        if not self.validation_no_special(attribute_name, attribute_value, "."): return False
         
        return True

    def __valid_claimant_adress(self):

        attribute_name = "Dirección del reclamante"
        attribute_value = self.reclamante_domicilio

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False
        
        # length
        if not self.validation_length_minmax(attribute_name, attribute_value, 10,255): return False
       
        # no special characters
        if not self.validation_no_special(attribute_name, attribute_value): return False
         
        return True

    def __valid_type_document(self):

        attribute_name = "Tipo de documento"
        attribute_value = self.reclamante_tipo_documento

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # valid types
        if not self.validation_list(attribute_name, attribute_value, ["dni","pasaporte"]): return False

        return True

    def __valid_claimant_document(self):

        attribute_name = "Documento del Reclamante"
        attribute_value = self.reclamante_numero_documento

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # correct length 
        if not self.validation_length_ab(attribute_name,attribute_value,8,12): return False
        
        # if it's dni
        if len(attribute_value) == 8:

            # no letters
            if not self.validation_no_letter(attribute_name, attribute_value): return False
            
        # no special characters
        if not self.validation_no_special(attribute_name, attribute_value, "."): return False
        
        return True

    def __valid_claimant_email(self):

        attribute_name = "Correo del Reclamante"
        attribute_value = self.reclamante_correo

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        return True

    def __valid_claimant_phone(self):

        attribute_name = "Celular del Reclamante"
        attribute_value = self.reclamante_telefono_celular

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # correct length
        if not self.validation_length_ab(attribute_name, attribute_value,7,9): return False

        # no letter
        if not self.validation_no_letter(attribute_name, attribute_value): return False

        # no special
        if not self.validation_no_special(attribute_name, attribute_value, "."): return False
        
        return True

    def __valid_claimant_age(self):

        attribute_name = "Edad del Reclamante"
        attribute_value = self.reclamante_menor_edad

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # list
        if not self.validation_list(attribute_name, attribute_value,["menor","mayor"]): return False
        
        return True

    def is_valid(self):

        if not self.__valid_claimant_name()     : return False
        if not self.__valid_claimant_adress()   : return False
        if not self.__valid_type_document()     : return False
        if not self.__valid_claimant_document() : return False
        if not self.__valid_claimant_email()    : return False
        if not self.__valid_claimant_phone()    : return False
        if not self.__valid_claimant_age()      : return False

        return True

class Father(Validations):

    def __init__(self,apoderado_nombre, apoderado_domicilio, apoderado_correo,apoderado_telefono_celular) -> None:

        self.apoderado_nombre            = apoderado_nombre 
        self.apoderado_domicilio         = apoderado_domicilio 
        self.apoderado_correo            = apoderado_correo 
        self.apoderado_telefono_celular  = apoderado_telefono_celular 
 
    def __valid_father_name(self):

        attribute_name = "Nombre de Apoderado"
        attribute_value = self.apoderado_nombre

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # length
        if not self.validation_length_minmax(attribute_name, attribute_value, 3,100): return False
        
        # no number
        if not self.validation_no_number(attribute_name, attribute_value): return False

        # no special characters
        if not self.validation_no_special(attribute_name, attribute_value, ".") : return False
        
        return True

    def __valid_father_adress(self):

        attribute_name = "Dirección del Apoderado"
        attribute_value = self.apoderado_domicilio

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # length
        if not self.validation_length_minmax(attribute_name, attribute_value, 10, 255): return False
        
        # no special characters
        if not self.validation_no_special(attribute_name, attribute_value) : return False
        
        return True
    
    def __valid_father_email(self):
        
        attribute_name = "Correo del Reclamante"
        attribute_value = self.apoderado_correo

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        return True

    def __valid_father_phone(self):

        attribute_name = "Celular del Apoderado"
        attribute_value = self.apoderado_telefono_celular

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # correct length
        if not self.validation_length_ab(attribute_name, attribute_value, 7,9): return False

        # no letter
        if not self.validation_no_letter(attribute_name, attribute_value): return False

        # no special
        if not self.validation_no_special(attribute_name, attribute_value, "."): return False
        
        return True

    def is_valid(self):

        if not self.__valid_father_name() : return False
        if not self.__valid_father_adress() : return False
        if not self.__valid_father_email() : return False
        if not self.__valid_father_phone() : return False

        return True

class Item(Validations):

    def __init__(self,bien_tipo,bien_monto,bien_descripcion) -> None:

        self.bien_tipo                   = bien_tipo
        self.bien_monto                  = bien_monto
        self.bien_descripcion            = bien_descripcion

    def __valid_item_list(self):

        attribute_name = "Tipo de Bien"
        attribute_value = self.bien_tipo

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # list pre setted
        if not self.validation_list(attribute_name, attribute_value, ["producto","servicio"]): return False

        return True

    def __valid_item_money(self):

        attribute_name = "Monto"
        attribute_value = self.bien_monto

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # no letters
        if not self.validation_no_letter(attribute_name, attribute_value): return False

        # length
        if not self.validation_length_minmax(attribute_name, attribute_value,1,7): return False

        # no special
        if not self.validation_decimal_format(attribute_name, attribute_value): return False
        
        return True
    
    def __valid_item_description(self):
        
        attribute_name = "Descripción del Bien"
        attribute_value = self.bien_descripcion

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # no letters
        if not self.validation_length_minmax(attribute_name, attribute_value,10,255): return False

        return True

    def is_valid(self):

        if not self.__valid_item_list()         : return False
        if not self.__valid_item_money()        : return False
        if not self.__valid_item_description()  : return False

        return True

class Claim(Validations):

    def __init__(self,reclamo_tipo,reclamo_descripcion,reclamo_pedido,reclamo_fecha) -> None:

        self.reclamo_tipo                = reclamo_tipo
        self.reclamo_descripcion         = reclamo_descripcion
        self.reclamo_pedido              = reclamo_pedido
        self.reclamo_fecha               = reclamo_fecha

    def __valid_claim_list(self):

        attribute_name = "Tipo de Reclamo"
        attribute_value = self.reclamo_tipo

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # list pre setted
        if not self.validation_list(attribute_name, attribute_value, ["reclamo","queja"]): return False

        return True

    def __valid_claim_description(self):
        
        attribute_name = "Descripción del Reclamo"
        attribute_value = self.reclamo_descripcion

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # length
        if not self.validation_length_minmax(attribute_name, attribute_value,10,255): return False

        return True

    def __valid_claim_query(self):
        
        attribute_name = "Descripción del Pedido"
        attribute_value = self.reclamo_pedido

        # no None Type
        if not self.validation_no_none(attribute_name, attribute_value): return False

        # length
        if not self.validation_length_minmax(attribute_name, attribute_value,10,255): return False

        # no special
        if not self.validation_no_special(attribute_name,attribute_value) : return False

        return True

    def is_valid(self):

        if not self.__valid_claim_list() : return False
        if not self.__valid_claim_description() : return False
        if not self.__valid_claim_query() : return False

        return True

class Pdf(ABC):

    def __divide_long_text(self, text, x):

        long_text       = text
        len_text        = len(text)
        text_area       = A4[0] - x                             
        char_len        = 20/4                                     
        total_char_fea  = math.floor(text_area / char_len)          
        total_lines     = math.floor(len_text / total_char_fea)            
        lines           = []

        for i in range(0, total_lines+1):
            
            lines.append(long_text[total_char_fea*i:total_char_fea*(i+1)])
        
        return lines

    def __create_text_object(self, canvas,text, x, y, fontsize):

        canvas.setFontSize(fontsize)
        text_object     = canvas.beginText(x,y)
        lines           = self.__divide_long_text(text,x)
        
        for line in lines:
            text_object.textLine(line)

        print("2nd method")
        return text_object

    @abstractmethod
    def create_pdf(self):

        try:

            # GENERAL VARIABLES
            BASE_DIR            = Path(__file__).resolve().parent.parent
            file_name           = f"rv_{self.id}.pdf"
            file_path           = f"{BASE_DIR}/complaint/media/reclamos/{file_name}"
            file_format         = "A4"
            file_title          = f"Reclamo N°{self.id}"
            file_restaurante    = "Cevicheria Puerto Nuevo"
            file_ruc            = f"RUC - 20504332340"
            message_one         = 'Estimado usuario, Su solicitud está en conocimiento de las autoridades, la cual se está analizando para emitir una respuesta y posible solución en un plazo máximo de 15 días. Conforme a lo establecido en el Código de Protección y Defensa del Consumidor este establecimiento cuenta con un Libro de Reclamaciones a tu disposición.'
            file_number         = f"HOJA DE RECLAMACIÓN - N°{self.id}"
            section             = [
                'Del Reclamante',
                'Del Apoderado',
                'Del Bien',
                'Del Reclamo',
            ]

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
                filename= file_path,
                pagesize= file_format
            )

            # PDF ::::::: TITLE
            pdf.setTitle(file_title)

            # HEADER ::::: NOMBRE + RUC
            pdf.setFontSize(20)
            pdf.drawString(tab_one,y_end-80,file_restaurante)
            pdf.setFontSize(15)
            pdf.drawString(tab_one,y_end-110,file_ruc)

            # HEADER :::::: MESSAGE 
            print("before")
            text = self.__create_text_object(pdf,message_one,tab_one,y_end-143,11)
            pdf.drawText(text)
            print("later")

            # HEADER :::::: NUMBER OF CLAIMANT
            pdf.rect(tab_one, y_end-230, x_middle-15,30)
            pdf.setFontSize(15)
            pdf.drawString(tab_two, y_end-222, file_number)

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
            pdf.drawString(tab_one,y_middle,section[1])
            pdf.line(tab_one, y_middle-5, x_middle, y_middle-5)
            pdf.setFontSize(11)
            pdf.drawString(tab_two,y_middle-20,f'- Nombre : {self.apoderado_nombre}')
            pdf.drawString(tab_two,y_middle-35,f'- Domicilio : {self.apoderado_domicilio}')
            pdf.drawString(tab_two,y_middle-50,f'- Correo : {self.apoderado_correo}')
            pdf.drawString(tab_two,y_middle-65,f'- Telefono : {self.apoderado_telefono_celular}')

            # BODY :::::::: ITEM
            pdf.setFontSize(13)
            pdf.drawString(tab_one,y_middle-105,section[2])
            pdf.line(tab_one, y_middle-110, x_middle+15, y_middle-110)
            pdf.setFontSize(11)
            pdf.drawString(tab_two,y_middle-125,f'- Tipo : {self.bien_tipo}')
            pdf.drawString(tab_two,y_middle-140,f'- Monto : {self.bien_monto}')
            pdf.drawString(tab_two,y_middle-155,f'- Descripción : ')
            text = self.__create_text_object(pdf,self.bien_descripcion,x+105,y_middle-155,11)
            pdf.drawText(text) 

            # BODY :::::: COMPLAIMANT
            pdf.setFontSize(13)
            pdf.drawString(tab_one,y_middle-215,section[3])
            pdf.line(tab_one, y_middle-220, x_middle+15, y_middle-220)
            pdf.setFontSize(11)
            pdf.drawString(tab_two,y_middle-235,f'- Tipo : {self.reclamo_tipo}')
            pdf.drawString(tab_two,y_middle-250,f'- Pedido : ')
            text = self.__create_text_object(pdf,self.reclamo_pedido,x+80,y_middle-250,11)
            pdf.drawText(text) 
            pdf.drawString(tab_two,y_middle-265,f'- Descripcion : ')
            text = self.__create_text_object(pdf,self.reclamo_descripcion,x+105,y_middle-265,11)
            pdf.drawText(text) 

            # FOOTER :::: DATE
            pdf.setFontSize(11)
            pdf.drawString(tab_one,y+10,self.reclamo_fecha)

            # PDF :::::: SAVING
            self.reclamo_pdf = f"{BASE_DIR}/media/reclamos/{file_name}"
            pdf.save()

            return True

        except:
     
            return False  

class Email(ABC):

    @abstractmethod
    def send_email(self):

        try:

            # variables for work
            BASE_DIR        = Path(__file__).resolve().parent.parent
            media_file      = f"{BASE_DIR}/complaint/media/reclamos/rv_{self.id}.pdf"
            email_sender    = config("email_sender")
            email_password  = config("email_password")
            email_receiver  = [self.reclamante_correo]  if self.apoderado_correo == ""  else [self.reclamante_correo, self.apoderado_correo] 
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
            with open(media_file, 'rb') as attachment_file:
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

            return False

class Formulario(Claimant, Father, Item, Claim, Pdf, Email):

    def __init__(self,id,reclamante_nombre,reclamante_domicilio,reclamante_tipo_documento,reclamante_numero_documento,reclamante_correo,reclamante_telefono_celular,reclamante_menor_edad,apoderado_nombre, apoderado_domicilio, apoderado_correo,apoderado_telefono_celular,bien_tipo,bien_monto,bien_descripcion,reclamo_tipo,reclamo_descripcion,reclamo_pedido,reclamo_fecha) -> None:

        self.id                          = id 
        Claimant.__init__(self,reclamante_nombre,reclamante_domicilio,reclamante_tipo_documento,reclamante_numero_documento,reclamante_correo,reclamante_telefono_celular,reclamante_menor_edad)
        Father.__init__(self,apoderado_nombre, apoderado_domicilio, apoderado_correo,apoderado_telefono_celular)
        Item.__init__(self,bien_tipo,bien_monto,bien_descripcion)
        Claim.__init__(self,reclamo_tipo,reclamo_descripcion,reclamo_pedido,reclamo_fecha)
        self.reclamo_pdf                 = None

    def apply_validations(self):

        if not Claimant.is_valid(self):
            return False
                
        if self.reclamante_menor_edad == "menor":

            if not Father.is_valid(self):
                return False
            
        elif self.reclamante_menor_edad == "mayor": 

            self.apoderado_nombre = ""
            self.apoderado_domicilio = ""
            self.apoderado_correo = ""
            self.apoderado_telefono_celular = ""

        if not Item.is_valid(self):
            return False

        if not Claim.is_valid(self):
            return False

        return True

    def create_pdf(self):

        if not Pdf.create_pdf(self) :
            Validations.errors.append("No se pudo crear un pdf con el documento de reclamación")
            return False
        
        return True

    def send_email(self):
       
        if not Email.send_email(self) :
            Validations.errors.append("No se pudo enviar el documento de reclamación por correo")
            return False
        
        return True

if __name__ == "__main__":

    queja = Formulario(
        # ID
        id="---",
        # RECLMANTE
        reclamante_nombre = "Anonimo",
        reclamante_domicilio = "Casa Anonima 123",
        reclamante_tipo_documento = "dni",
        reclamante_numero_documento= "12345678",
        reclamante_correo= "abc@abc.com",
        reclamante_telefono_celular = "123456789",
        reclamante_menor_edad = "menor", # valid for older
        # APODERADO
        apoderado_nombre = "Papa de Anonimo",
        apoderado_domicilio = "La misma cuadra",
        apoderado_correo = "abc@abc.com",
        apoderado_telefono_celular = "123456789",
        # BIEN
        bien_tipo = "producto",
        bien_monto = "1000.99",
        bien_descripcion = "Descripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamo",
        # RECLAMO
        reclamo_tipo = "queja",
        reclamo_pedido= "Descripcion del pedido", 
        reclamo_descripcion= "Descripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamoDescripción del reclamo",
        reclamo_fecha= "today"  
    )

    print(queja)
    print(queja.apply_validations())
    print(queja.errors)
    queja.create_pdf()
    queja.send_email()
