from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

app = Flask(__name__)
app.secret_key = 'una_clave_secreta_cualquiera'

# Lista de productos (puedes agregar más productos y campos aquí)
productos_lista = [
    {
        'id': '4',
        'nombre': 'Arduino Uno',
        'precio': 15.00,
        'imagen': 'images/arduino.jpg'
    },
    {
        'id': '5',
        'nombre': 'Sensor temp',
        'precio': 5.50,
        'imagen': 'images/sensor.jpg'
    },
    {
        'id': '6',
        'nombre': 'Pantalla LCD',
        'precio': 9.99,
        'imagen': 'images/lcd.jpg'
    },
    {
        'id': '7',
        'nombre': 'Raspberry Pi Pico',
        'precio': 6.00,
        'imagen': 'images/pico.png'
    },
    {
        'id': '8',
        'nombre': 'Sensor HC-SR04',
        'precio': 2.50,
        'imagen': 'images/ultrasonico.png'
    },
    {
        'id': '9',
        'nombre': 'ESP8266',
        'precio': 4.75,
        'imagen': 'images/esp8266.png'
    },
    {
        'id': '10',
        'nombre': 'Servo SG90',
        'precio': 3.20,
        'imagen': 'images/servo.png'
    },
    {
        'id': '11',
        'nombre': 'Matriz LED 8x8',
        'precio': 2.80,
        'imagen': 'images/ledmatrix.png'
    },
    {
        'id': '12',
        'nombre': 'Sensor de Luz LDR',
        'precio': 0.75,
        'imagen': 'images/ldr.png'
    },
    {
        'id': '13',
        'nombre': 'HC-05 Bluetooth',
        'precio': 4.30,
        'imagen': 'images/bluetooth.png'
    },
    {
        'id': '14',
        'nombre': 'Relevador',
        'precio': 1.80,
        'imagen': 'images/rele.png'
    },
    {
        'id': '15',
        'nombre': 'Potenciómetro',
        'precio': 1.50,
        'imagen': 'images/pot.png'
    },
    {
        'id': '16',
        'nombre': 'Pantalla OLED',
        'precio': 6.70,
        'imagen': 'images/oled.png'
    }
]


@app.route('/productos')
def productos():
    return render_template('productos.html', productos=productos_lista)


@app.route('/agregar/<id>')
def agregar_al_carrito(id):
    if 'carrito' not in session:
        session['carrito'] = {}

    carrito = session['carrito']

    producto = next((p for p in productos_lista if p['id'] == id), None)
    if producto:
        if id in carrito:
            carrito[id]['cantidad'] += 1
        else:
            carrito[id] = {
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'cantidad': 1
            }
        session['carrito'] = carrito
        flash(f"{producto['nombre']} agregado al carrito.")
    else:
        flash("Producto no encontrado.")

    return redirect(url_for('productos'))


@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render_template('carrito.html', carrito=carrito, total=total)


@app.route('/eliminar/<id>', methods=['POST'])
def eliminar_producto(id):
    carrito = session.get('carrito', {})
    if id in carrito:
        del carrito[id]
        session['carrito'] = carrito
        flash("Producto eliminado del carrito.")
    return redirect(url_for('ver_carrito'))


@app.route('/cambiar_cantidad/<id>', methods=['POST'])
def cambiar_cantidad(id):
    nueva_cantidad = int(request.form.get('cantidad', 1))
    carrito = session.get('carrito', {})
    if id in carrito:
        if nueva_cantidad > 0:
            carrito[id]['cantidad'] = nueva_cantidad
        else:
            del carrito[id]
        session['carrito'] = carrito
    return redirect(url_for('ver_carrito'))


@app.route('/')
def raiz():
    return redirect(url_for('inicio'))


@app.route('/inicio')
def inicio():
    return render_template('inicio.html')


if __name__ == '__main__':
    app.run(debug=True)