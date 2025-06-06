-- Script de criação do banco de dados para o projeto Perfilador

CREATE TABLE crawler_execucoes (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    search_query         TEXT,
    start_time           TEXT NOT NULL,
    end_time             TEXT,
    total_arquivos       INTEGER DEFAULT 0,
    successful_downloads INTEGER DEFAULT 0,
    failed_downloads     INTEGER DEFAULT 0,
    duration_seconds     REAL
);

CREATE TABLE documentos (
    id                    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name                  TEXT NOT NULL,
    path                  TEXT NOT NULL,
    content               TEXT,
    clean                 TEXT,
    normalized            TEXT,
    pages                 TEXT,
    pipeline_executed     INTEGER DEFAULT 0,
    information_extracted INTEGER DEFAULT 0,
    hash                  TEXT NOT NULL UNIQUE,
    crawler_execucao_id   INTEGER REFERENCES crawler_execucoes(id),
    source_url            TEXT,
    search_query          TEXT,
    download_timestamp    DATETIME
);

CREATE TABLE enderecos (
    id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    logradouro TEXT,
    numero     TEXT,
    cidade     TEXT,
    bairro     TEXT,
    cep        TEXT,
    uf         TEXT
);

CREATE TABLE identidades (
    id               INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome             TEXT,
    cpf              TEXT,
    rg               TEXT,
    rg_orgao_emissor TEXT,
    data_nascimento  INTEGER,
    email            INTEGER,
    telefone         INTEGER,
    documento_id     INTEGER NOT NULL REFERENCES documentos(id),
    endereco_id      INTEGER REFERENCES enderecos(id)
);
