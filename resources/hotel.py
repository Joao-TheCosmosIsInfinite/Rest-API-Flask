from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from resources.filtros import normalize_path_params
from resources.site import SiteModel
import database.scripts as datascripts

import sqlite3

# Passar alguns filtros via path
# path /hoteis?cidade=Rio de Janeiro&csat=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('csat_min', type=float)
path_params.add_argument('csat_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


# Obrigar login para realziar algumas operacoes com hoteis
from flask_jwt_extended import jwt_required

class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        # filtrar os dados validos
        dados_validos = {key: dados[key] for key in dados \
                            if dados[key] is not None}

        parametros = normalize_path_params(**dados_validos)

        consulta = datascripts.consulta_hoteis(parametros.get('cidade'))

        tupla = tuple([parametros[value] for value in parametros])

        resultado = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id':linha[0],
                'nome':linha[1],
                'csat':linha[2],
                'diaria':linha[3],
                'cidade':linha[4],
                'site_id':linha[5]
            })
        return {'hoteis': hoteis} # SELECT * FROM hoteis

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    # Campo 'nome' eh requerido
    argumentos.add_argument('nome',
                            type=str,
                            required=True,
                            help="The field 'nome' cannot be left blank.")

    argumentos.add_argument('csat', type=float)
    argumentos.add_argument('diaria', type=float)
    argumentos.add_argument('cidade', type=str)
    argumentos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            return hotel.json(), 200
        return {'message': 'Hotel not found'}, 404

    @jwt_required() # Sera preciso passar um token de acesso
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message":"Hotel id '{}' already exists." \
                            .format(hotel_id)}, 400
        # Recebendo atributos
        dados = Hotel.argumentos.parse_args()
        # Instanciando um objeto hotel
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_site_by_id(dados['site_id']):
            return {"message":"The hotel must be associated to a valid site id."}, 400

        try:
            # Insere/ salva hotel no banco de dados
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save'}, 500

        return hotel.json(), 201

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {'message': 'An internal error ocurred trying to update'}, 500
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save'}, 500

        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete'}, 500

            return {'message': 'Hotel deleted.'}, 200
        return {'message': 'Hotel not found'}, 404