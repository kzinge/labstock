CREATE DATABASE db_labstock;
use db_labstock;

CREATE TABLE tb_categorias (
    cat_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cat_nome VARCHAR(50) NOT NULL
);

CREATE TABLE tb_usuarios (
	usu_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    usu_matricula VARCHAR(20) NOT NULL UNIQUE,
    usu_nome VARCHAR(100) NOT NULL,
    usu_email VARCHAR(150) NOT NULL UNIQUE,
    usu_tipo VARCHAR(150) NOT NULL,
    usu_foto VARCHAR(200)
);

CREATE TABLE tb_laboratorios (
    lab_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    lab_nome VARCHAR(50) NOT NULL,
    lab_local VARCHAR(50) NOT NULL,
    lab_capacidade INT NOT NULL,
    lab_especialidade ENUM('Química', 'Biologia')
);

CREATE TABLE tb_materiais (
    mat_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    mat_nome VARCHAR(50) NOT NULL,
    mat_quantidade DECIMAL(10, 2) NOT NULL,
    mat_unidade ENUM('kg', 'g', 'l', 'ml') NOT NULL,
    mat_fornecedor VARCHAR(90) NOT NULL,
    mat_validade DATE,
    mat_lab_id INT NOT NULL,
    mat_cat_id INT NOT NULL,
    FOREIGN KEY (mat_lab_id) REFERENCES tb_laboratorios(lab_id),
    FOREIGN KEY (mat_cat_id) REFERENCES tb_categorias(cat_id)
);

CREATE TABLE tb_reservas_laboratorios (
    rel_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    rel_data DATETIME NOT NULL,
    rel_motivo TEXT NOT NULL,
    rel_tipo ENUM('Anual', 'Semestral', 'Extraordinária'),
    rel_lab_id INT NOT NULL,
    rel_usu_matricula VARCHAR(20) NOT NULL,
    FOREIGN KEY (rel_usu_matricula) REFERENCES tb_usuarios(usu_matricula),
    FOREIGN KEY (rel_lab_id) REFERENCES tb_laboratorios(lab_id)
);

CREATE TABLE tb_reservas_materiais (
    rem_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    rem_mat_id INT NOT NULL,
    rem_rel_id INT NOT NULL,
    FOREIGN KEY (rem_mat_id) REFERENCES tb_materiais(mat_id),
    FOREIGN KEY (rem_rel_id) REFERENCES tb_reservas_laboratorios(rel_id)
);