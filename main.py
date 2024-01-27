from flask import Flask, render_template, request, redirect, url_for,flash, jsonify, session,  send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json, os
from datetime import timedelta

app = Flask(__name__)

app.secret_key = 'S0l03nt1D10s'  # Cambia esto por una clave secreta segura.

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
######################## Manejo de inicio de Sesión ########################
# Configuración de Flask-Login
login_manager = LoginManager(app)

login_manager.login_view = 'login'

# Clase de usuario para Flask-Login
class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

# Cargar usuarios desde el archivo JSON
with open('usuarios.json', 'r', encoding='utf-8') as users_file:
    users_data = json.load(users_file)

# Crear objetos de usuario a partir de los datos cargados
users = {username: User(username, data[1]) for username, data in users_data.items()}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        password = request.form['contrasena']

        user = users.get(nombre_usuario)
        if user and password == users_data.get(nombre_usuario, [None])[0]:
            login_user(user)
            return redirect(url_for('inicio'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'success')  # Agrega un mensaje de éxito
    return redirect(url_for('login'))  # Redirige al inicio de sesión

@app.route('/inicio', methods=['GET', 'POST'])
@login_required
def inicio():
    rol = current_user.role
    usuario = current_user.id
    return render_template('calendario.html', rol = rol, usuario=usuario)
############################################################################################


############################ Bloque para la oración ############################

def cargar_tareas():
    with open('tareas.json', 'r', encoding='utf-8') as json_file:
        tareas = json.load(json_file)
    return tareas

@app.route('/oracion')
@login_required
def mostrarTareasActivas():
    tareas = cargar_tareas()
    rol = current_user.role
    return render_template('mostrarTareaActiva.html', tareas=tareas, rol=rol)

@app.route('/sumar_oracion', methods=['POST'])
def sumar_veces_oradas():
    # Obtén el índice del elemento que se está sumando
    index = int(request.form.get('index')) - 1

    # Lee el JSON desde el archivo
    with open('tareas.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 0 <= index < len(data):
        # Accede al elemento en la posición especificada y actualiza el 'total'
        print(data[index])
        data[index]['total'] += 1
        print(data[index])
        # Escribe el JSON actualizado de vuelta al archivo
        with open('tareas.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        return jsonify({'message': 'Operación exitosa'})
    else:
        return jsonify({'message': 'Índice fuera de rango'}), 400

@app.route('/marcar_completa', methods=['POST'])
def marcar_completa():
    data = request.get_json()
    index = data.get('index', None)
    testimonio = data.get('testimonio', '')  # Obtener el testimonio ingresado por el usuario

    if index is not None:
        index = int(index) - 1

        with open('tareas.json', 'r', encoding='utf-8') as json_file:
            tareas = json.load(json_file)

            if 0 <= index < len(tareas):
                tarea = tareas[index]

                if tarea['isActive'] == 'True':
                    tarea['isActive'] = 'False'
                    tarea['fechaFinal'] = format_date(datetime.now(), format='d-MMMM-y', locale='es_ES')

                    # Agregar el testimonio si se proporciona
                    if testimonio:
                        tarea['testimonio'] = testimonio

        with open('tareas.json', 'w', encoding='utf-8') as json_file:
            json.dump(tareas, json_file, indent=2)

        # Devolver las tareas actualizadas en la respuesta
        return jsonify(success=True, tareas_actualizadas=tareas)
    else:
        return jsonify(success=False, error='Índice no proporcionado')


############################################################################################


############################ Bloque para la Hora Silenciosa ############################
from datetime import datetime, timedelta
from babel.dates import format_date, format_datetime
import pytz
zhl = pytz.timezone('America/Mexico_City')
dias_semana = {'Monday': 'Lunes','Tuesday': 'Martes','Wednesday': 'Miércoles','Thursday': 'Jueves','Friday': 'Viernes','Saturday': 'Sábado','Sunday': 'Domingo'}

@app.route('/hora_silenciosa', methods=['GET', 'POST'])
@login_required
def hora_silenciosa():

    rol = current_user.role
    usuario = current_user.id
    devocional, fecha_actual, dia, nombre_dia1 = devocional_del_dia()

    fecha_actual = datetime.now(zhl)
    nombre_dia = dias_semana[fecha_actual.strftime('%A').capitalize()]
    if request.method =='POST':
        if usuario_ha_enviado_formulario_hoy(usuario):
            return render_template('formularioEnviado.html')  # Mostrar un mensaje de error
        else:
            exp_autor = request.form['exp_autor']
            apl_vida = request.form['apl_vida']
            dudas = request.form['dudas']
            fecha_domingo_anterior, fecha_sabado_siguiente, hoy = obtener_semana_actual()

            semana_actual = f'{fecha_domingo_anterior.day} al {fecha_sabado_siguiente.day} de {format_date(fecha_domingo_anterior, "MMMM", locale="es")}'
            ruta_archivo = os.path.join('data', f'hora_silenciosa_de_{usuario}.json')
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    datos_usuario = json.load(f)
            else:
                datos_usuario = {
                    'nombre': usuario,
                    'semana': []
                }

            semana_actual_existe = False
            for semana in datos_usuario['semana']:
                if semana['semanaActual'] == semana_actual:
                    semana_actual_existe = True
                    semana['info'].append({
                        'dia': nombre_dia,
                        'queExpresa': exp_autor,
                        'comoaplicar': apl_vida,
                        'pregunta': dudas
                    })
                    break

            if not semana_actual_existe:
                datos_usuario['semana'].append({
                    'semanaActual': semana_actual,
                    'info': [{
                        'dia': nombre_dia,
                        'queExpresa': exp_autor,
                        'comoaplicar': apl_vida,
                        'pregunta': dudas
                    }]
                })
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_usuario, f, ensure_ascii=False, indent=4)
            # Cierra la sesión del usuario
            if os.path.exists(FORMULARIOS_ENVIADOS_JSON):
                with open(FORMULARIOS_ENVIADOS_JSON, 'r', encoding='utf-8') as f:
                    datos_envio = json.load(f)
            else:
                datos_envio = {}

            fecha_actual = fecha_actual = fecha_actual.strftime('%Y-%m-%d %H')
            usuario_datos = datos_envio.get(usuario, [])
            usuario_datos.append(fecha_actual)
            datos_envio[usuario] = usuario_datos

            with open(FORMULARIOS_ENVIADOS_JSON, 'w', encoding='utf-8') as f:
                json.dump(datos_envio, f, ensure_ascii=False, indent=4)

            contabilizar_puntos(usuario)
            return render_template('gracias.html')  # Muestra mensaje de agradecimiento
    # Si el método de la solicitud es GET, muestra el formulario
    return render_template('horaSilenciosa.html',rol = rol, usuario=usuario, entrada_dia_actual=devocional, fecha_actual=fecha_actual, dia=dia, nombre_dia1=nombre_dia1)


# Ruta al archivo JSON que registra las fechas de envío de formularios
FORMULARIOS_ENVIADOS_JSON = 'formulariosEnviados.json'

# Función para verificar si un usuario ya envió el formulario hoy
def usuario_ha_enviado_formulario_hoy(usuario):
    fecha_actual = datetime.now(zhl)
    if os.path.exists(FORMULARIOS_ENVIADOS_JSON):
        with open(FORMULARIOS_ENVIADOS_JSON, 'r', encoding='utf-8') as f:
            datos_envio = json.load(f)
        usuario_datos = datos_envio.get(usuario, [])
        fecha_actual = fecha_actual = fecha_actual.strftime('%Y-%m-%d %H')
        print(f"HOLA SOY NUEVA{fecha_actual}")
        return fecha_actual in usuario_datos
    return False

def devocional_del_dia():
    with open('horaSilenciosa.json', 'r', encoding='utf-8') as archivo_hs:
        devocionales = json.load(archivo_hs)

    fecha_actual = datetime.now(zhl)
    print(f"Aquiii sooy el devocional fecha: {fecha_actual}")
    nombre_dia = dias_semana[fecha_actual.strftime('%A')]
    fecha_actual = fecha_actual.strftime(f'{nombre_dia} %d, %Y').capitalize()
    entrada_dia_actual = None
    for devocional in devocionales:
        if devocional['fecha'] == fecha_actual:
            entrada_dia_actual = devocional

    return entrada_dia_actual, fecha_actual, devocional['fecha'], nombre_dia

def obtener_semana_actual():
    zona_horaria_local = pytz.timezone('America/Mexico_City')
    hoy = datetime.now(zona_horaria_local)
    dias_domingo_anterior = (hoy.weekday() + 1) % 7
    fecha_domingo_anterior = hoy - timedelta(days = dias_domingo_anterior)
    dias_sabado_siguiente = (5-hoy.weekday())%7
    fecha_sabado_siguiente = hoy + timedelta (days=dias_sabado_siguiente)

    return fecha_domingo_anterior, fecha_sabado_siguiente, hoy

############################################################################################

############################ Bloque para los puntos ############################
def abrir_usuarios():
    ruta_usuarios = 'usuarios.json'
    datos_usuarios = None

    if os.path.exists(ruta_usuarios):
        with open(ruta_usuarios, 'r', encoding='utf-8') as f:
            datos_usuarios = json.load(f)

    return datos_usuarios

def abrir_equipos():
    ruta_equipo = 'equipos.json'
    datos_equipo = None

    if os.path.exists(ruta_equipo):
        with open(ruta_equipo, 'r', encoding='utf-8') as f:
            datos_equipo = json.load(f)

    return datos_equipo


def escribir_usuarios(datos_usuarios):
    ruta_usuarios = 'usuarios.json'

    with open(ruta_usuarios, 'w', encoding='utf-8') as f:
        json.dump(datos_usuarios, f, ensure_ascii=False)

def escribir_equipos(datos_equipos):
    ruta_equipos = 'equipos.json'

    with open(ruta_equipos, 'w', encoding='utf-8') as f:
        json.dump(datos_equipos, f, ensure_ascii=False)

def contabilizar_puntos(usuario):
    ruta_equipos = 'equipos.json'

    datos_usuarios = abrir_usuarios()
    datos_equipos = abrir_equipos()

    if usuario in datos_usuarios:
        puntos_actual = datos_usuarios[usuario][2]
        datos_usuarios[usuario][2] = puntos_actual + 100

        # Obtener el equipo del usuario
        equipo = datos_usuarios[usuario][3]

        print(equipo)

        # Verificar el equipo y agregar puntos correspondientes
        if equipo == "CP":  # Chicas Super Poderosas
            puntos_equipo = int(datos_equipos["Chicas Super Poderosas"])
            puntos_equipo += 100
            datos_equipos["Chicas Super Poderosas"] = puntos_equipo
        elif equipo == "CB":  # Chicos del Barrio
            puntos_equipo = int(datos_equipos["Chicos del Barrio"])
            puntos_equipo += 100
            datos_equipos["Chicos del Barrio"] = puntos_equipo

        escribir_usuarios(datos_usuarios)
        escribir_equipos(datos_equipos)

    else:
        print("El usuario no se encontró en el archivo JSON.")

############################################################################################

############################ Bloque para mostrar los puntos ############################

# @app.route('/tabla_puntos')
# def tabla_puntos():
#     return render_template("puntos.html")
@app.route('/ruta-en-tu-servidor-flask', methods=['POST'])
def manejar_puntos():
    data = request.json
    equipos = abrir_equipos()
    opcion = data.get('opcion')
    puntos = int (data.get('puntos'))
    equipoVF = True

    for equipo in equipos:
    # Verificar el equipo y agregar puntos correspondientes
        if opcion == "CP+":
            equipos['Chicas Super Poderosas'] += puntos
            equipoVF = False
            break
        elif opcion == "CB+":
            equipos['Chicos del Barrio'] += puntos
            equipoVF = True
            break
        elif opcion == "CP-":
            equipos['Chicas Super Poderosas'] -= puntos
            equipoVF = False
            break
        elif opcion == "CB-":
            equipos['Chicos del Barrio'] -= puntos
            equipoVF = True
            break

    escribir_equipos(equipos)
    #escribir_usuarios(datos_usuarios)
    if equipoVF == True:
        print(equipoVF)
        return jsonify(equipos['Chicos del Barrio'])
    else:
        print(equipoVF)
        return jsonify(equipos['Chicas Super Poderosas'])

@app.route('/tabla_puntos_sumar')
def tabla_puntos_sumar():
    return render_template("puntosSumar.html")

# # Ruta para cargar y mostrar la tabla de usuarios
# @app.route('/mostrar_usuarios')
# def mostrar_usuarios():
#     usuarios = abrir_usuarios()
#     usuarios_ordenados = dict(sorted(usuarios.items(), key=lambda item: item[1][2], reverse=True))
#     return render_template("puntos.html", usuarios=usuarios_ordenados, mostrar_usuarios=True)

@app.route('/mostrar_usuarios_admin')
def mostrar_usuarios_admin():
    usuarios = abrir_usuarios()
    rol = current_user.role
    usuarios_ordenados = dict(sorted(usuarios.items(), key=lambda item: item[1][2], reverse=True))
    return render_template("puntosSumar.html", usuarios=usuarios_ordenados, mostrar_usuarios=True, rol = rol)

# # Ruta para cargar y mostrar la tabla de equipos
# @app.route('/mostrar_equipos')
# def mostrar_equipos():
#     equipos = abrir_equipos()
#     return render_template("puntos.html", mostrar_equipos=True, equipos=equipos)

@app.route('/mostrar_equipos_admin')
def mostrar_equipos_admin():
    rol = current_user.role
    equipos = abrir_equipos()
    return render_template("puntosSumar.html", mostrar_equipos=True, equipos=equipos, rol = rol)


preguntas = []
with open('preguntas.json', 'r', encoding='utf-8') as json_file:
    preguntas = json.load(json_file)

import random
import hashlib
def obtener_id_usuario():
    if 'usuario_id' not in session:
        # Genera un nuevo ID de usuario y guárdalo en la sesión
        session['usuario_id'] = random.randint(1, 1000000)
    return session['usuario_id']

@app.route('/procesar_voto', methods=['GET'])
def procesar_voto():
    global preguntas
    pregunta = request.args.get('pregunta')
    usuario_id = obtener_id_usuario()

    # Verificar si el usuario ya ha votado por esta pregunta
    if f"{usuario_id}-{pregunta}" not in session.get('votos', []):
        for bloque in preguntas:
            pregunta2 = bloque['texto']
            votos = bloque['votos']
            if pregunta == pregunta2:
                bloque['votos'] = bloque['votos'] + 1

                # Marcar que este usuario ya votó por esta pregunta
                votos_registrados = session.get('votos', [])
                votos_registrados.append(f"{usuario_id}-{pregunta}")
                session['votos'] = votos_registrados

                break

        with open('preguntas.json', 'w', encoding='utf-8') as json_file:
            json.dump(preguntas, json_file)

    return redirect('/preguntas_anonimas')

def generar_color_oscuro():
    r = random.randint(0, 128)
    g = random.randint(0, 128)
    b = random.randint(0, 128)
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

@app.route('/preguntas_anonimas')
def preguntas_anonimas():
    # Ordena las preguntas de mayor a menor basado en los votos
    cabecera_html = "<div onclick=\"mostrarContenido(this)\" class=\"col-sm-12\" style=\"position: relative; overflow: auto; word-wrap: break-word; background-color: {}; color: white; min-height: 7em;\">"
    contenido_html = "<span class=\"contenido\"> {pregunta} </span> <i class=\"fa-solid fa-star\" style=\"position: absolute; bottom: 8px; right: 5px;\"></i><small style=\"position: absolute; bottom: 5px; right: 30px;\">{votos}</small></div>"
    txt = ''
    preguntas_ordenadas = sorted(preguntas, key=lambda x: x['votos'], reverse=True)

    for bloque in preguntas_ordenadas:
        pregunta = bloque['texto']
        votos = bloque['votos']
        color_oscuro = generar_color_oscuro()
        txt += f'{cabecera_html.format(color_oscuro)} {contenido_html.format(pregunta=pregunta, votos=votos)}'

    return render_template('preguntasAnonimas.html', preguntas=txt)


"""@app.route('/procesar_voto', methods=['GET'])
def procesar_voto():
    global preguntas
    print(preguntas)
    pregunta = request.args.get('pregunta')
    print("Soy la pregunta: ", pregunta)
    # Aquí puedes realizar el procesamiento del voto o cualquier otra lógica necesaria
    # ...
    for bloque in preguntas:
        pregunta2 = bloque['texto']
        votos = bloque['votos']
        if pregunta == pregunta2:
            bloque['votos'] = bloque['votos']+1
            break;
    with open('preguntas.json', 'w', encoding='utf-8') as json_file:
        json.dump(preguntas, json_file)
    # Redirige a la página principal u otra ruta según tus necesidades
    return redirect('/preguntas_anonimas')"""

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/events.json')
def events_json():
    return send_from_directory('static', 'events.json')

@app.route('/procesar_pregunta', methods=['POST'])
def procesar_pregunta():
    global preguntas
    nueva_pregunta = request.json.get('pregunta')
    print("Soy la nueva pregunta: ")
    if nueva_pregunta:
        with open('preguntas.json', 'r', encoding='utf-8') as json_file:
            preguntas = json.load(json_file)

        preguntas.append({"texto": nueva_pregunta, "votos": 0})

        with open('preguntas.json', 'w', encoding='utf-8') as json_file:
            json.dump(preguntas, json_file, indent=2)

        return jsonify({"status": "success"})

    return redirect('/preguntas_anonimas')
############################################################################################

@app.route('/save_events', methods=['POST'])
def save_events():
    try:
        data = request.json
        with open('static/events.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)
        return jsonify({'message': 'Events saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#====================================================================================================#
# """
# [miércoles 18:46] Esteban Garciaa
# SELECT NumProveedor, Cli_Id, OrdenCompra, Folio, UUID, Estatus, FechaRecepcion,

#   replace(replace( replace(	REPLACE(REPLACE( REPLACE(UltimoMensaje, 'C:\_MasterEDI\OBJ_GENERIC\', ''), 'InvoiceIn\', ''), 'MEDI_INVOICE_', ''), 'Renombrando documento ', ''), '.reqretryxtemp', ''), '.reqretry', '') Mensaje

#   FROM [Masteredi].[dbo].[EdiControlDoctos]

#   --WHERE Estatus = 0

#   ORDER BY Id ASC;
# [miércoles 18:47] Esteban Garciaa
# 192.168.1.125 / sa / srvdesarrollo
# """



#====================================================================================================#


if __name__ == '__main__':
    app.run(debug=True)