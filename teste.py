import couchdb
import json

# Conectar ao servidor CouchDB
couch = couchdb.Server('http://music_admin:fib01123@localhost:5984/')

# Escolher ou criar um banco de dados
db_name = 'esquema_vinicola'
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

# Dados das tabelas
regioes = [
    {"regiaoID": "R1", "nomeRegiao": "Vale S. Francisco", "estadoRegiao": "Pernambuco"},
    {"regiaoID": "R2", "nomeRegiao": "Zona da Mata", "estadoRegiao": "Pernambuco"},
    {"regiaoID": "R3", "nomeRegiao": "Garibaldi", "estadoRegiao": "Rio Grande do Sul"},
    {"regiaoID": "R4", "nomeRegiao": "Gramado", "estadoRegiao": "Rio Grande do Sul"}
]

vinicolas = [
    {"vinicolaID": 1, "nomeVinciola": "A1", "foneVinicola": 1234, "regiaoID": "R1"},
    {"vinicolaID": 2, "nomeVinciola": "A2", "foneVinicola": 5234, "regiaoID": "R1"},
    {"vinicolaID": 3, "nomeVinciola": "A3", "foneVinicola": 6234, "regiaoID": "R2"},
    {"vinicolaID": 4, "nomeVinciola": "A4", "foneVinicola": 7234, "regiaoID": "R2"},
    {"vinicolaID": 5, "nomeVinciola": "A5", "foneVinicola": 8234, "regiaoID": "R3"}
]

vinhos = [
    {"vinhoID": 10, "nomeVinho": "V1", "tipoVinho": "tinto", "precoVinho": 100.00, "vinicolaID": 1},
    {"vinhoID": 20, "nomeVinho": "V2", "tipoVinho": "branco", "precoVinho": 200.00, "vinicolaID": 1},
    {"vinhoID": 30, "nomeVinho": "V3", "tipoVinho": "rose", "precoVinho": 300.00, "vinicolaID": 1},
    {"vinhoID": 40, "nomeVinho": "V4", "tipoVinho": "rose", "precoVinho": 350.00, "vinicolaID": 2},
    {"vinhoID": 50, "nomeVinho": "V5", "tipoVinho": "branco", "precoVinho": 250.00, "vinicolaID": 2},
    {"vinhoID": 60, "nomeVinho": "V6", "tipoVinho": "tinto", "precoVinho": 150.00, "vinicolaID": 2},
    {"vinhoID": 70, "nomeVinho": "V7", "tipoVinho": "tinto", "precoVinho": 397.00, "vinicolaID": 3},
    {"vinhoID": 80, "nomeVinho": "V8", "tipoVinho": "branco", "precoVinho": 333.00, "vinicolaID": 3}
]

# Estrutura do JSON
dados_json = {
    "regioes": regioes,
    "vinicolas": vinicolas,
    "vinhos": vinhos
}

# Escrever os dados em um arquivo JSON
with open('dados.json', 'w') as arquivo_json:
    json.dump(dados_json, arquivo_json, indent=4)

#db.save(dados_json)
    
# Enviar cada linha como um documento individual para o banco de dados
for tabela, linhas in dados_json.items():
    for linha in linhas:
        db.save(linha)