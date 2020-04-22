create table combustivel(
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    placa VARCHAR(255) NOT NULL,
    quilometragem VARCHAR(255) NOT NULL,
    qnt_litro VARCHAR(255) NOT NULL,
    val_litro VARCHAR(255) NOT NULL,
    val_total VARCHAR(255) NOT NULL,
    tp_combustivel VARCHAR(255) NOT NULL,
    posto VARCHAR(255) NOT NULL,
    path VARCHAR(255) NOT NULL
);