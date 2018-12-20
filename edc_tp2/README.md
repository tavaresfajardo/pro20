Para executar a aplicação é necessário os pacotes django, s4api e requests. 
É também necessário uma instancia de graphDB iniciado na porta 7200 com os dados importados para o repositório 'Guns'
O ficheiro para a criação de dados na base de dados encontra-se no diretório preprocess com o nome storage.nt
Podem ser gerados diferentes datasets aleatórios executando o ficheiro CreateDatabase.py no mesmo diretório

Depois é so executar 'python3 manage.py runserver'