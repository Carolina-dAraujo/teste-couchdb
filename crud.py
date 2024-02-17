import socket
import couchdb

def conectar():
    """
    Função para conectar ao servidor
    """
    user = 'music_admin'
    password = 'fib01123'
    conn = couchdb.Server(f'http://{user}:{password}@localhost:5984')
    # Não aceita caracteres maiúsculos
    banco = 'esquema_vinicola'

    if banco in conn:
        db = conn[banco]
        return db
    else:
        try:
            db = conn.create(banco)
            return db
        except socket.gaierror as e:
            print(f'Erro ao conectar ao servidor: {e}')
        except couchdb.http.Unauthorized as f:
            print(f'Sem permissão para acessar o servidor: {f}')
        except ConnectionRefusedError as g:
            print(f'Não foi possível conectar ao servidor: {g}')

# 'couchdb' não necessita de procedimentos específicos para finalizar a conexão, uma vez que o mesmo realiza automaticamente

def listar():
    """
    Função para listar os vinhos
    """
    # Definição da conexão
    db = conectar()

    if db:
        if db.info()['doc_count'] > 0:
            print('Listando vinhos ...')
            print('---------------------')
            for doc_id in db:
                doc = db[doc_id]
                # Verificar se o documento tem o campo 'nomeVinho'
                if 'nomeVinho' in doc:
                    print(f"ID: {doc['_id']}")
                    print(f"Rev: {doc['_rev']}")
                    print(f"Nome do Vinho: {doc['nomeVinho']}")
                    print(f"Tipo de Vinho: {doc['tipoVinho']}")
                    print(f"Preço do Vinho: {doc['precoVinho']}")
                    print(f"ID da Vinícola: {doc['vinicolaID']}")
                    print('---------------------')

        else:
            print("Não existem vinhos a serem listados!")
            print('---------------------')
    else:
        print('Não foi possível conectar ao servidor.')
        print('---------------------')


def inserir():
    """
    Função para inserir um vinho
    """ 
    # Definição da conexão 
    db = conectar()

    if db:
        print('Inserindo vinho ...')
        print('---------------------')
        nome = input("Informe o nome do vinho: ")
        tipo = input("Informe o tipo do vinho: ")
        preco = float(input("Informe o preço do vinho: "))
        vinhoID = int(input("Informe o vinhoID: "))
        vinicolaID = int(input("Informe o ID da vinícola: "))

        # Verificar se o vinhoID já existe
        if any(doc.get('vinhoID') == vinhoID for doc in db.view('_all_docs', include_docs=True)):
            print(f"O vinhoID {vinhoID} já está em uso. Por favor, escolha outro.")
            print('---------------------')
            return

        vinho = {'nomeVinho': nome, 'tipoVinho': tipo, 'precoVinho': preco, 'vinhoID': vinhoID, 'vinicolaID': vinicolaID}
        
        res = db.save(vinho)

        if res:
            print(f'O vinho {nome} foi inserido com sucesso')
            print('---------------------')
        else:
            print('Não foi possível inserir o vinho.')
            print('---------------------')
    else:
        print(f'Não foi possível conectar ao servidor.')
        print('---------------------')


def atualizar():
    """
    Função para atualizar um vinho
    """
    # Definição da conexão
    db = conectar()

    if db:
        print('Atualizando vinho ...')
        print('---------------------')

        chave = input('Informe a chave do vinho: ')
        
        try:
            doc = db[chave]

            # Pergunta ao usuário quais atributos ele deseja atualizar
            print("Deixe em branco para manter o valor atual.")
            nome = input('Informe o novo nome do vinho: ').strip()
            id = input("Informe o novo ID do vinho: ").strip()
            tipo = input('Informe o novo tipo do vinho: ').strip()
            preco = input('Informe o novo preço do vinho: ').strip()
            vinhoID = input("Informe o novo ID do vinho: ").strip()
            vinicolaID = input("Informe o novo ID da vinícola: ").strip()

            # Atualiza apenas os atributos que não estão vazios
            if nome:
                doc['nomeVinho'] = nome
            if id:
                doc['vinhoID'] = id
                doc['_id'] = id  # Atualiza o ID do documento também
            if tipo:
                doc['tipoVinho'] = tipo
            if preco:
                doc['precoVinho'] = float(preco)
            if vinhoID:
                doc['vinhoID'] = int(vinhoID)
            if vinicolaID:
                doc['vinicolaID'] = int(vinicolaID)
        
            # Atualiza o documento no banco de dados
            db[doc.id] = doc

            print('O vinho foi atualizado com sucesso.')
            print('---------------------')
        except couchdb.http.ResourceNotFound as e:
            print(f'Não foi possível atualizar o vinho: {e}')
            print('---------------------')
        except couchdb.http.ResourceConflict as e:
            print('Erro ao atualizar o vinho: ID já existente, por favor, escolha outro.')
            print('---------------------')
    else:
        print('Não foi possível conectar ao servidor.')
        print('---------------------')


def deletar():
    """
    Função para deletar um vinho
    """  
    # Definição da conexão
    db = conectar()

    if db:
        print('Deletando vinhos ...')
        print('---------------------')

        chave = input('Informe a chave do vinho: ')

        try:
            db.delete(db[chave])
            print(f'O vinho com a chave {chave} foi deletado com sucesso.')
            print('---------------------')
        except couchdb.http.ResourceNotFound as e:
            print(f'Não foi possível deletar o vinho: {e}.')
            print('---------------------')
    else:
        print('Não foi possível conectar ao servidor.')
        print('---------------------')

def menu():
    """
    Função para gerar o menu inicial
    """
    # Operações disponíveis no menu ('sair' sempre em última posição)
    operacoesTxt = ['Listar vinhos.', 'Inserir vinho.', 'Atualizar vinho.', 'Deletar vinho.', 'Sair.']
    # Extração de nomes das funções correspondentes
    operacoes = [operacao.split()[0].lower() for operacao in operacoesTxt]
    # Formatação de exibição de texto das operações disponíveis no menu
    operacoesTxt = [str(it+1) + ' - ' + operacoesTxt[it] for it in range(0,len(operacoesTxt))]
    
    opcao = 0
    # Loop para seleção de operações no menu pelo usuário
    while(opcao != len(operacoesTxt)):
        #  Prints das operações dispníveis no terminal
        print('=========Gerenciamento de Vinhos==============')
        print('Selecione uma opção: ')
        for operacaoTxt in operacoesTxt:
            print(operacaoTxt)
        # Coleta da operação desejada pelo usuário
        opcao = int(input())
        # Chamada das funções desejadas pelo usuário
        if opcao != len(operacoesTxt):
            globals()[operacoes[opcao-1]]()
        # Encerramento do loop 
        elif opcao == len(operacoesTxt):
                print('*** Saindo ***')
        else:
            print('*** Opção inválida ***')

if __name__ == "__main__":
    menu()

