from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DB_HOST = "137.184.120.127"
DB_NAME = "sigcon"
DB_USER = "modulo4"
DB_PASS = "modulo4"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = """
    SELECT c.id_casa, c.numero, c.piso, c.area, pr.descripcion, t_pre.nomre_predio, pr.direccion, per.nombres, tp.descripcion, ce.descripcion
    FROM casa AS c
    JOIN predio AS pr ON c.id_predio = pr.id_predio
    JOIN tipo_predio AS t_pre ON pr.id_tipo_predio = t_pre.id_tipo_predio
    JOIN propietario AS pro ON c.id_casa = pro.id_casa
    JOIN persona AS per ON pro.id_persona = per.id_persona
    LEFT JOIN mascota AS mas ON c.id_casa = mas.id_casa
    LEFT JOIN tipo_mascota AS tp ON mas.id_tipo_mascota = tp.id_tipo_mascota
    JOIN casa_estado AS ce ON c.id_estado = ce.id_estado
    """

    cur.execute(s) # Execute the SQL
    datos = cur.fetchall()
    return render_template('index.html', datos=datos)

@app.route('/', methods=['POST'])
def index_post():
    tipo_predio = request.form.get('tipo_predio')

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    s = """
    SELECT c.id_casa, c.numero, c.piso, c.area, pr.descripcion,t_pre.nomre_predio, pr.direccion, per.nombres, tp.descripcion, ce.descripcion
    FROM casa AS c
    JOIN predio AS pr ON c.id_predio = pr.id_predio
    JOIN tipo_predio AS t_pre ON pr.id_tipo_predio = t_pre.id_tipo_predio
    JOIN propietario AS pro ON c.id_casa = pro.id_casa
    JOIN persona AS per ON pro.id_persona = per.id_persona
    LEFT JOIN mascota AS mas ON c.id_casa = mas.id_casa
    LEFT JOIN tipo_mascota AS tp ON mas.id_tipo_mascota = tp.id_tipo_mascota
    JOIN casa_estado AS ce ON c.id_estado = ce.id_estado
    """

    if tipo_predio:
        s += " WHERE t_pre.nomre_predio = %s"
        cur.execute(s, (tipo_predio,))
    else:
        cur.execute(s)

    datos = cur.fetchall()
    
    categorizar = False
    if 'categorizar' in request.form:
        categorizar = True

    return render_template('index.html', datos=datos, categorizar=categorizar)

if __name__ == "__main__":
    app.run(debug=True)
