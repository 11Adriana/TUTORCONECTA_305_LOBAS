from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Base de datos de usuarios
usuarios_db = {
    "jessi@correo.com": {"password": "123", "nombre": "Jessi", "tipo": "Administrativo", "materia": None, "hijo": None},
    "ana@correo.com": {"password": "123", "nombre": "Ana", "tipo": "Administrativo", "materia": None, "hijo": None},
    "zenaido@correo.com": {"password": "123", "nombre": "Zenaido", "tipo": "Administrativo", "materia": None, "hijo": None},
    
    "josem@correo.com": {"password": "123", "nombre": "Prof. Jose M", "tipo": "Docente", "materia": "Geografia (GEO)", "hijo": None},
    "fab@correo.com": {"password": "123", "nombre": "Prof. Fab", "tipo": "Docente", "materia": "Historia (HIS)", "hijo": None},
    "rox@correo.com": {"password": "123", "nombre": "Profa. Rox", "tipo": "Docente", "materia": "Espanol (ESP)", "hijo": None},
    "kas@correo.com": {"password": "123", "nombre": "Profa. Kas", "tipo": "Docente", "materia": "Ciencias (CIE)", "hijo": None},
    "celene@correo.com": {"password": "123", "nombre": "Profa. Celene", "tipo": "Docente", "materia": "Matematicas (MAT)", "hijo": None},
    "anayeli@correo.com": {"password": "123", "nombre": "Profa. Anayeli", "tipo": "Docente", "materia": "Artes (ART)", "hijo": None},
    "ninive@correo.com": {"password": "123", "nombre": "Profa. Ninive", "tipo": "Docente", "materia": "Ingles (ING)", "hijo": None},
    "justino@correo.com": {"password": "123", "nombre": "Prof. Justino", "tipo": "Docente", "materia": "Computacion (Comp)", "hijo": None},
    "gilberto@correo.com": {"password": "123", "nombre": "Prof. Gilberto", "tipo": "Docente", "materia": "PEC", "hijo": None},
    "josue@correo.com": {"password": "123", "nombre": "Prof. Josue", "tipo": "Docente", "materia": "Formacion Civica y Etica (FCE)", "hijo": None},

    "tutor_maria@correo.com": {"password": "123", "nombre": "Tutor de Maria", "tipo": "Padre de familia", "materia": None, "hijo": "Maria Perez"},
    "tutor_paola@correo.com": {"password": "123", "nombre": "Tutor de Paola", "tipo": "Padre de familia", "materia": None, "hijo": "Paola Salgado"},
    "tutor_luis@correo.com": {"password": "123", "nombre": "Tutor de Luis", "tipo": "Padre de familia", "materia": None, "hijo": "Luis Flores"},
    "tutor_bernardo@correo.com": {"password": "123", "nombre": "Tutor de Bernardo", "tipo": "Padre de familia", "materia": None, "hijo": "Bernardo Lopez"},
    "tutor_carlos@correo.com": {"password": "123", "nombre": "Tutor de Carlos", "tipo": "Padre de familia", "materia": None, "hijo": "Carlos Jimenez"},

    "maria@correo.com": {"password": "123", "nombre": "Maria Perez", "tipo": "Alumno", "materia": None, "hijo": "Maria Perez"},
    "paola@correo.com": {"password": "123", "nombre": "Paola Salgado", "tipo": "Alumno", "materia": None, "hijo": "Paola Salgado"},
    "luis@correo.com": {"password": "123", "nombre": "Luis Flores", "tipo": "Alumno", "materia": None, "hijo": "Luis Flores"},
    "bernardo@correo.com": {"password": "123", "nombre": "Bernardo Lopez", "tipo": "Alumno", "materia": None, "hijo": "Bernardo Lopez"},
    "carlos@correo.com": {"password": "123", "nombre": "Carlos Jimenez", "tipo": "Alumno", "materia": None, "hijo": "Carlos Jimenez"}
}

materias_oficiales = [
    "Espanol (ESP)", "Matematicas (MAT)", "Ciencias (CIE)", "Historia (HIS)", 
    "Ingles (ING)", "Geografia (GEO)", "Artes (ART)", "Computacion (Comp)", 
    "PEC", "Formacion Civica y Etica (FCE)", "Educacion Fisica (EFI)"
]

