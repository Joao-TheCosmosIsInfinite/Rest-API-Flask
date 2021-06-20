from flask_restful import Resource, reqparse
from models.Hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hoteis.json() for hoteis in HotelModel.query.all()]} # SELECT * FROM hoteis

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

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            return hotel.json(), 200
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message":"Hotel id '{}' already exists." \
                            .format(hotel_id)}, 400
        # Recebendo atributos
        dados = Hotel.argumentos.parse_args()
        # Instanciando um objeto hotel
        hotel = HotelModel(hotel_id, **dados)

        try:
            # Insere/ salva hotel no banco de dados
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save'}, 500

        return hotel.json(), 200

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

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete'}, 500

            return {'message': 'Hotel deleted.'}, 200
        return {'message': 'Hotel not found'}, 404