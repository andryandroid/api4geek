import os
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Usuario, Evento, Participante, Imagen, Item, Requerimiento
from flask_cors import CORS
from flask_uploads import UploadSet, configure_uploads, IMAGES #libreria para cargar imagenes


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG']= True
app.config['ENV']= 'development'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+ os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['UPLOADED_PHOTOS_DEST']= '/img' #carpeta de destino de imagenes subidas
CORS(app)

photos = UploadSet('photos', IMAGES) #configuracion de flask_uploads
configure_uploads(app, photos) #configuracion de flask_uploads

db.init_app(app)

Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route("/")
def home():
    
    return render_template("index.html")

@app.route("/usuario", methods=['GET', 'POST'])
@app.route("/usuario/<int:id>", methods=['GET', 'PUT', 'DELETE'])

def usuario(id=None):
    if request.method == 'GET':
        if id is not None:
            usuario = Usuario.query.get(id)
            if usuario:
                return jsonify(usuario.serialize()), 200
            else:
                return jsonify({"msg":"User not found"}), 404
        else:
            usuario = Usuario.query.all()
            usuario = list(map(lambda usuario: usuario.serialize(), usuario))
            return jsonify(usuario), 200

    if request.method == 'POST':
        nombre = request.json.get('nombre', None)
        apellido = request.json.get('apellido', None)
        correo = request.json.get('correo', None)
        ubicacion = request.json.get('ubicacion', None)
        descripcion = request.json.get('descripcion', None)
        contrasena = request.json.get('contrasena', None)
        nombre_usuario = request.json.get('nombre_usuario', None)
        imagen_perfil = request.json.get('imagen_perfil', None)

        if not nombre:
            return jsonify({"msg":"name is required"}), 422

        if not apellido:
            return jsonify({"msg":"Last name is required"}), 422

        if not correo:
            return jsonify({"msg":"email is required"}), 422

        if not contrasena:
            return jsonify({"msg":"password is required"}), 422

        if not nombre_usuario:
            return jsonify({"msg":"user name is required"}), 422    

        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario:
            return jsonify({"msg":"correo electronico no disponible"}), 422
        
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if usuario:    
            return jsonify({"msg":"Nombre de Usuario no disponible"}), 422

        usuario = Usuario()
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.correo = correo
        usuario.ubicacion = ubicacion
        usuario.descripcion = descripcion
        usuario.contrasena = contrasena
        usuario.nombre_usuario = nombre_usuario
        usuario.imagen_perfil = imagen_perfil


        db.session.add(usuario)
        db.session.commit()

        return jsonify(usuario.serialize()), 201

    if request.method == 'PUT':
        nombre = request.json.get('nombre', None)
        apellido = request.json.get('apellido', None)
        correo = request.json.get('correo', None)
        ubicacion = request.json.get('ubicacion', None)
        descripcion = request.json.get('descripcion', None)
        contrasena = request.json.get('contrasena', None)
        nombre_usuario = request.json.get('nombre_usuario', None)
        imagen_perfil = request.json.get('imagen_perfil', None)

        if not nombre:
            return jsonify({"msg":"name is required"}), 422

        if not apellido:
            return jsonify({"msg":"Last name is required"}), 422

        if not correo:
            return jsonify({"msg":"email is required"}), 422

        if not contrasena:
            return jsonify({"msg":"password is required"}), 422

        if not nombre_usuario:
            return jsonify({"msg":"user name is required"}), 422

        usuario = Usuario.query.get(id)

        if not usuario:
                return jsonify({"msg":"User not found"}), 404

        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.correo = correo
        usuario.ubicacion = ubicacion
        usuario.descripcion = descripcion
        usuario.contrasena = contrasena
        usuario.nombre_usuario = nombre_usuario
        usuario.imagen_perfil = imagen_perfil

        db.session.commit()

        return jsonify(usuario.serialize()), 200

    if request.method == 'DELETE':

        usuario = Usuario.query.get(id)

        if not usuario:
                return jsonify({"msg":"User not found"}), 404

        db.session.delete(usuario)
        db.session.commit()

        return jsonify({"msg":"User deleted"}), 200