calificaciones_db = {}
for alumno in ["Maria Perez", "Paola Salgado", "Luis Flores", "Bernardo Lopez", "Carlos Jimenez"]:
    calificaciones_db[alumno] = [
        {"materia": mat, "p1": 9.0, "p2": 8.5, "p3": 9.0, "promedio": 8.8, "observacion": "Buen desempeno en clase."} for mat in materias_oficiales
    ]

asistencias_db = [
    {"alumno": "Paola Salgado", "fecha": "2026-10-08", "estado": "Asistencia"},
    {"alumno": "Paola Salgado", "fecha": "2026-10-16", "estado": "Falta"},
    {"alumno": "Paola Salgado", "fecha": "2026-10-21", "estado": "Retardo"},
    {"alumno": "Maria Perez", "fecha": "2026-10-08", "estado": "Asistencia"},
    {"alumno": "Maria Perez", "fecha": "2026-10-16", "estado": "Retardo"},
    {"alumno": "Luis Flores", "fecha": "2026-10-15", "estado": "Falta"}
]

mensajes_motivacion = {}
fortalezas_guardadas = {
    "Maria Perez": ["Estudiosa", "Creativa", "Puntual"],
    "Paola Salgado": ["Dedicada", "Entusiasta", "Puntual"],
    "Luis Flores": ["Participativo", "Agil", "Companero"],
    "Bernardo Lopez": ["Analitico", "Responsable", "Atento"],
    "Carlos Jimenez": ["Constante", "Lider", "Solidario"]
}

avisos_db = [
    {"titulo": "Reunion General de Padres", "contenido": "Se les invita cordialmente a la junta trimestral este viernes a las 10:00 AM.", "emisor": "Administracion"},
    {"titulo": "Inicio de Evaluaciones", "contenido": "Los examenes del segundo parcial comenzaran la proxima semana.", "emisor": "Direccion Escolar"}
]

tareas_db = [
    {"id": 1, "materia": "Matematicas (MAT)", "titulo": "Resolver ejercicios de la pagina 45", "fecha_entrega": "2026-10-28", "destinatario": "Grupo General", "estado": "Por entregar"},
    {"id": 2, "materia": "Historia (HIS)", "titulo": "Entrega de linea del tiempo de la Independencia", "fecha_entrega": "2026-10-30", "destinatario": "Grupo General", "estado": "Realizada"}
]

calendario_db = [
    {"id": 1, "evento": "Examen Parcial de Matematicas", "fecha": "2026-10-28", "estado": "Pendiente"},
    {"id": 2, "evento": "Consejo Tecnico Escolar (Sin clases)", "fecha": "2026-10-30", "estado": "Realizada"}
]

reportes_db = [
    {"alumno": "Paola Salgado", "docente": "Prof. Jose M", "motivo": "Uso de telefono celular en clase", "fecha": "2026-10-18"}
]

@app.route('/')
def login():
    error = request.args.get('error')
    return render_template('login.html', error=error)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    correo = request.form.get('usuario')
    password = request.form.get('password')
    
    if correo in usuarios_db and usuarios_db[correo]["password"] == password:
        usr = usuarios_db[correo]
        hijo = usr["hijo"] if usr["hijo"] else "Maria Perez"
        
        if usr["tipo"] == "Padre de familia":
            return redirect(url_for('calificaciones', usuario=usr["nombre"], tipo=usr["tipo"], hijo=hijo))
        elif usr["tipo"] == "Docente":
            return redirect(url_for('calificaciones', usuario=usr["nombre"], tipo=usr["tipo"], materia=usr["materia"]))
        else:
            return redirect(url_for('bienvenida', usuario=usr["nombre"], tipo=usr["tipo"], hijo=hijo))
    else:
        return redirect(url_for('login', error="Datos incorrectos. Intentalo de nuevo."))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    mensaje = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        tipo = request.form.get('tipo')
        hijo = request.form.get('hijo') if tipo == 'Padre de familia' else nombre

        if correo in usuarios_db:
            mensaje = "El correo ya esta registrado."
        else:
            usuarios_db[correo] = {
                "password": password,
                "nombre": nombre,
                "tipo": tipo,
                "materia": "Matematicas (MAT)" if tipo == 'Docente' else None,
                "hijo": hijo
            }
            target_alumno = hijo if tipo == 'Padre de familia' else nombre
            if (tipo == 'Alumno' or tipo == 'Padre de familia') and target_alumno not in calificaciones_db:
                calificaciones_db[target_alumno] = []
                
            return redirect(url_for('login'))
            
    return render_template('registro.html', mensaje=mensaje)

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

