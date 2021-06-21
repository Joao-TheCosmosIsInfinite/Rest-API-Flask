from sql_alchemy import banco

# A Classe e definida como uma tabela no banco de dados
class UserModel(banco.Model):
    __tablename__='usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
        # O id nao sera incluido, com isso o sqlalchemy ira incrementar automaticamente

    def json(self):
        return {
            'user_id':self.user_id,
            'login':self.login
        }

    # Metodo de Classe
    @classmethod
    def find_user(cls, user_id):
        # metodo da classe que extendo o banco model, nesse caso sql_alchemy.model
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        # metodo da classe que extendo o banco model, nesse caso sql_alchemy.model
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    def save_user(self):
        # Metodo built-in
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        # Metodo built-in
        banco.session.delete(self)
        banco.session.commit()


