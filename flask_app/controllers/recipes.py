from flask_app import app, render_template, redirect, request, session, bcrypt, flash
from flask_app.models.recipe import Recipe

@app.route('/recipe/create')
def connect_new_recipe():

    return render_template('new_recipe.html')

# // validate recipe information
# // if validation passes, create new recipe and redirect to the dashboard
# // if the dont pass display error messages
@app.route('/recipe/new', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/create')
    Recipe.save(request.form) 
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    Recipe.get_all()
    return render_template('dashboard.html', recipes = Recipe.get_all())
    
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    data = {'id': id}
    return render_template('edit_recipe.html', recipe = Recipe.get_one(data))

@app.route('/update/recipe', methods = ['POST'])
def update_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")
    print(request.form)
    Recipe.update(request.form)
    return redirect('/dashboard')

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    data = {'id': id}
    Recipe.delete(data)
    return redirect('/dashboard')

@app.route('/recipes/show/<int:id>')
def show_recipe(id):
    data = {'id': id}

    return render_template("show.html", recipe = Recipe.get_one(data))