@app.route('/socioemocional', methods=['GET', 'POST'])
def socioemocional():
    usuario = request.args.get('usuario')
    hijo = request.args.get('hijo')
    tipo = request.args.get('tipo')
    
    if request.method == 'POST':
        f1 = request.form.get('f1')
        f2 = request.form.get('f2')
        f3 = request.form.get('f3')
        if f1 and f2 and f3:
            fortalezas_guardadas[hijo] = [f1, f2, f3]
        return redirect(url_for('bienvenida', usuario=usuario, tipo=tipo, hijo=hijo))
        
    fortalezas = fortalezas_guardadas.get(hijo, ["", "", ""])
    return render_template('socioemocional.html', usuario=usuario, hijo=hijo, tipo=tipo, fortalezas=fortalezas)

@app.route('/bienvenida')
def bienvenida():
    usuario = request.args.get('usuario', 'Usuario')
    tipo = request.args.get('tipo', 'Alumno')
    hijo = request.args.get('hijo', '')
    materia = request.args.get('materia', '')

    for correo, datos in usuarios_db.items():
        if datos["nombre"] == usuario:
            tipo = datos["tipo"]
            if datos["materia"]:
                materia = datos["materia"]
            if datos["hijo"]:
                hijo = datos["hijo"]
            break

    return render_template('bienvenida.html', usuario=usuario, tipo=tipo, hijo=hijo, materia=materia)

@app.route('/calificaciones', methods=['GET', 'POST'])
def calificaciones():
    usuario = request.args.get('usuario', 'Usuario')
    tipo = request.args.get('tipo', 'Alumno')
    hijo = request.args.get('hijo', 'Maria Perez')
    materia_docente = request.args.get('materia', '')

    for correo, datos in usuarios_db.items():
        if datos["nombre"] == usuario:
            tipo = datos["tipo"]
            if datos["materia"]:
                materia_docente = datos["materia"]
            if datos["hijo"]:
                hijo = datos["hijo"]
            break

    if request.method == 'POST' and tipo == 'Docente':
        alumno_obj = request.form.get('alumno_obj')
        parcial_sel = request.form.get('parcial_sel')
        nota = request.form.get('nota')
        observacion_text = request.form.get('observacion', '')
        
        if alumno_obj not in calificaciones_db:
            calificaciones_db[alumno_obj] = []

        encontrado_mat = False
        for item in calificaciones_db[alumno_obj]:
            if item["materia"] == materia_docente:
                encontrado_mat = True
                if nota:
                    item[parcial_sel] = float(nota)
                    item["promedio"] = round((float(item.get("p1", 0)) + float(item.get("p2", 0)) + float(item.get("p3", 0))) / 3, 1)
                if observacion_text:
                    item["observacion"] = observacion_text
        
        if not encontrado_mat:
            calificaciones_db[alumno_obj].append({
                "materia": materia_docente, 
                "p1": float(nota) if parcial_sel == 'p1' else 0.0, 
                "p2": float(nota) if parcial_sel == 'p2' else 0.0, 
                "p3": float(nota) if parcial_sel == 'p3' else 0.0, 
                "promedio": float(nota) if nota else 0.0, 
                "observacion": observacion_text
            })

    if request.method == 'POST' and tipo == 'Padre de familia':
        mensaje = request.form.get('mensaje_motivacion')
        if mensaje:
            mensajes_motivacion[hijo] = mensaje

    if tipo == 'Docente':
        hijo = request.args.get('hijo', 'Maria Perez')

    lista_calificaciones = calificaciones_db.get(hijo, [])
    msg_actual = mensajes_motivacion.get(hijo, "")
    fortalezas = fortalezas_guardadas.get(hijo, [])
    
    return render_template('calificaciones.html', usuario=usuario, tipo=tipo, hijo=hijo, materia=materia_docente, calificaciones=lista_calificaciones, mensaje=msg_actual, fortalezas=fortalezas, alumnos_lista=list(calificaciones_db.keys()))

