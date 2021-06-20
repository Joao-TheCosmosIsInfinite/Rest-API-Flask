from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

app = Flask(__name__)
# Configurando a raiz/ caminho onde ficara alocado o banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
# Desabilitar o rastreamento de modificacoes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

# Verificar se existe um banco, e caso n~ao exista sera criado
# junto com as tabelas a partir do model
@app.before_first_request
def cria_banco():
    banco.create_all()

# Adicionar a Classe Hoteis a API, determinando tambem sua localizacao
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

# Executar a Res API
if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
