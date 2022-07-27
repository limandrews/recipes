from flask_app import app, render_template, redirect, request, session, bcrypt, flash
from flask_app.models.user import User



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/register', methods=['POST']) 
def register_user():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    # hash password
    hash_pass = bcrypt.generate_password_hash(request.form['password'])
    # create data dict to change password value to the hash created above.
    data = {'first_name': request.form['first_name'], 'last_name': request.form['last_name'], 'email': request.form['email'], 'password': hash_pass}
    # save user to database
    user_id = User.save(data)
    # log user in
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    print(session)
    return redirect('/dashboard')

@app.route('/users/show/<int:id>')
def show_user(id):
    # create user show page if necessary
    return render_template("show_user.html")


@app.route('/users/login', methods = ['post'])
def login_user():
    # query database for user email from form
    data = {'email': request.form['log_email']}
    
    new_user = User.getemail(data)
    print(new_user)
    
    if not new_user:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(new_user.password, request.form['log_password']):
        flash("Invalid Email/Password")
        return redirect('/')

    # log user in
    session['user_id'] = new_user.id
    session['first_name'] = new_user.first_name

    # use query to redirect if not found
    # check password in form against password hash in database
    # redirect if not found

    # redirect to app page
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