@app.route('/asistencia', methods=['GET', 'POST'])
def asistencia():
    usuario = request.args.get('usuario', 'Usuario')
    tipo = request.args.get('tipo', 'Alumno')
    materia = request.args.get('materia', '')
    
    for correo, datos in usuarios_db.items():
        if datos["nombre"] == usuario:
            tipo = datos["tipo"]
            if datos["materia"]:
                materia = datos["materia"]
            break

    if request.method == 'POST':
        hijo = request.form.get('alumno_sel')
        fecha_sel = request.form.get('fecha_sel')
        estado_sel = request.form.get('estado_sel')
        
        if fecha_sel and estado_sel and (tipo == 'Administrativo' or tipo == 'Docente'):
            encontrado = False
            for reg in asistencias_db:
                if reg["alumno"] == hijo and reg["fecha"] == fecha_sel:
                    reg["estado"] = estado_sel
                    encontrado = True
                    break
            if not encontrado:
                asistencias_db.append({"alumno": hijo, "fecha": fecha_sel, "estado": estado_sel})
    else:
        hijo = request.args.get('alumno_sel', request.args.get('hijo', 'Maria Perez'))

    historial = [a for a in asistencias_db if a["alumno"] == hijo]

    mapa_asistencias = {}
    for reg in asistencias_db:
        if reg["alumno"] == hijo and reg["fecha"].startswith("2026-10-"):
            dia_str = str(int(reg["fecha"].split("-")[2]))
            mapa_asistencias[dia_str] = reg["estado"]

    return render_template('asistencia.html', usuario=usuario, tipo=tipo, hijo=hijo, materia=materia, asistencias=historial, mapa_asistencias=mapa_asistencias, alumnos_lista=list(calificaciones_db.keys()))

@app.route('/avisos', methods=['GET', 'POST'])
def avisos():
    usuario = request.args.get('usuario', 'Usuario')
    tipo = request.args.get('tipo', 'Alumno')
    hijo = request.args.get('hijo', '')
    materia = request.args.get('materia', '')

    for correo, datos in usuarios_db.items():
        if datos["nombre"] == usuario:
            tipo = datos["tipo"]
            if datos["materia"]:
                materia = datos["materia"]
            if datos["hijo"]:
                hijo = datos["hijo"]
            break

    if request.method == 'POST' and tipo == 'Administrativo':
        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')
        if titulo and contenido:
            avisos_db.append({"titulo": titulo, "contenido": contenido, "emisor": usuario})

    return render_template('avisos.html', usuario=usuario, tipo=tipo, hijo=hijo, materia=materia, avisos=avisos_db)

@app.route('/tareas', methods=['GET', 'POST'])
def tareas():
    usuario = request.args.get('usuario', 'Usuario')
    tipo = request.args.get('tipo', 'Alumno')
    hijo = request.args.get('hijo', '')
    materia = request.args.get('materia', '')

    for correo, datos in usuarios_db.items():
        if datos["nombre"] == usuario:
            tipo = datos["tipo"]
            if datos["materia"]:
                materia = datos["materia"]
            if datos["hijo"]:
                hijo = datos["hijo"]
            break

    if request.method == 'POST':
        accion = request.form.get('accion')
        if accion == 'crear' and tipo == 'Docente':
            titulo = request.form.get('titulo')
            fecha_entrega = request.form.get('fecha_entrega')
            destinatario = request.form.get('destinatario')
            estado = request.form.get('estado')
            if titulo and fecha_entrega:
                nuevo_id = len(tareas_db) + 1
                tareas_db.append({"id": nuevo_id, "materia": materia, "titulo": titulo, "fecha_entrega": fecha_entrega, "destinatario": destinatario, "estado": estado})
        elif accion == 'actualizar':
            tarea_id = int(request.form.get('tarea_id', 0))
            nuevo_estado = request.form.get('nuevo_estado')
            for t in tareas_db:
                if t["id"] == tarea_id:
                    t["estado"] = nuevo_estado
                    break

    if tipo == 'Alumno' or tipo == 'Padre de familia':
        target_nombre = hijo if hijo else usuario
        tareas_filtradas = [t for t in tareas_db if t.get('destinatario') == 'Grupo General' or t.get('destinatario') == target_nombre]
    else:
        tareas_filtradas = tareas_db

    alumnos_lista = list(calificaciones_db.keys())
    return render_template('tareas.html', usuario=usuario, tipo=tipo, hijo=hijo, materia=materia, tareas=tareas_filtradas, alumnos_lista=alumnos_lista)

