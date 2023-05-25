from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from transbank.webpay.webpay_plus.transaction import Transaction
from models import Producto, Region, Comuna, Categoria, TipoPago, Venta, DetalleVenta, Usuario


# 3. instanciamos la app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:musicpro1234AB@db.colafxnkypjqvelgindi.supabase.co:5432/postgres'


#db.init_app(app)

#Migrate(app, db)

# 5. Creamos la ruta por defecto para saber si mi app esta funcionado
# 6. ejecutamos el comando en la consola: python app.py o python3 app.py y revisamos nuestro navegador
@cross_origin()
@app.route('/')
def index():
    """Bienvenida a la API Tienda de MusicPro"""
    return 'MusicPro Api Tienda V 0.1'

@cross_origin()
@app.route('/productos', methods=['GET'])
def get_productos():
    """Ruta para consultar todos los productos"""
    productos = Producto.query.all()
    productos = list(map(lambda producto: producto.serialize(), productos))
    #opcional con imagen
    #productos = list(map(lambda producto: producto.serialize_with_image(), productos))
    return jsonify(productos), 200

@cross_origin()
@app.route('/regiones', methods=['GET'])
def get_regiones():
    """Ruta para consultar todas las regiones"""
    regiones = Region.query.all()
    regiones = list(map(lambda region: region.serialize(), regiones))
    return jsonify(regiones), 200

@cross_origin()
@app.route('/comunas', methods=['GET'])
def get_comunas():
    """Ruta para consultar todas las comunas"""
    comunas = Comuna.query.all()
    comunas = list(map(lambda comuna: comuna.serialize(), comunas))
    return jsonify(comunas), 200

@cross_origin()
@app.route('/categorias', methods=['GET'])
def get_categorias():
    """Ruta para consultar todas las categorias"""
    categorias = Categoria.query.all()
    categorias = list(map(lambda categoria: categoria.serialize(), categorias))
    return jsonify(categorias), 200

@cross_origin()
@app.route('/tipos-pago', methods=['GET'])
def get_tipos_pago():
    """Ruta para consultar todos los tipos de pago"""
    tipos_pago = TipoPago.query.all()
    tipos_pago = list(map(lambda tipo_pago: tipo_pago.serialize(), tipos_pago))
    return jsonify(tipos_pago), 200

@cross_origin()
@app.route('/agregar-venta', methods=['POST'])
def agregar_venta():
    """Ruta para agregar una venta"""
    data = request.get_json()
    venta = Venta()
    venta.total = data['total']
    venta.id_tipo_pago = data['id_tipo_pago']
    venta.id_usuario = data['id_usuario']
    venta.save()
    return jsonify(venta.serialize()), 201

@cross_origin()
@app.route('/agregar-detalle-venta', methods=['POST'])
def agregar_detalle_venta():
    """Ruta para agregar un detalle de venta"""
    data = request.get_json()
    detalle_venta = DetalleVenta()
    detalle_venta.cantidad = data['cantidad']
    detalle_venta.valor = data['valor']
    detalle_venta.id_venta = data['id_venta']
    detalle_venta.cod_producto = data['cod_producto']
    detalle_venta.descuento = data['descuento']
    detalle_venta.save()
    return jsonify(detalle_venta.serialize()), 201

##### METODOS DE USUARIO #####

@cross_origin()
@app.route('/agregar-usuario', methods=['POST'])
def agregar_usuario():
    """Ruta para agregar un usuario"""
    data = request.get_json()
    usuario = Usuario()
    usuario.nombres = data['nombres']
    usuario.apellidos = data['apellidos']
    usuario.domicilio = data['domicilio']
    usuario.id_comuna = data['id_comuna']
    usuario.fono = data['fono']
    usuario.nombre_usuario = data['nombre_usuario']
    usuario.password = data['password'] #TODO: encriptar password
    usuario.tipo = data['tipo']
    usuario.save()
    return jsonify(usuario.serialize()), 201

@cross_origin()
@app.route('/login', methods=['POST'])
def login():
    """Ruta para iniciar sesion"""
    data = request.get_json()
    usuario = Usuario.query.filter_by(nombre_usuario=data['nombre_usuario']).first()
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    if usuario.password != data['password']:
        return jsonify({"msg": "Contraseña incorrecta"}), 404
    return jsonify(usuario.serialize()), 200

##### METODOS DE API EXTERNA #####
### API WEBPAY ###

@cross_origin()
@app.route('/webpay', methods=['POST'])
def webpay():
    """Crea una transaccion webpay"""
    data = request.get_json()
    buy_order = '123456789'
    session_id = '123456789'
    amount = data['valor']
    return_url = 'http://127.0.0.1:5500/test.html'

    transaction = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    tx = Transaction().create(buy_order, session_id, amount, return_url)

    transaction.update(tx)

    return jsonify(transaction), 200

@cross_origin()
@app.route('/webpay/commit', methods=['POST'])
def webpay_commit():
    """Confirma una transaccion webpay"""
    data = request.get_json()
    token = data['token_ws']
    tx = Transaction().commit(token)
    return jsonify(tx), 200



# 4. Configurar los puertos nuestra app 
if __name__ == '__main__':
    app.run(debug=True, port=8000)




