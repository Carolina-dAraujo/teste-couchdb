import socket
import couchdb

def conectar():
    """
    Função para conectar ao servidor
    """
    user = 'elias'
    password = 'elias123'
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
            for doc in db:
                print(f"ID: {db[doc]['_id']}")
                print(f"Rev: {db[doc]['_rev']}")
                print(f"Nome do Vinho: {db[doc]['nomeVinho']}")
                print(f"Tipo de Vinho: {db[doc]['tipoVinho']}")
                print(f"Preço do Vinho: {db[doc]['precoVinho']}")
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

        vinho = {'nomeVinho': nome, 'tipoVinho': tipo, 'precoVinho': preco}
        
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
            
            nome = input('Informe o novo nome do vinho: ')
            tipo = input('Informe o novo tipo do vinho: ')
            preco = float(input('Informe o novo preço do vinho: '))

            doc['nomeVinho'] = nome
            doc['tipoVinho'] = tipo
            doc['precoVinho'] = preco
            # Atualiza o documento no banco de dados
            db[doc.id] = doc

            print(f'O vinho {nome} foi atualizado com sucesso.')
            print('---------------------')
        except couchdb.http.ResourceNotFound as e:
            print(f'Não foi possível atualizar o vinho: {e}')
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
