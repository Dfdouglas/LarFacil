CREATE DATABASE larfacil;
USE larfacil;

CREATE TABLE locador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    email VARCHAR(255),
    telefone VARCHAR(15)
);



	CREATE TABLE locatario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    email VARCHAR(255),
    telefone VARCHAR(15),
    status_aluguel BOOLEAN DEFAULT FALSE
);


CREATE TABLE imoveis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(255),
    endereco VARCHAR(255),
    valor_aluguel DECIMAL(10, 2),
    locador_id INT,
    status_aluguel BOOLEAN DEFAULT FALSE,  -- Indica se o imóvel está alugado ou não
    FOREIGN KEY (locador_id) REFERENCES locador(id)
);


CREATE TABLE aluguel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    imovel_id INT,
    locatario_id INT,
    data_inicio DATE,
    data_fim DATE,
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id),
    FOREIGN KEY (locatario_id) REFERENCES locatario(id)
);