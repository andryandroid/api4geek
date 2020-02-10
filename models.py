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

class Evento(db.Model):
    __tablename__ = 'evento'
    id = db.Column ( db.Integer, primary_key=True)
    titulo = db.Column ( db.String(50), nullable = False)
    descripcion = db.Column ( db.String(50),nullable=False)
    fecha_limite = db.Column ( db.String(50),nullable=False)
    estado_evento = db.Column (db.String(50))
    imagen = db.Relationship("Imagen", uselist=False, back_populates="evento")
   

    def __repr__(self):
        return "<Evento %r>" % self.titulo

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "fecha_limite": self.fecha_limite,
            "estado_evento": self.estado_evento,
            "usuario_id": self.usuario_id,

        }

class Requerimiento(db.Model):
    __tablename__ = 'requerimiento'
    id = db.Column ( db.Integer, primary_key=True)
    nombre = db.Column ( db.String(50), nullable = False)
    descripcion = db.Column ( db.String(50),nullable=False)
      

    def __repr__(self):
        return "<Requerimiento %r>" % self.nombre

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

class Participantes(db.Model):
    __tablename__ = 'Participantes'
    id = db.Column ( db.Integer, primary_key=True)
    requerimiento_id = db.Column ( db.Integer, db.ForeignKey(requerimiento.id), primary_key=True)
    evento_id = db.Column ( db.Integer, db.ForeignKey(evento.id), primary_key=True)
    usuario_id = db.Column ( db.Integer, db.ForeignKey(usuario.id), primary_key=True)
    cantidad_Aportada = db.Column ( db.Integer,nullable=False)
    

    def __repr__(self):
        return "<Participantes %r>" % self.cantidad_Aportada

    def serialize(self):
        return {
            "id": self.id,
            "cantidad aportada": self.cantidad_Aportada,
            "id de evento": self.evento_id,
            "id de usuario": self.usuario_id,
            "id de requerimiento": self.requerimiento_id,
        }