from flask import Flask, jsonify, request
from dbconfig import db
from flask_migrate import Migrate
from models.Mensagem import Mensagem

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubancodedados.db'

db.init_app(app)
migrate = Migrate(app,db)


@app.route('/')
def home():
    return jsonify( {"mensagem": "Bem vindo a API de mensagens!"} )


@app.route('/mensagens') # read
def ler_mensagens():
    mensagens = Mensagem.query.all() # busca todas as mensagens no banco de dados
    mensagens = [mensagem.to_dict() for mensagem in mensagens] # transforma todas as mensagens em dicionários
    return jsonify(mensagens), 200


@app.route('/mensagens/criar', methods=['POST']) # create
def criar_mensagem():
    dados = request.get_json()
    conteudo = dados['conteudo']

    novaMensagem = Mensagem(conteudo=conteudo)

    db.session.add(novaMensagem)
    db.session.commit()

    return jsonify(novaMensagem.to_dict()), 201


@app.route('/mensagens/editar/<id>', methods=['PUT']) # update
def atualizar_mensagem(id):
    dados = request.get_json()
    conteudo = dados['conteudo']
   
    mensagem = Mensagem.query.get_or_404(id)

    mensagem.conteudo = conteudo
    db.session.commit()

    return jsonify(mensagem.to_dict()), 200



@app.route('/mensagens/excluir/<id>', methods=['DELETE']) # delete
def excluir_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id)
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify( {"mensagem": "Mensagem excluída com sucesso!"} ), 200



with app.app_context():
    from models.Mensagem import Mensagem 
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
