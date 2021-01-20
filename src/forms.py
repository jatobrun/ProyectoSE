from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, ValidationError
from src import tabla_carritos, tabla_productos

class BuscadorForm(FlaskForm):
    carrito = StringField('Carrito', validators=[
                           DataRequired(message='Ingrese un numero de carrito porfavor')])
    submit = SubmitField('Consultar')
    
    def validar_carrito(self, carrito):
        carrito = tabla_carritos.find_one({'carrito_id': carrito.data})
        if not(carrito):
            raise ValidationError(
                'Este carrito no existe. Porfavor ingrese bien el codigo')


class PagoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
                           DataRequired(message='Ingrese su nombre porfavor')])
    apellido = StringField('Apellido', validators=[
                           DataRequired(message='Ingrese su apellido porfavor')])
    cedula = StringField('Cedula', validators=[
                           DataRequired(message='Ingrese su cedula porfavor porfavor')])
    email = StringField('Email', validators=[DataRequired(
        message='Ingrese un email porfavor')])
    tarjeta = StringField('Tarjeta de Credito', validators=[
                           DataRequired(message='Ingrese una tarjeta de credito')])
    submit = SubmitField('Pagar')

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
                           DataRequired(message='Ingrese su nombre porfavor')])
    fabricante = StringField('Fabricante', validators=[
                           DataRequired(message='Ingrese un fabricante porfavor')])
    codigo = StringField('Codigo', validators=[
                           DataRequired(message='Ingrese un codigo porfavor')])
    precio = IntegerField('Precio', validators=[
                           DataRequired(message='Ingrese un precio porfavor')])
    imagen = FileField('Foto')
    submit = SubmitField('Crear Producto')  

    def validar_producto(self, codigo):
        producto = tabla_productos.find_one({'codigo': codigo.data})
        if producto:
            raise ValidationError(
                'Este codigo ya existe. Porfavor ingrese otro  codigo')