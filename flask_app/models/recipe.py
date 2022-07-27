from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL


DATABASE = 'recipes_db'


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        if 'first_name' in data:
            self.first_name = data['first_name']

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['recipe_name']) < 3:
            flash('invalid recipe name, must be at least 3 characters, try again')
            is_valid = False
        if len(recipe['description']) < 3:
            flash('invalid description, dust yo self off and try again')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash('invalid instructions, dust yo self off and try again')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        # this is how we save the recipe to the database 
        query = "INSERT INTO recipes (recipe_name, description, instructions, date_cooked, under_30, user_id) VALUES (%(recipe_name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

#this is when i want to display all the recipes with their user. dashboard
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        recipes = []
        for result in results:
            recipes.append(Recipe(result))
        return recipes

#show the recipe to get one specific recipe. do this for both the one recipe and the edit onoe recipe
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return Recipe(results[0])

#update/edit the form of the recipe 
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET recipe_name = %(recipe_name)s, description = %(description)s, instructions = %(instructions)s, date_cooked = %(date_cooked)s, under_30 = %(under_30)s, user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)