import sqlite3 # Importa a biblioteca para trabalhar com banco de dados SQLite
import time    # Importa a biblioteca para usar pausas no tempo (time.sleep)


# Conexão com o banco de dados
# Cria ou se conecta a um arquivo de banco de dados chamado "db_tarefa".
conn = sqlite3.connect("db_tarefa") 
# Cria um cursor, que permite executar comandos SQL no banco de dados.
cursor = conn.cursor()

# Criação da tabela de tarefas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tb_tarefas (
    id_tarefa INTEGER PRIMARY KEY AUTOINCREMENT,
    nm_tarefa TEXT,
    nm_descricao TEXT,
    bol_status TEXT CHECK(bol_status IN ('Pendente', 'Concluido')),
    dt_criacao DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

""")
# - `CREATE TABLE IF NOT EXISTS`: Cria a tabela `tb_tarefas` apenas se ela ainda não existir.
# - `id_tarefa INTEGER PRIMARY KEY AUTOINCREMENT`: Define um ID único para cada tarefa, que é gerado automaticamente.
# - `nm_tarefa TEXT`: Coluna para o nome da tarefa (texto).
# - `nm_descricao TEXT`: Coluna para a descrição (texto).
# - `bol_status TEXT CHECK(...)`: Coluna para o status, que só pode ser 'Pendente' ou 'Concluido'.
# - `dt_criacao DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL`: Coluna para a data e hora de criação, preenchida automaticamente.

#-----------------------------------------------------------#

# Definição da função do menu principal
def menu_show():
    # Loop infinito para manter o menu ativo até que o usuário decida sair
    while True:
        # Exibe o menu principal com as opções
        print("=" * 40)
        print("📋  GERENCIADOR DE TAREFAS".center(40))
        print("=" * 40)
        print("1️⃣  Adicionar nova tarefa")
        print("2️⃣  Listar tarefas")
        print("3️⃣  Sair do programa")
        print("=" * 40)
        
        # Pede ao usuário para escolher uma opção
        escolha = int(input("Escolha uma opção: "))
        
        # Opção 1: Adicionar nova tarefa
        if escolha == 1:
            nmT = input("Nomeie sua tarefa: ")
            descT = input("Adicione uma descrição (Opcional): ")
            status = "Pendente"
            # Executa o comando SQL para inserir uma nova tarefa na tabela
            cursor.execute("INSERT INTO tb_tarefas (nm_tarefa, nm_descricao, bol_status) VALUES (?, ?, ?)", (nmT, descT, status))
            print("Criando...")
            time.sleep(3) # Pausa a execução por 3 segundos
            print(f"🎉Tarefa {nmT} criada com sucesso!🥳")
            time.sleep(1) # Pausa a execução por 1 segundo
            conn.commit() # Salva as mudanças no banco de dados
        
        # Opção 2: Listar tarefas
        elif escolha == 2:
            
            # Seleciona todos os dados da tabela de tarefas
            cursor.execute("select * from tb_tarefas where bol_status = 'Pendente'")
            resultado = cursor.fetchall() # Obtém todos os resultados da consulta
            
            # Exibe o submenu de tarefas
            print("=" * 40)
            print("🕵️  Suas tarefas".center(40))
            print("=" * 40)
            
            # Sub-loop para o menu de gerenciamento de tarefas
            while True:
                line = False
                titulos = ["ID", "Tarefa", "Descrição", "Status", "Data de Criação"]
                print("\n")
                print(" | ".join(titulos))
                print("-" * 60)
                # Itera sobre os resultados e imprime cada tarefa
                for linha in resultado:
                    print(" | ".join(str(valor) for valor in linha))
                    line = True
                
                # Se não houver tarefas, exibe uma mensagem
                if not line:
                    print("\n😪Sem tarefas no momento😴".center(40))
                    print("Volte para o menu principal para criar uma nova tarefa\n".center(40))
                    
                # Exibe as opções de gerenciamento de tarefas
                print("\n")
                print("=" * 40)         
                print("1️⃣  Concluir uma tarefa")
                print("2️⃣  Editar tarefa")
                print("3️⃣  Excluir tarefa")
                print(" 4 - Mostrar as concluidas")
                print(" 5 - Mostrar as pendentes")
                print(" E - Voltar para o menu principal")
                print("=" * 40)
            
                escolha = input("Escolha uma opção: ")
                
                # Se a escolha for 'E', sai do sub-loop e volta para o menu principal
                if escolha.upper() == "E":
                    break
                
                # Opção 1 do sub-menu: Concluir tarefa
                elif escolha == "1":
                    idT = input("Digite o código da tarefa que deseja finalizar: ")
                    try:
                        # Tenta atualizar o status da tarefa para 'Concluido'
                        cursor.execute("update tb_tarefas set bol_status = 'Concluido' where id_tarefa = ?;", (idT))
                        print("Tarefa concluida com sucesso.")
                        time.sleep(2)
                        conn.commit()
                        break # Sai do sub-loop após a conclusão
                    except:
                        # Exibe uma mensagem de erro se a tarefa não for encontrada
                        print("Tarefa não encontrada")
                
                # Opção 2 do sub-menu: Editar tarefa
                elif escolha == "2":
                    idT = input("Digite o código da tarefa que deseja editar: ")
                    try:
                        print("(Deixe vazio caso não queira editar)")
                        nmTnovo = input("Digite o novo nome da sua tarefa: ")
                        
                        print("(Deixe vazio caso não queira editar)")
                        descNovo = input("Digite a nova descrição: ")
                        
                        # Verifica se tanto o nome quanto a descrição foram fornecidos
                        if nmTnovo != "" and descNovo != "":
                            cursor.execute("update tb_tarefas set nm_tarefa = ?, nm_descricao = ? where id_tarefa = ?;", (nmTnovo, descNovo, idT))
                            print("Tarefa editada com sucesso!")
                            time.sleep(2)
                            conn.commit()
                            break
                        # Verifica se apenas a descrição foi fornecida
                        elif nmTnovo == "" and descNovo != "":
                            cursor.execute("update tb_tarefas set nm_descricao = ? where id_tarefa = ?;", (descNovo, idT))
                            print("Tarefa editada com sucesso!")
                            time.sleep(2)
                            conn.commit()
                            break
                        # Verifica se apenas o nome foi fornecido
                        elif nmTnovo != "" and descNovo == "":
                            cursor.execute("update tb_tarefas set nm_tarefa = ? where id_tarefa = ?;", (nmTnovo, idT))
                            print("Tarefa editada com sucesso!")
                            time.sleep(2)
                            conn.commit()
                            break
                    except:
                        print("Tarefa não encontrada")
               
                    
                # Opção 3 do sub-menu: Excluir tarefa
                elif escolha == "3":
                    idT = input("Digite o código da tarefa que deseja excluir: ")
                    try:
                        # Tenta excluir a tarefa com o ID fornecido
                        cursor.execute("delete from tb_tarefas where id_tarefa = ?;", (idT))
                        print("Tarefa excluida com sucesso.")
                        time.sleep(2)
                        conn.commit()
                        break
                    except:
                        print("Tarefa não encontrada")
                elif escolha == "4":
                    cursor.execute("select * from tb_tarefas where bol_status = 'Concluido'")
                    resultado = cursor.fetchall() # Obtém todos os resultados da consulta
                elif escolha == "5":
                    cursor.execute("select * from tb_tarefas where bol_status = 'Pendente'")
                    resultado = cursor.fetchall() # Obtém todos os resultados da consulta
                    
                
                # Lida com opções inválidas no sub-menu
                else:
                    print("Opção invalida, tente novamente.")
        
        # Opção 3: Sair do programa
        elif escolha == 3:
            print("Tchau tchau!")
            break # Sai do loop principal, encerrando o programa
        
        # Lida com opções inválidas no menu principal
        else:
            print("Opção invalida, tente novamente.")

# Executa a função do menu para iniciar o programa
menu_show()

# Fecha a conexão com o banco de dados ao final do programa
conn.close()