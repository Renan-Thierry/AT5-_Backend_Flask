from flask_restful import Resource
from flask import request, jsonify
from helpers.utils.MRequisicao import enviar_email


class EmailResource(Resource):
    def post(self):
        data = request.get_json()  # Obtém os dados JSON da requisição
        titulo_grupo = data.get('titulo_grupo') # Obtém o valor do campo 'titulo_grupo'
        mensagem_manual = data.get('mensagem_manual') # Obtém o valor do campo 'mensagem_manual'


        result = enviar_email(titulo_grupo, mensagem_manual) # Chama a função 'enviar_email' com os dados recebidos
        
        # Imprime o valor de 'mensagem_manual' para fins de depuração
        print(f"Valor de mensagem_manual recebido: {mensagem_manual}")
        
        # Verifica se o resultado do envio do email foi bem-sucedido
        if result:
            return {'message': 'Mensagem enviada com sucesso!'}  # Retorna uma resposta JSON de sucesso
        else:
            return {'message': 'Erro ao enviar mensagem.'} # # Retorna uma resposta JSON de erro
       
