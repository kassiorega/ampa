from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Adotante(db.Model):
    __tablename__ = 'Adotantes'
    id_adotante = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    endereco = db.Column(db.Text, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    data_cadastro = db.Column(db.Date, server_default=db.func.current_date())
    animais = db.relationship('Animal', backref='tutor', lazy=True)

class Animal(db.Model):
    __tablename__ = 'Animais'
    id_animal = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(100))
    idade = db.Column(db.Integer) # Consider using DATE for nascimento if preferred
    sexo = db.Column(db.String(1)) # M ou F
    porte = db.Column(db.String(20))
    saude = db.Column(db.Text)
    historico = db.Column(db.Text)
    numero_chip = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(50), nullable=False, default='registrado com tutor') # Default status for this registration type
    id_abrigo = db.Column(db.Integer, db.ForeignKey('Abrigos.id_abrigo'), nullable=True) # Nullable as it's with tutor
    id_adotante = db.Column(db.Integer, db.ForeignKey('Adotantes.id_adotante'), nullable=True) # Link to tutor

# Note: We are not defining Abrigo, Adocao, Voluntario, Campanha models here
# as the current requirement is focused on registering animals with tutors.
# The Abrigos table is referenced by ForeignKey, ensure it exists in the DB.
# We might need a minimal Abrigos model if strict FK checks are enabled or if needed later.

# Minimal Abrigo model just for FK reference if needed, otherwise ensure table exists.
class Abrigo(db.Model):
    __tablename__ = 'Abrigos'
    id_abrigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    # Add other fields if needed later

