from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column ( db.Integer, primary_key=True)
    name = db.Column ( db.String(50), nullable = False)
    phone = db.Column ( db.String(50),nullable=False)

    def __repr__(self):
        return "<Contact %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone
        }


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column ( db.Integer, primary_key=True)
    nombre = db.Column ( db.String(50), nullable = False)
    apellido = db.Column ( db.String(50),nullable=False)
    correo = db.Column ( db.String(50),nullable=False)
    ubicacion = db.Column (db.String(50))
    descripcion = db.Column (db.String(200))
    contrasena = db.Column (db.String(50), nullable=False)
    nombre_usuario = db.Column (db.String(50), nullable=False)
    imagen_perfil = db.Column (db.String(100))
    requerimiento = db.relationship("Association", back_populates="requerimiento")
        
    def __repr__(self):
        return "<Usuario %r>" % self.nombre_usuario

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "ubicacion": self.ubicacion,
            "descripcion": self.descripcion,
            "contrasena": self.contrasena,
            "nombre_usuario": self.nombre_usuario,
            "imagen_perfil": self.imagen_perfil
        }

class Requerimiento(db.Model):
    __tablename__ = 'requerimiento'
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    cantidad_requerida = db.Column ( db.Integer, nullable = False)
    cantidad_actual = db.Column ( db.Integer, nullable = False)
    estado_requerimiento = db.Column (db.String(50))
    item = db.relationship("Item")
    usuario = db.relationship("Association", back_populates="usario")
        
    def __repr__(self):
        return "<Requerimiento %r>" % self.cantidad_requerida

    def serialize(self):
        return {
            "evento_id": self.evento_id,
            "item_id": self.item_id,
            "cantidad_requerida": self.cantidad_requerida,
            "cantidad_actual": self.cantidad_actual, 
            "estado del requerimiento": self.estado_requerimientos
        }

class Evento(db.Model):
    __tablename__ = 'evento'
    id = db.Column ( db.Integer, primary_key=True)
    titulo = db.Column ( db.String(50), nullable = False)
    descripcion = db.Column ( db.String(200),nullable=False)
    fecha_limite = db.Column ( db.String(50),nullable=False)
    estado_evento = db.Column (db.String(50))
    imagen = db.Relationship("Imagen", uselist=False, back_populates="evento")
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario = db.relationship("Usuario")
    requerimientos = db.relationship("Evento_Requerimiento")  
   
    def __repr__(self):
        return "<Evento %r>" % self.titulo

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "fecha_limite": self.fecha_limite,
            "estado_evento": self.estado_evento,
            "usuario_id": self.usuario_id
        }

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column ( db.Integer, primary_key=True)
    nombre = db.Column ( db.String(50), nullable = False)
    descripcion = db.Column ( db.String(50),nullable=False)
      
    def __repr__(self):
        return "<Item %r>" % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,          

        }

class Imagen(db.Model):
    __tablename__ = 'imagen'
    id = db.Column ( db.Integer, primary_key=True)
    evento = db.Relationship("Evento", back_populates="imagen")
    evento_id = db.Column ( db.Integer, db.ForeignKey(evento.id))
    imagen_Evento = db.Column ( db.String(250),nullable=False)
     

    def __repr__(self):
        return "<Imagen %r>" % self.imagen_Evento

    def serialize(self):
        return {
            "id": self.id,
            "imagen de evento": self.imagen_Evento,
            "id de evento": self.evento_id,
        }

class Participante(db.Model):
    __tablename__ = 'Participante'
    id = db.Column ( db.Integer, primary_key=True)
    item = db.relationship("Item", back_populates="item")
    evento = db.relationship("Evento", back_populates="evento")
    usuario = db.relationship("Usuario", back_populates="usuario")
    item_id = db.Column ( db.Integer, db.ForeignKey(item.id), primary_key=True)
    evento_id = db.Column ( db.Integer, db.ForeignKey(evento.id), primary_key=True)
    usuario_id = db.Column ( db.Integer, db.ForeignKey(usuario.id), primary_key=True)
    cantidad_Aportada = db.Column ( db.Integer,nullable=False)


    def __repr__(self):
        return "<Participante %r>" % self.cantidad_Aportada

    def serialize(self):
        return {
            "id": self.id,
            "cantidad aportada": self.cantidad_Aportada,
            "id de evento": self.evento_id,
            "id de usuario": self.usuario_id,
            "id de item": self.item_id,
        }
