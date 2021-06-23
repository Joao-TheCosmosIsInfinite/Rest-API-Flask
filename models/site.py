from sql_alchemy import banco

# A Classe e definida como uma tabela no banco de dados
class SiteModel(banco.Model):
    __tablename__='sites'
    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            'site_id':self.site_id,
            'url':self.url,
            'hoteis':[]
        }

    # Metodo de Classe
    @classmethod
    def find_site(cls, url):
        # metodo da classe que extendo o banco model, nesse caso sql_alchemy.model
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None

    def save_site(self):
        # Metodo built-in
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        # Metodo built-in
        banco.session.delete(self)
        banco.session.commit()


