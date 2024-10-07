from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações de acesso ao MySQL
app.config.update(
    MYSQL_HOST='localhost',       # Servidor do MySQL
    MYSQL_USER='root',            # Usuário do MySQL
    MYSQL_PASSWORD='',            # Senha do MySQL
    MYSQL_DB='tarefaspydb',           # Nome da base de dados
    MYSQL_CURSORCLASS='DictCursor'  # Retorna dados como DICT
)

# Variável de conexão com o MySQL
mysql = MySQL(app)

# Configura a conexão com o MySQL para usar utf8mb4 e português do Brasil


@app.before_request
def before_request():
    cur = mysql.connection.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute("SET character_set_client=utf8mb4")
    cur.execute("SET character_set_results=utf8mb4")
    cur.execute("SET lc_time_names = 'pt_BR'")
    cur.close()


# Rota padrão
@app.route('/')
def home():
    page = {
        'href': '/new',
        'label': 'Nova tarefa'
    }
    return render_template('home.html', page=page)


# Rota para um nova tarefa
@app.route('/new', methods=['GET', 'POST'])
def new():

    created = False

    form = dict(request.form)

    # Para debug
    # print('\n\n\n', form, '\n\n\n')

    if form['expire'] == '':
        subquery = 'DATE_ADD(NOW(), INTERVAL 30 DAY)'
    else:
        subquery = form['expire'].replace('T', ' ')

    sql = '''
            -- Com o campo tipo number
            INSERT INTO task (name, description, expire)
            VALUES (%s, %s, %s));
        '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (form['name'], form['description'], subquery,))
    mysql.connection.commit()
    cur.close()
    
    created = True

    page = {
        'href': '/',
        'label': 'Ver as tarefas',
        'created': created
    }
    return render_template('new_task.html', page=page)


# Rota para tratamento de erro 404
@app.errorhandler(404)
def page_not_found(e):
    # Renderiza um template de erro 404
    return f"Mensagem: {e}", 404
    # return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
