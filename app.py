from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos sin credenciales
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/datoscuenta1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo de la base de datos
class Formulario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cuenta = db.Column(db.Integer, nullable=False)
    apartamento = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    capital = db.Column(db.Float, nullable=False)
    honorarios = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    carteras = db.Column(db.String(100), nullable=False)

# Manejo del contexto de la aplicación para la creación de tablas
with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return """<p>Hello, World Open Source!</p>"""

@app.route("/datos", methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Recoger los datos del formulario
        id_cuenta = request.form['ID_cuenta']
        apartamento = request.form['Apartamento']
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        capital = float(request.form['Capital'])
        honorarios = capital * 0.1
        total = capital + honorarios
        carteras = request.form['Carteras']

        # Crear una nueva entrada de formulario
        nuevo_formulario = Formulario(
            id_cuenta=id_cuenta, apartamento=apartamento, nombre=nombre, apellido=apellido,
            capital=capital, honorarios=honorarios, total=total, carteras=carteras
        )

        # Añadir y confirmar la transacción a la base de datos
        db.session.add(nuevo_formulario)
        db.session.commit()

        mensaje = "Formulario enviado exitosamente."
        return render_template("formulario.html", mensaje=mensaje)

    return render_template("formulario.html")

if __name__ == "__main__":
    app.run(debug=True)