@app.route('/calendario', methods=['GET', 'POST'])
def calendario():
    usuario = request.args.get('usuario', 'Usuario')
    tipo = request.args.get('tipo', 'Alumno')
    hijo = request.args.get('hijo', '')
    materia = request.args.get('materia', '')

    for correo, datos in usuarios_db.items():
        if datos["nombre"] == usuario:
            tipo = datos["tipo"]
            if datos["materia"]:
                materia = datos["materia"]
            if datos["hijo"]:
                hijo = datos["hijo"]
            break

    if request.method == 'POST':
        accion = request.form.get('accion')
        if accion == 'crear' and (tipo == 'Administrativo' or tipo == 'Docente'):
            evento = request.form.get('evento')
            fecha = request.form.get('fecha')
            estado = request.form.get('estado', 'Pendiente')
            if evento and fecha:
                nuevo_id = len(calendario_db) + 1
                calendario_db.append({"id": nuevo_id, "evento": evento, "fecha": fecha, "estado": estado})
        elif accion == 'actualizar':
            evento_id = int(request.form.get('evento_id', 0))
            nuevo_estado = request.form.get('nuevo_estado')
            for ev in calendario_db:
                if ev["id"] == evento_id:
                    ev["estado"] = nuevo_estado
                    break

    dias_con_eventos = [item["fecha"] for item in calendario_db]

    return render_template('calendario.html', usuario=usuario, tipo=tipo, hijo=hijo, materia=materia, calendario=calendario_db, dias_con_eventos=dias_con_eventos)

@app.route('/reportes', methods=['GET', 'POST'])
def reportes():
    usuario = request.args.get('usuario', 'Usuario')
    tipo = request.args.get('tipo', 'Alumno')
    hijo = request.args.get('hijo', '')
    materia = request.args.get('materia', '')

    for correo, datos in usuarios_db.items():
        if datos["nombre"] == usuario:
            tipo = datos["tipo"]
            if datos["materia"]:
                materia = datos["materia"]
            if datos["hijo"]:
                hijo = datos["hijo"]
            break

    if request.method == 'POST' and tipo == 'Docente':
        alumno_sel = request.form.get('alumno_sel')
        motivo = request.form.get('motivo')
        fecha = request.form.get('fecha')
        if alumno_sel and motivo and fecha:
            reportes_db.append({"alumno": alumno_sel, "docente": usuario, "motivo": motivo, "fecha": fecha})

    if tipo == 'Padre de familia' or tipo == 'Alumno':
        lista_reportes = [r for r in reportes_db if r["alumno"] == hijo]
    else:
        lista_reportes = reportes_db

    return render_template('reportes.html', usuario=usuario, tipo=tipo, hijo=hijo, materia=materia, reportes=lista_reportes, alumnos_lista=list(calificaciones_db.keys()))

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    usuario = request.args.get('usuario', 'Usuario')
    tipo = request.args.get('tipo', 'Administrativo')
    
    if request.method == 'POST':
        correo_editar = request.form.get('correo_editar')
        nuevo_nombre = request.form.get('nuevo_nombre')
        nuevo_tipo = request.form.get('nuevo_tipo')
        if correo_editar in usuarios_db:
            usuarios_db[correo_editar]["nombre"] = nuevo_nombre
            usuarios_db[correo_editar]["tipo"] = nuevo_tipo

    return render_template('usuarios.html', usuario=usuario, tipo=tipo, usuarios_db=usuarios_db)

@app.route('/notificaciones')
def notificaciones():
    usuario = request.args.get('usuario', 'Usuario')
    tipo = request.args.get('tipo', 'Alumno')
    hijo = request.args.get('hijo', '')
    materia = request.args.get('materia', '')

    for correo, datos in usuarios_db.items():
        if datos["nombre"] == usuario:
            tipo = datos["tipo"]
            if datos["hijo"]:
                hijo = datos["hijo"]
            break

    notifs = [
        {"tipo": "Aviso", "mensaje": "Nuevo aviso escolar publicado: Reunion General de Padres."},
        {"tipo": "Falta", "mensaje": f"Se registro una falta o incidencia reciente para {hijo if hijo else 'el alumno'}."},
        {"tipo": "Reporte", "mensaje": "Se emitio un nuevo reporte de conducta que requiere atencion."}
    ]

    return render_template('notificaciones.html', usuario=usuario, tipo=tipo, hijo=hijo, materia=materia, notificaciones=notifs)

@app.route('/respaldo')
def respaldo():
    data = {
        "usuarios": usuarios_db,
        "calificaciones": calificaciones_db,
        "asistencias": asistencias_db,
        "reportes": reportes_db,
        "avisos": avisos_db,
        "tareas": tareas_db
    }
    return json.dumps(data, ensure_ascii=False, indent=4), 200, {'Content-Type': 'application/json; charset=utf-8', 'Content-Disposition': 'attachment; filename=respaldo_tutorconecta.json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)