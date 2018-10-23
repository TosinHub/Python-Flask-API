from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy='dynamic')
    
    def __init__(self,name):      
        self.name = name
 

    def json(self):
        return {'name': self.name,'items': [item.json() for item in self.items.all()]}    
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()  

'''     connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name =?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)''' 
            

'''         connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(NULL,?,?)"
        cursor.execute(query,(self.name,self.price))
        connection.commit()
        connection.close()    
    
    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price =? WHERE name =?"
        cursor.execute(query,(self.price,self.name))
        connection.commit()
        connection.close()''' 
               