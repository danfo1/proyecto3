from flask import Flask, render_template, request, redirect, session , flash 
from flask_mysqldb import MySQL
from route.usuario import usuario 
from route.vehiculo import vehiculo1
from route.orden import ORDEN



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mg'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql = MySQL(app)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST' and 'usuario' in request.form and 'contrasena' in request.form:
        nombreusu = request.form['usuario']
        contrasena = request.form['contrasena']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE nombreusu=%s and contrasena=%s", (nombreusu, contrasena))
        account = cursor.fetchone()  # Utiliza fetchone para obtener una sola fila
        cursor.close()  # Cierra el cursor después de usarlo
        
        if account:
            session['logeado'] = True
            session['id'] = account['idusu']
            session['rol'] = account['fk_id_rol']
            return redirect('/inicio')  
        else:   
            flash('Nombre de usuario o contraseña incorrectos')
        
    return render_template('login.html')



@app.route("/inicio")
def inicio():
    if 'logeado' in session and 'rol' in session:
        if session['rol'] == 1:
            return render_template('inicio.html')
        elif session['rol'] == 2:
            return render_template('cliente.html')
    
    # Si no se cumple ninguna condición, devolver algo (puede ser un redirect, un render_template, etc.)
    return redirect('/login')
app.register_blueprint(ORDEN)
app.register_blueprint(vehiculo1)
app.register_blueprint(usuario)
if __name__ == '__main__':
    app.secret_key="daniel_forero"
    app.run(debug=True , host='0.0.0.0', port=5000 , threaded=True) 






    

    

        
 

       

    
