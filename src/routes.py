from PIL import Image
import os
import time
import secrets
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from src import app, tabla_productos, tabla_carritos
from src.forms import BuscadorForm, PagoForm, ProductoForm
from bson.objectid import ObjectId

@app.route('/', methods =['GET', 'POST'])
def home():
    form = BuscadorForm()
    if form.validate_on_submit():
        carrito = tabla_carritos.find_one({'carrito_id': form.carrito.data})
        if carrito:
            session['carrito_id'] = form.carrito.data
            print(session['carrito_id'])
            return redirect(url_for('buscar_carrito'))
        flash('No existe el carrito', 'warning')
    return render_template('buscador.html', form = form)

@app.route('/carritos', methods = ['POST'])
def crear_carritos():
    lista = request.get_data().decode("utf-8").split(',')
    carrito_id = lista[1]
    producto_id = lista[0]
    print(carrito_id)
    carrito = tabla_carritos.find_one({'carrito_id': carrito_id})
    producto = tabla_productos.find_one({'codigo': producto_id})
    if not(carrito):
        carrito = {
                'carrito_id': carrito_id,
                'productos': [producto['codigo']],
                'objetos':[producto],
                'cantidades': [1]

                }
        tabla_carritos.insert_one(carrito)
    else:
        productos = carrito['productos']
        cantidades = carrito['cantidades']
        objetos = carrito['objetos']
        if producto['codigo'] in productos:
            index = productos.index(producto_id)
            cantidades[index] += 1
        else:
            productos.append(producto_id)
            cantidades.append(1)
            objetos.append(producto)

        cambios = {
                    'productos': productos,
                    'objetos': objetos,
                    'cantidades': cantidades
                    }
        tabla_carritos.update_one(
                                    {'carrito_id': carrito_id}, 
                                    {'$set': cambios}
                                    )

    return jsonify({'status': 'ok'})
@app.route('/carritos/', methods = ['GET'])
def buscar_carrito():
    final = []
    carrito = tabla_carritos.find_one({'carrito_id': session['carrito_id']})
    productos = carrito['objetos']
    cantidades = carrito['cantidades']
    for indice, producto in enumerate(productos):
        elemento = (producto, cantidades[indice])
        final.append(elemento)
    return render_template('carrito.html', productos = final)

@app.route('/producto', methods = ['GET', 'POST'])
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        picture_file, f_ext = save_picture(form.imagen.data)
        producto = {
                    'nombre': form.nombre.data,
                    'fabricante': form.fabricante.data,
                    'codigo': form.codigo.data,
                    'precio': form.precio.data,
                    'imagen': picture_file
                    }
        tabla_productos.insert_one(producto)
        form.nombre.data = ''
        form.fabricante.data = ''
        form.codigo.data = ''
        form.precio.data = 0
        flash('Producto creado satisfactoriamente', 'success')
    
    return render_template('producto.html', form = form)

@app.route('/productos', methods = ['GET'])
def ver_productos():
    productos = tabla_productos.find_one({})
    if productos:
        productos = tabla_productos.find({})
        return render_template('productos.html', productos=productos)
    else: 
        return render_template('productos.html', vacio_productos = True)
    return render_template('productos.html', productos=productos)

@app.route('/pago', methods = ['GET', 'POST'])
def pago():
    form = PagoForm()
    if form.validate_on_submit():
        flash('Gracias por su compra')
        return redirect(url_for('logout'))
    return render_template('pago.html', form = form)

@app.route("/logout")
def logout():
    tabla_carritos.delete_one({'carrito_id': session['carrito_id']})
    session.clear()

    flash('Pago realizado satisfactoriamente')
    return redirect(url_for('home'))

@app.route("/productos/<_id>/delete", methods=['POST'])
def borrar_producto(_id):
    tabla_productos.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('ver_productos'))



def save_picture(form_picture):
    extensions = ['.jpg', '.jpeg', '.tif', '.png', '.PNG']
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    if f_ext in extensions:
        picture_path = os.path.join(
            app.root_path, 'static/Productos', picture_fn)
        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

    return picture_fn, f_ext