@app.route("/evento", methods=['GET', 'POST'])
@app.route("/evento/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def evento(id=None):
    if request.method == 'GET':
        if id is not None:
            evento = Evento.query.get(id)
            if evento:
                return jsonify(evento.serialize()), 200
            else:
                return jsonify({"msg":"Evento not found"}), 404
        else:
            evento = Evento.query.all()
            evento = list(map(lambda evento: evento.serialize(), evento))
            return jsonify(evento), 200
    if request.method == 'POST':
        titulo = request.json.get('titulo', None)
        descripcion = request.json.get('descripcion', None)
        fecha_limite = request.json.get('fecha_limite', None)
        estado_evento = request.json.get('estado_evento', None)
        usuario_id = request.json.get('usuario_id', None)
        if not titulo:
            return jsonify({"msg":"title is required"}), 422
        if not descripcion:
            return jsonify({"msg":"description is required"}), 422
        if not fecha_limite:
            return jsonify({"msg":"deadline is required"}), 422
        if not estado_evento:
            return jsonify({"msg":"event status is required"}), 422    
        
        if not usuario_id:
            return jsonify({"msg":"user id is required"}), 422
         
        evento = Evento()
        evento.titulo = titulo
        evento.descripcion = descripcion
        evento.fecha_limite = fecha_limite
        evento.estado_evento = estado_evento
        evento.usuario_id = usuario_id
        db.session.add(evento)
        db.session.commit()
        return jsonify(evento.serialize()), 201
    if request.method == 'PUT':
        titulo = request.json.get('titulo', None)
        descripcion = request.json.get('descripcion', None)
        fecha_limite = request.json.get('fecha_limite', None)
        estado_evento = request.json.get('estado_evento', None)
        usuario_id = request.json.get('usuario_id', None)
        if not titulo:
            return jsonify({"msg":"title is required"}), 422
        if not descripcion:
            return jsonify({"msg":"description is required"}), 422
        if not fecha_limite:
            return jsonify({"msg":"deadline is required"}), 422
        if not estado_evento:
            return jsonify({"msg":"event status is required"}), 422    
        if not usuario_id:
            return jsonify({"msg":"user id is required"}), 422
        evento = Evento.query.get(id)
        if not evento:
                return jsonify({"msg":"Evento not found"}), 404
        evento.titulo = titulo
        evento.descripcion = descripcion
        evento.fecha_limite = fecha_limite
        evento.estado_evento = estado_evento
        evento.usuario_id = usuario_id
        db.session.commit()
        return jsonify(evento.serialize()), 200
    if request.method == 'DELETE':
        evento = Evento.query.get(id)
        if not evento:
                return jsonify({"msg":"Evento not found"}), 404
        db.session.delete(evento)
        db.session.commit()
        return jsonify({"msg":"Evento deleted"}), 200

@app.route("/item", methods=['GET', 'POST'])
@app.route("/item/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def item(id=None):
    if request.method == 'GET':
        if id is not None:
            item = Item.query.get(id)
            if item:
                return jsonify(item.serialize()), 200
            else:
                return jsonify({"msg":"item not found"}), 404
        else:
            item = Item.query.all()
            item = list(map(lambda item: item.serialize(), item))
            return jsonify(item), 200
    if request.method == 'POST':
        nombre = request.json.get('nombre', None)
        descripcion = request.json.get('descripcion', None)
       
        if not nombre:
            return jsonify({"msg":"name is required"}), 422
        if not descripcion:
            return jsonify({"msg":"description is required"}), 422
         
        item = Item()
        item.nombre = nombre
        item.descripcion = descripcion
        
        db.session.add(item)
        db.session.commit()
        return jsonify(item.serialize()), 201
    if request.method == 'PUT':
        nombre = request.json.get('nombre', None)
        descripcion = request.json.get('descripcion', None)
     
        if not nombre:
            return jsonify({"msg":"name is required"}), 422
        if not descripcion:
            return jsonify({"msg":"description is required"}), 422
        
        item = Item.query.get(id)
        if not item:
                return jsonify({"msg":"item not found"}), 404
        item.nombre = nombre
        item.descripcion = descripcion
        
        db.session.commit()
        return jsonify(item.serialize()), 200
    if request.method == 'DELETE':
        item = Item.query.get(id)
        if not item:
                return jsonify({"msg":"item not found"}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({"msg":"item deleted"}), 200


@app.route("/requerimiento", methods=['GET', 'POST'])
@app.route("/requerimiento/<int:id>", methods=['GET', 'PUT', 'DELETE'])

def requerimiento(id=None):
    if request.method == 'GET':
        if id is not None:
            requerimiento = Requerimiento.query.get(id)
            if requerimiento:
                return jsonify(requerimiento.serialize()), 200
            else:
                return jsonify({"msg":"Requerimiento not found"}), 404
        else:
            requerimiento = Requerimiento.query.all()
            requerimiento = list(map(lambda requerimiento: requerimiento.serialize(), requerimiento))
            return jsonify(requerimiento), 200

    if request.method == 'POST':
        evento_id = request.json.get('evento_id', None)
        item_id = request.json.get('item_id', None)
        cantidad_requerida = request.json.get('cantidad_requerida', None)
        cantidad_actual = request.json.get('cantidad_actual', None)
        estado_requerimiento = request.json.get('estado_requerimiento', None)

        if not evento_id:
            return jsonify({"msg":"evento_id is required"}), 422

        if not item_id:
            return jsonify({"msg":"item_id is required"}), 422

        if not cantidad_requerida:
            return jsonify({"msg":"cantidad requerida is required"}), 422

        if not cantidad_actual:
            return jsonify({"msg":"cantidad actual is required"}), 422

        if not estado_requerimiento:
            return jsonify({"msg":"estado requerimiento is required"}), 422    

        requerimiento = Requerimiento()
        requerimiento.evento_id = evento_id
        requerimiento.item_id = item_id
        requerimiento.cantidad_requerida = cantidad_requerida
        requerimiento.cantidad_actual = cantidad_actual
        requerimiento.estado_requerimiento = estado_requerimiento

        db.session.add(requerimiento)
        db.session.commit()

        return jsonify(requerimiento.serialize()), 201

    if request.method == 'PUT':
        evento_id = request.json.get('evento_id', None)
        item_id = request.json.get('item_id', None)
        cantidad_requerida = request.json.get('cantidad_requerida', None)
        cantidad_actual = request.json.get('cantidad_actual', None)
        estado_requerimiento = request.json.get('estado_requerimiento', None)

        if not evento_id:
            return jsonify({"msg":"evento id is required"}), 422

        if not item_id:
            return jsonify({"msg":"item id is required"}), 422

        if not cantidad_requerida:
            return jsonify({"msg":"cantidad requerida is required"}), 422

        if not cantidad_actual:
            return jsonify({"msg":"cantidad actual is required"}), 422

        if not estado_requerimiento:
            return jsonify({"msg":"estado requerimiento is required"}), 422

        requerimiento = Requerimiento.query.get(id)

        if not requerimiento:
                return jsonify({"msg":"Requerimiento not found"}), 404

        requerimiento.evento_id = evento_id
        requerimiento.item_id = item_id
        requerimiento.cantidad_requerida = cantidad_requerida
        requerimiento.cantidad_actual = cantidad_actual
        requerimiento.estado_requerimiento = estado_requerimiento

        db.session.commit()

        return jsonify(requerimiento.serialize()), 200

    if request.method == 'DELETE':

        requerimiento = Requerimiento.query.get(id)

        if not requerimiento:
                return jsonify({"msg":"Requerimiento not found"}), 404

        db.session.delete(requerimiento)
        db.session.commit()

        return jsonify({"msg":"Requerimiento deleted"}), 200


@app.route("/participante", methods=['GET', 'POST'])
@app.route("/participante/<int:id_usuario>/<int:id_requerimiento>", methods=['GET', 'PUT', 'DELETE'])

def participante(id_usuario=None, id_requerimiento = None):
    if request.method == 'GET':
        if id_usuario is not None and id_requerimiento is not None:
            participante = Participante.query.get(( id_usuario , id_requerimiento ))
            if participante:
                return jsonify(participante.serialize()), 200
            else:
                return jsonify({"msg":"participante not found"}), 404
        else:
            participante = Participante.query.all()
            participante = list(map(lambda participante: participante.serialize(), participante))
            return jsonify(participante), 200

    if request.method == 'POST':
        
        requerimiento_id = request.json.get('requerimiento_id', None)
        usuario_id = request.json.get('usuario_id', None)
        cantidad_aportada = request.json.get('cantidad_aportada', None)

        if not requerimiento_id:
            return jsonify({"msg":"requerimiento_id is required"}), 422

        if not usuario_id:
            return jsonify({"msg":"usuario_id is required"}), 422

        if not cantidad_aportada:
            return jsonify({"msg":"cantidad_aportada is required"}), 422

        participante = Participante()
        participante.requerimiento_id = requerimiento_id
        participante.usuario_id = usuario_id
        participante.cantidad_aportada = cantidad_aportada

        db.session.add(participante)
        db.session.commit()

        return jsonify(participante.serialize()), 201

    if request.method == 'PUT':
        requerimiento_id = request.json.get('requerimiento_id', None)
        usuario_id = request.json.get('usuario_id', None)
        cantidad_aportada = request.json.get('cantidad_aportada', None)

        if not requerimiento_id:
            return jsonify({"msg":"requerimiento_id is required"}), 422

        if not usuario_id:
            return jsonify({"msg":"usuario_id is required"}), 422

        if not cantidad_aportada:
            return jsonify({"msg":"cantidad_aportada is required"}), 422
        
        participante = Participante.query.get(( id_usuario , id_requerimiento ))
        
        if not participante:
                return jsonify({"msg":"participante not found"}), 404

        participante.requerimiento_id = requerimiento_id
        participante.usuario_id = usuario_id
        participante.cantidad_aportada = cantidad_aportada

        db.session.commit()

        return jsonify(participante.serialize()), 200

    if request.method == 'DELETE':

        participante = Participante.query.get(( id_usuario , id_requerimiento ))

        if not participante:
                return jsonify({"msg":"participante not found"}), 404

        db.session.delete(participante)
        db.session.commit()

        return jsonify({"msg":"Participante deleted"}), 200

@app.route("/imagen", methods=['GET', 'POST'])
@app.route("/imagen/<int:id>/<int:id_evento>", methods=['GET', 'PUT', 'DELETE'])
def imagen(id=None):
    if request.method == 'GET':
        if id is not None:
            imagen = Imagen.query.get(id)
            if imagen:
                return jsonify(imagen.serialize()), 200
            else:
                return jsonify({"msg":"image not found"}), 404
        else:
            imagen = Imagen.query.all()
            imagen = list(map(lambda imagen: imagen.serialize(), imagen))
            return jsonify(imagen), 200
    if request.method == 'POST':
        imagen_Evento = request.json.get('imagen de evento', None)
        
        if not imagen_Evento:
            return jsonify({"msg":"event image is required"}), 422
         
        imagen = Imagen()
        imagen.imagen_Evento = imagen_Evento
        
        db.session.add(imagen)
        db.session.commit()
        return jsonify(imagen.serialize()), 201
    if request.method == 'PUT':
        imagen_Evento = request.json.get('imagen de evento', None)
     
        if not imagen_Evento:
            return jsonify({"msg":"event image is required"}), 422
        
        imagen = Imagen.query.get(id)
        if not imagen:
                return jsonify({"msg":"image not found"}), 404
        item.imagen_Evento = imagen_Evento
        
        db.session.commit()
        return jsonify(imagen.serialize()), 200
    if request.method == 'DELETE':
        imagen = Imagen.query.get(id)
        if not imagen:
                return jsonify({"msg":"image not found"}), 404
        db.session.delete(imagen)
        db.session.commit()
        return jsonify({"msg":"image deleted"}), 200


@app.route("/login", methods=['GET', 'POST'])
def login(correo=None):
    if request.method == 'POST':
        correo = request.json.get('correo', None)
        contrasena = request.json.get('contrasena', None)

        if not correo:
            return jsonify({"msg":"correo is required"}), 422

        if not contrasena:
            return jsonify({"msg":"contrasena is required"}), 422

        login = Usuario.query.filter_by(correo=correo).first()
        if login:
            if login.contrasena != contrasena:
                return jsonify({"msg":"contrasena incorrecta"}), 404
            else:    
                return jsonify(login.serialize()), 200
        else:
            return jsonify({"msg":"User not found"}), 404\


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        photos = request.json.get('photo', None)
        filename= photos.save(request.files['photo'])
        if not photos:
            return jsonify({"msg":"image file is required"}), 422

        photos = Imagen()
        imagen.imagen_Evento = filename
                
        db.session.add(photos)
        db.session.commit()
        return jsonify(imagen.serialize()), 201
        

if __name__=="__main__":
    manager.run()