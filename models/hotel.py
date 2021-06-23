from sql_alchemy import banco

# A Classe e definida como uma tabela no banco de dados
class HotelModel(banco.Model):
    __tablename__='hoteis'
    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    csat = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id'))

    def __init__(self, hotel_id, nome, csat, diaria, cidade, site_id):
        self.hotel_id = hotel_id
        self.nome = nome
        self.csat = csat
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id

    def json(self):
        return {
            'hotel_id':self.hotel_id,
            'nome':self.nome,
            'csat':self.csat,
            'diaria':self.diaria,
            'cidade':self.cidade,
            'site_id':self.site_id
        }

    # Metodo de Classe
    @classmethod
    def find_hotel(cls, hotel_id):
        # metodo da classe que extendo o banco model, nesse caso sql_alchemy.model
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()# SELECT * FROM hoteis WHERE hotel_id = hotel_id LIMIT 1
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        # Metodo built-in
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, csat, diaria, cidade):
        self.nome = nome
        self.csat = csat
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        # Metodo built-in
        banco.session.delete(self)
        banco.session.commit()


