import sqlite3
from flask_restful import  Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help="This field cannot be blank"
    
    )
    parser.add_argument('password',
    type=str,
    required=True,
    help="This field cannot be blank"
    
    )

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users"        
        for row in cursor.execute(query):
            return {'Users': {'id': row[0], 'username': row[1]}}

    def post(self):
        
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "User with username already exists"}
        user = UserModel(**data)
        user.save_to_db();

        return {"message": "User created successfully"},201
    