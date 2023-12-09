# ConexãoIF

```virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
Ctrl + C

Cria o banco "models" com id "postgres" e senha "123" ou então modifica no arquivo "app.py"

flask db init
flask run
Ctrl + C
flask db migrate -m "Models and Resources"
flask db upgrade
flask run

npm install react-select
npm install uuid


#Endereco
{ "rua": "BR 101 Guarabira", 
    "bairro": "Nordeste I", 
    "cep": "58200-000", 
    "numero": "Sem Número", 
    "complemento": "Saída de Guarabira a Araçagi"
}
#Periodo
{ 
    "semestrereferencia": "1º Período"
}
{ 
    "semestrereferencia": "2º Período"
}
{ 
    "semestrereferencia": "3º Período"
}
{ 
    "semestrereferencia": "4º Período"
}
{ 
    "semestrereferencia": "5º Período"
}
{ 
    "semestrereferencia": "6º Período"
}
#Instiuicao
{ 
    "nome": "Instituto Federal da Paraíba(IFPB) - Campus Guarabira - PB",
    "endereco": {"id": 1}
}
#Curso 
{ 
    "nome": "Tecnologia em Sistemas para Internet", 
    "instituicao": {"id": 1}
}
{ 
    "nome": "Gestão Comercial", "instituicao": {"id": 1}
}
#Pessoa
{ 
    "nome": "Renan",
    "email": "Renan@gmail.com",
    "senha": "renan", 
    "telefone": "(83)9 9988-8899"
}
#Aluno
{ 
    "nome": "renanthierry",
    "email": "rennan-thierry@academico.ifpb.edu.br", 
    "senha": "renanthierry",
    "telefone": "(83)9 9988-8899",
    "matricula": "20210001", 
    "periodo": {"id": 1}, 
    "curso": {"id": 1}
}
#Professor
{ 
    "nome": "Rhavy Maia", 
    "email": "rhavyy.maia@academico.ifpb.edu.br", 
    "senha": "rhavyymaia", 
    "telefone": "(83)9 8877-6655", 
    "disciplina": "Programação Web II", 
    "curso": {"id": 1}
}
#Coordenador
{ 
    "nome": "Otacílio", 
    "email": "otacilio@academico.ifpb.edu.br", 
    "senha": "otacilio", 
    "telefone": "(83)9 9889-7667", 
    "disciplina": "Ciência de Dados", 
    "registrodeTrabalho": "0001.1025", 
    "curso": {"id": 1}
}
#Grupo
{ 
    "titulo": "Grupo do Whatsapp - 5º Período", 
    "link": "whatsappweb.com.br", 
    "mensagem": "Bem vindo!Clique no link para entrar.", 
    "periodo": {"id": 5}, 
    "coordenador": {"id": 3}
}