
import psycopg2
import sqlite3

USAR_SQLITE = False

def usar_sqlite():
    global USAR_SQLITE
    USAR_SQLITE = True

def usar_postgres():
    global USAR_SQLITE
    USAR_SQLITE = False

def conectar():
    if USAR_SQLITE:
        conn = sqlite3.connect("livros.db")
        conn.row_factory = sqlite3.Row
        return conn
    else:
        return psycopg2.connect(
            host="localhost",
            database="livros",
            user="postgres",
            password="Sun@09072018"
        )

def inicializar_sqlite_se_necessario():
    conn = conectar()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS autor (
        codigo INTEGER PRIMARY KEY,
        nome TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS livros (
        codigo INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS edicao (
        codigolivro INTEGER,
        numero TEXT,
        ano INTEGER,
        PRIMARY KEY (codigolivro, numero)
    );

    CREATE TABLE IF NOT EXISTS livroautor (
        codigolivro INTEGER,
        codigoautor INTEGER,
        PRIMARY KEY (codigolivro, codigoautor)
    );
    """)

    cursor.execute("SELECT COUNT(*) FROM livros")
    count = cursor.fetchone()[0]
    if count == 0:
        usar_postgres()
        livros = listar_livros_completos()
        usar_sqlite()
        for livro in livros:
            print(livro)
            cursor.execute("INSERT OR IGNORE INTO livros (codigo, titulo) VALUES (?, ?)", (int(livro['codigo']), livro['titulo']))
            if livro['edicao'] and livro['ano']:
                cursor.execute("INSERT OR IGNORE INTO edicao (codigolivro, numero, ano) VALUES (?, ?, ?)",
                               (int(livro['codigo']), livro['edicao'], livro['ano']))
            if livro['autor_id'] and livro['autor_nome']:
                cursor.execute("INSERT OR IGNORE INTO autor (codigo, nome) VALUES (?, ?)", (int(livro['autor_id']), livro['autor_nome']))
                cursor.execute("INSERT OR IGNORE INTO livroautor (codigolivro, codigoautor) VALUES (?, ?)",
                               (int(livro['codigo']), int(livro['autor_id'])))

        conn.commit()

    cursor.close()
    conn.close()

def listar_livros():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, titulo FROM livros ORDER BY titulo")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    print(dados[0])
    if USAR_SQLITE:
        lista = []
        for row in dados:
            lista.append((row["codigo"], row["titulo"]))
        return lista
    return dados

def listar_livros_completos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.codigo, l.titulo, e.numero AS edicao, e.ano, a.codigo as autor_id, a.nome AS autor_nome
        FROM livros l
        LEFT JOIN edicao e ON e.codigolivro = l.codigo
        LEFT JOIN livroautor la ON la.codigolivro = l.codigo
        LEFT JOIN autor a ON a.codigo = la.codigoautor
    """)
    dados = cursor.fetchall()
    colunas = []
    for desc in cursor.description:
        colunas.append(desc[0])
    cursor.close()
    conn.close()
    livros = []
    for row in dados:
        livros.append(dict(zip(colunas, row)))
    return livros

def buscar_detalhes(offset, limite, letra=None, busca=None):
    conn = conectar()
    cursor = conn.cursor()

    base = """
        SELECT l.codigo, l.titulo, e.numero, e.ano, a.nome
        FROM livros l
        LEFT JOIN edicao e ON e.codigolivro = l.codigo
        LEFT JOIN livroautor la ON la.codigolivro = l.codigo
        LEFT JOIN autor a ON a.codigo = la.codigoautor
    """

    condicoes = []
    valores = []

    if letra and letra != "Todos":
        if USAR_SQLITE:
            condicoes.append("l.titulo LIKE ? COLLATE NOCASE")
        else:
            condicoes.append("l.titulo ILIKE %s")
        valores.append(f"{letra}%")

    if busca:
        if str(busca).isdigit():
            if USAR_SQLITE:
                condicoes.append("l.codigo = ?")
            else:
                condicoes.append("l.codigo = %s")
            valores.append(int(busca))
        else:
            if USAR_SQLITE:
                condicoes.append("(l.titulo LIKE ? COLLATE NOCASE OR a.nome LIKE ? COLLATE NOCASE)")
            else:
                condicoes.append("(l.titulo ILIKE %s OR a.nome ILIKE %s)")
            valores.extend([f"%{busca}%", f"%{busca}%"])

    if condicoes:
        base += " WHERE " + " AND ".join(condicoes)

    if USAR_SQLITE:
        base += " ORDER BY l.titulo LIMIT ? OFFSET ?"
    else:
        base += " ORDER BY l.titulo LIMIT %s OFFSET %s"
    valores.extend([limite, offset])
    print(base, valores)
    cursor.execute(base, valores)
    dados = cursor.fetchall()
    colunas = []
    for desc in cursor.description:
        colunas.append(desc[0])

    cursor.close()
    conn.close()

    resultado = []
    for row in dados:
        if not USAR_SQLITE:
            resultado.append(tuple(row))
        else:
            valores = []
            for col in colunas:
                valores.append(row[col])
            resultado.append(tuple(valores))

    return resultado
