from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
# Configurando a raiz/ caminho onde ficara alocado o banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
# Desabilitar o rastreamento de modificacoes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Definir a chave/ criptografia com uma string
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
# Habilitar a blacklist para invalidar algum id ja passado
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)

# Verificar se existe um banco, e caso n~ao exista sera criado
# junto com as tabelas a partir do model
@app.before_first_request
def cria_banco():
    banco.create_all()

# Verificar se um token esta na blacklist
@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message':'You have been logged out.'}), 401

# Adicionar a Classe Hoteis a API, determinando tambem sua localizacao
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


# Executar a Res API
if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
