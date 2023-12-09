from flask import Blueprint, jsonify, request
import os
import json
import tempfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD

api_bp = Blueprint('api', __name__)

# Obtenha o diretório do projeto
project_dir = os.path.dirname(os.path.abspath(__file__))

# Concatene o diretório do projeto com a pasta "bot_email" e o nome do arquivo
file_path = os.path.join(project_dir, 'lista.json')

def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        json_content = file.read()  # Lê o conteúdo do arquivo
        data = json.loads(json_content)  # Faz o parse do conteúdo JSON
        return data

def enviar_email(assunto, mensagem_manual):
    try:
        print(f"Caminho do arquivo JSON: {file_path}")
        emails_data = load_json_from_file(file_path)  # Carrega os dados do arquivo JSON
        emails = emails_data['emails']  # Obtém a lista de emails

        for email_data in emails:
            assunto_email = email_data['titulo']  # Obtém o título do email
            corpo = f"{email_data['link']}\n\n{mensagem_manual}"  # Monta o corpo do email

            mensagem = MIMEMultipart()
            mensagem['From'] = EMAIL_SENDER  # Define o remetente do email
            mensagem['To'] = email_data['email']  # Define o destinatário do email
            mensagem['Subject'] = assunto_email  # Define o assunto do email
            mensagem.attach(MIMEText(corpo, 'plain'))  # Anexa o corpo do email à mensagem

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
                servidor.starttls()  # Inicia a conexão TLS
                servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Realiza o login no servidor SMTP
                servidor.send_message(mensagem)  # Envia a mensagem de email

        return True  # Retorna True se o envio do email foi bem-sucedido
    except Exception as e:
        print(f'Erro ao enviar email: {str(e)}')
        return False  # Retorna False se ocorreu algum erro ao enviar o email

def load_emails():
    try:
        file = request.files['arquivo']  # Obtém o arquivo enviado na requisição
        file_path = os.path.join(project_dir,file.filename)  # Obtém o caminho completo do arquivo
        file.save(file_path)  # Salva o arquivo no sistema de arquivos

        emails_data = load_json_from_file(file_path)  # Carrega os dados do arquivo JSON
        emails = emails_data['emails']  # Obtém a lista de emails

        first_group = emails[0]  # Considerando apenas o primeiro grupo do arquivo
        titulo_grupo = first_group['titulo']  # Obtém o título do grupo
        link_grupo = first_group['link']  # Obtém o link do grupo

        return jsonify({'message': 'Arquivo carregado com sucesso!', 'titulo_grupo': titulo_grupo, 'link_grupo': link_grupo})  # Retorna uma resposta JSON com os dados carregados
    except Exception as e:
        return jsonify({'message': f'Erro ao carregar arquivo: {str(e)}'})  # Retorna uma resposta JSON com a mensagem de erro em caso de falha



def load_emails():
    file_path = os.path.join(os.path.dirname(__file__), 'lista.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


@api_bp.route('/get_emails', methods=['GET'])
def get_emails():
    try:
        emails_data = load_emails()  # Carrega os dados do arquivo JSON
        print(emails_data)  # Exibe os dados carregados do arquivo JSON

        if 'emails' not in emails_data:
            return jsonify({'message': 'Nenhum email encontrado'})  # Retorna uma resposta JSON caso não haja emails

        emails = emails_data['emails']  # Acessa a lista de emails no JSON

        return jsonify(emails)  # Retorna os dados carregados do arquivo JSON como resposta JSON
    except Exception as e:
        return jsonify({'message': f'Erro ao obter os emails: {str(e)}'})  # Retorna uma resposta JSON com a mensagem de erro em caso de falha


# Habilitar o CORS usando o decorador after_request
@api_bp.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE"

    if response.headers.get("Content-Type") == "application/json" and response.status_code == 200:
        response.headers["Access-Control-Allow-Origin"] = "*"  # Permitir de qualquer origem para solicitações com status 200

    return response


# Tratar as solicitações de pré-voo OPTIONS explicitamente
@api_bp.route('/api/salvar-json', methods=['POST'])
def handle_post_request():
    # Lógica para manipular a solicitação POST
    salvar_arquivo_json()  # Chama a função salvar_arquivo_json para salvar o arquivo
    response = jsonify({"message": "Sucesso"})
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


def salvar_arquivo_json():
    # Obter os dados JSON da solicitação
    data = request.get_json()

    # Extrair as informações relevantes do JSON
    file_path = data.get('filePath')
    data_str = data.get('dataStr')

    # Verificar se as informações estão presentes
    if file_path and data_str:
        try:
            # Salvar o arquivo no diretório temporário do sistema
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, file_path)  # Combinar o diretório temporário com o caminho fornecido

            with open(file_path, 'w') as file:
                file.write(data_str)
            print("Arquivo salvo:", file_path)  # Declaração print para verificar se o arquivo foi salvo

            return jsonify({'message': 'Arquivo salvo com sucesso!'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Informações insuficientes'}), 400
