from flask import Flask, render_template, request, jsonify
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

# YOUTUBE VIDEO: https://www.youtube.com/watch?v=-1DmVCPB6H8&list=LL&index=17

app = Flask(__name__)       # un objeto tipo flask que recibe un nombre

#Conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'abaco'

conexion = MySQL(app)

# @app.before_request         # funciones para examinar o ejecutar operaciones antes y después de la petición
# def before_request():
#     print("Antes de la petición..")

# @app.after_request
# def after_request(response):
#     print("Después de la petición")
#     return response


@app.route('/')         # ruta raíz de la app
def index():            # una vista llamada index que está en la raíz de la app, un def es una vista
    # return "<h1>This is heading 1</h1>"
    cursos=['php', 'css', 'html']
    # cursos=[]
    data={
        'cursos':cursos,
        'numero_cursos':len(cursos),
        'titulo':'Index',
        'bienvenida':'saludos gente 2'
    }
    return render_template('index.html',data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre,edad):          # una vista nueva, llamada contacto
    data={
        'titulo':'Contacto',
        'nombre': nombre,
        'edad': edad,
    }
    return render_template('contacto.html',data=data)

def query_string():  # recuperar parámetros desde la request en URLS dinamicas

    print(request)
    print(request.args)
    print(request.args.get('param1'))
    return "OK"


@app.route('/cursos')
def listar_cursos():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT Nombre FROM curso ORDER BY Nombre ASC"
        cursor.execute(sql)
        cursos = cursor.fetchall()
        data['mensaje']='Exito'
        cursos_list = []
        
        for e in range(len(cursos)):
            cursos_list.append(cursos[e][0])    
        print(cursos_list)

        data['cursos'] = cursos_list
    except Exception as ex:
        data['mensaje'] = 'Error...'

    # return jsonify(data)
    return render_template('cursos.html',cursos_list=cursos_list)


def pagina_no_encontrada(error):   # vista para error 404
    # return render_template('404.html'), 404    # renderiza html de 404
    return redirect(url_for('index'))        # redirecciona a la página principal de index

if __name__=='__main__':
    app.add_url_rule('/query_string',view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada) # asociar la vista de 404 al error 404
    app.run(debug=True,port=5021)