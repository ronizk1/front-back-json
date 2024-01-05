

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_of_recipe = db.Column(db.String(45), nullable=False)
    ingredients = db.Column(db.String(45), nullable=False)
    prepare_time = db.Column(db.String(45), nullable=False)
    # image = db.Column(db.String(100), nullable=False)


# Uncomment the next two lines to create tables
# with app.app_context():
#     db.create_all()

@app.route('/list_recipes', methods=['GET'])
def list_recipes():
    recipes = Recipe.query.all()
    recipes_list = []
    for recipe in recipes:
        recipes_list.append({
            'id': recipe.id,
            'name_of_recipe': recipe.name_of_recipe,
            'ingredients': recipe.ingredients,
            'prepare_time': recipe.prepare_time
        })
    return jsonify({'recipes': recipes_list})

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    try:
        data = request.get_json()
        new_recipe = Recipe(
            name_of_recipe=data.get('name_of_recipe'),
            ingredients=data.get('ingredients'),
            prepare_time=data.get('prepare_time')
        )
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    try:
        recipe_to_delete = Recipe.query.get(recipe_id)
        if recipe_to_delete:
            db.session.delete(recipe_to_delete)
            db.session.commit()
            return jsonify({'message': 'Recipe deleted successfully'})
        else:
            return jsonify({'message': 'Recipe not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/update_recipe/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    try:
        recipe_to_update = Recipe.query.get(recipe_id)
        if recipe_to_update:
            data = request.get_json()
            recipe_to_update.name_of_recipe = data.get('name_of_recipe')
            recipe_to_update.ingredients = data.get('ingredients')
            recipe_to_update.prepare_time = data.get('prepare_time')
            db.session.commit()
            return jsonify({'message': 'Recipe updated successfully'}), 200
        else:
            return jsonify({'message': 'Recipe not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from PIL import Image
# from io import BytesIO

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Configure SQLite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['UPLOAD_FOLDER'] = 'uploads'
# db = SQLAlchemy(app)

# class Recipe(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name_of_recipe = db.Column(db.String(45), nullable=False)
#     ingredients = db.Column(db.String(45), nullable=False)
#     prepare_time = db.Column(db.String(45), nullable=False)
#     image_path = db.Column(db.String(255))  # Path to the uploaded image

# # Uncomment the next two lines to create tables
# # with app.app_context():
# #     db.create_all()

# @app.route('/list_recipes', methods=['GET'])
# def list_recipes():
#     recipes = Recipe.query.all()
#     recipes_list = []
#     for recipe in recipes:
#         recipes_list.append({
#             'id': recipe.id,
#             'name_of_recipe': recipe.name_of_recipe,
#             'ingredients': recipe.ingredients,
#             'prepare_time': recipe.prepare_time,
#             'image_path': recipe.image_path
#         })
#     return jsonify({'recipes': recipes_list})

# @app.route('/add_recipe', methods=['POST'])
# def add_recipe():
#     try:
#         data = request.form.to_dict()
#         # Save image
#         if 'image' in request.files:
#             image = request.files['image']
#             image_path = save_image(image)
#             data['image_path'] = image_path

#         new_recipe = Recipe(
#             name_of_recipe=data.get('name_of_recipe'),
#             ingredients=data.get('ingredients'),
#             prepare_time=data.get('prepare_time'),
#             image_path=data.get('image_path')
#         )
#         db.session.add(new_recipe)
#         db.session.commit()
#         return jsonify({'message': 'Recipe added successfully'}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/delete_recipe/<int:recipe_id>', methods=['DELETE'])
# def delete_recipe(recipe_id):
#     try:
#         recipe_to_delete = Recipe.query.get(recipe_id)
#         if recipe_to_delete:
#             # Delete image file if it exists
#             if recipe_to_delete.image_path:
#                 delete_image(recipe_to_delete.image_path)
#             db.session.delete(recipe_to_delete)
#             db.session.commit()
#             return jsonify({'message': 'Recipe deleted successfully'})
#         else:
#             return jsonify({'message': 'Recipe not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# def save_image(image):
#     img = Image.open(image)
#     # Generate a unique filename for the image
#     image_filename = f"recipe_image_{hash(image)}"  # You may want to use a proper hashing method
#     image_path = f"{app.config['UPLOAD_FOLDER']}/{image_filename}.png"
#     img.save(image_path, "PNG")
#     return image_path

# def delete_image(image_path):
#     try:
#         os.remove(image_path)
#     except Exception as e:
#         print(f"Error deleting image: {str(e)}")

# if __name__ == '__main__':
#     app.run(debug=True)
