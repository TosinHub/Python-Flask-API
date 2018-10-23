import sqlite3
from flask import Flask, request
from flask_restful import Resource,reqparse
from flask_jwt import JWT, jwt_required
from security import  authenticate, identity
from models.item import  ItemModel


class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=int,
    required=True,
    help="This field cannot be blank"
    
    )
    parser.add_argument('store_id',
    type=int,
    required=True,
    help="Every item must have a store ID"
    
    )
    
    @jwt_required()
    def get(self,name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name =?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'id':row[0], 'name': row[1], 'price': row[2]}}
           

    def post(self,name):
        
        if ItemModel.find_by_name(name):
            return {"message": "Item with name already exists"}

        data = Item.parser.parse_args()
        item = ItemModel(name,**data) 
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"},500    

        return {"message": "Item added successfully"},201
   
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item successfully deleted"},201

    def put(self,name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name,**data)
        if item is None:
            item = ItemModel(name,**data)          
        else:
            item.price = data['price']  
        item.save_to_db()                    
        return updated_item.json()

class ItemList(Resource):
    def get(self):
         return {'items': [item.json() for item in ItemModel.query.all()]}
         ##return {'item': list(map(lambda x: x.json(),ItemModel.query.all()))}
    
    
    ''' connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items  = []
        for row in result:
            items.append({'name': row[1],'price': row[2]})
        connection.commit()
        connection.close()
        return {'items': items} '''