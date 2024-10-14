from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from datetime import datetime, timedelta

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Configurações de acesso ao MySQL
app.config.update(
    MYSQL_HOST='localhost',       # Servidor do MySQL
    MYSQL_USER='root',            # Usuário do MySQL
    MYSQL_PASSWORD='',            # Senha do MySQL
    MYSQL_DB='tarefaspydb',      # Nome da base de dados
    MYSQL_CURSORCLASS='DictCursor',  # Retorna dados como dicionário
    MYSQL_CHARSET='utf8mb4',     # Transações em UTF-8
    MYSQL_USE_UNICODE=True        # Usa a conversão unicode para caracteres
)

# Variável de conexão com o MySQL
mysql = MySQL(app)

# Configura a conexão com o MySQL para usar utf8mb4 e português do Brasil


@app.before_request
def before_request():
    cur = mysql.connection.cursor()  # Cria um cursor para executar comandos
    # Define a configuração de charset e localidade
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute("SET character_set_client=utf8mb4")
    cur.execute("SET character_set_results=utf8mb4")
    # Define a localidade para português do Brasil
    cur.execute("SET lc_time_names = 'pt_BR'")
    cur.close()  # Fecha o cursor


# Rota padrão que exibe as tarefas
@app.route('/')
def home():
    # Obtém um parâmetro de consulta 'ac' da URL
    action = request.args.get('ac')

    sql = '''
        SELECT id, name, description, expire, status,
        DATE_FORMAT(expire, '%d/%m/%Y às %H:%i') AS expirebr 
        FROM task
        WHERE status = 'pen' OR status = 'com'
        ORDER BY expire,status ASC;
    '''  # Consulta para obter tarefas pendentes ou completas

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql)  # Executa a consulta
    mysql.connection.commit()  # Confirma a transação
    task = cur.fetchall()  # Obtém todos os resultados
    cur.close()  # Fecha o cursor

    page = {
        'label': 'Nova tarefa',  # Rótulo para a página
        'tasks': task,           # Lista de tarefas
        'action': action         # Ação para mostrar na interface
    }
    # Renderiza o template 'home.html' com os dados
    return render_template('home.html', page=page)


# Rota para criar uma nova tarefa
@app.route('/new', methods=['GET', 'POST'])
def new():
    created = False  # Flag para verificar se a tarefa foi criada

    if request.method == 'POST':  # Verifica se o método é POST
        # Converte os dados do formulário em um dicionário
        form = dict(request.form)

        # Define a data de expiração
        if form['expire'] == '':
            # Se não for especificado, adiciona 30 dias
            subquery = 'DATE_ADD(NOW(), INTERVAL 30 DAY)'
        else:
            # Substitui 'T' por espaço para formato de data
            subquery = form['expire'].replace('T', ' ')

        sql = '''
            INSERT INTO task (name, description, expire)
            VALUES (%s, %s, %s);
        '''  # Consulta para inserir uma nova tarefa

        cur = mysql.connection.cursor()  # Cria um cursor
        # Executa a inserção
        cur.execute(sql, (form['name'], form['description'], subquery,))
        mysql.connection.commit()  # Confirma a transação
        cur.close()  # Fecha o cursor

        created = True  # Atualiza a flag para verdadeiro

    # Obtém a data atual
    data_atual = datetime.now()
    # Adiciona 30 dias à data atual
    data_futura = data_atual + timedelta(days=30)
    # Formata a data no formato desejado
    data_formatada = data_futura.strftime('%Y-%m-%d %H:%M:%S')

    page = {
        'label': 'Ver tarefas',  # Rótulo para a página
        'created': created,      # Indica se uma tarefa foi criada
        'date30': data_formatada  # Data formatada para exibição
    }

    # Renderiza o template 'new_task.html' com os dados
    return render_template('new_task.html', page=page)

# Rota para deletar uma tarefa


@app.route('/del/<taskid>')
def delete(taskid):
    sql = '''
        UPDATE task SET status = 'del' WHERE id = %s;        
    '''  # Consulta para marcar a tarefa como deletada

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, (taskid,))  # Executa a atualização
    mysql.connection.commit()  # Confirma a transação
    cur.close()  # Fecha o cursor

    # Redireciona para a página principal com um parâmetro de ação
    return redirect(url_for('home', ac='del'))

# Rota para marcar uma tarefa como pendente
@app.route('/pen/<taskid>')
def pending(taskid):
    sql = '''
        UPDATE task SET status = 'pen' WHERE id = %s;        
    '''  # Consulta para marcar a tarefa como pendente

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, (taskid,))  # Executa a atualização
    mysql.connection.commit()  # Confirma a transação
    cur.close()  # Fecha o cursor

    # Redireciona para a página principal com um parâmetro de ação
    return redirect(url_for('home', ac='pen'))

# Rota para marcar uma tarefa como completa
@app.route('/com/<taskid>')
def complete(taskid):
    sql = '''
        UPDATE task SET status = 'com' WHERE id = %s;        
    '''  # Consulta para marcar a tarefa como completa

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, (taskid,))  # Executa a atualização
    mysql.connection.commit()  # Confirma a transação
    cur.close()  # Fecha o cursor

    # Redireciona para a página principal com um parâmetro de ação
    return redirect(url_for('home', ac='com'))


@app.route('/edit/<taskid>', methods=['GET', 'POST'])
def edit(taskid):

    if not taskid.isdigit():
        return page_not_found(404)

    # Se o formulário foi enviado
    if request.method == 'POST':

        # Dados vindos do formulário pelo POST
        form = dict(request.form)

        sql = '''
            UPDATE task 
            SET
                name = %s,
                description = %s,
                expire = %s
            WHERE id = %s 
            '''

        cur = mysql.connection.cursor()
        cur.execute(sql, (form['name'], form['description'], form['expire'], taskid,) )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('home', ac='edit'))

    else: 

        sql = '''
            SELECT * 
            FROM task
            WHERE id = %s AND status != 'deleted'
        '''

        # Debug
        # print('\n\n\n', sql, '\n\n\n')

        cur = mysql.connection.cursor()
        cur.execute(sql, (taskid,))
        task = cur.fetchone()
        cur.close()

        if task == None:
            return page_not_found(404)

    page = {
        'task': task
    }

    return render_template('edit.html', page=page)


# Rota para tratamento de erro 404
@app.errorhandler(404)
def page_not_found(e):
    return f"Mensagem: {e}", 404  # Retorna uma mensagem de erro 404
    # return render_template('404.html'), 404  # Alternativa para renderizar uma página de erro


# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)  # Inicia a aplicação em modo de depuração
