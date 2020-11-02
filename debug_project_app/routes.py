from debug_project_app import app, Message, mail, db

# Import specific packages from flask
from flask import render_template, request, redirect, url_for

# Import for Forms
from debug_project_app.forms import UserInfoForm, PostForm, LoginForm

# Import for Models
from debug_project_app.models import User, Post, check_password_hash

# Import for Flask Login - login_required, login_user,current_user, logout_user
from flask_login import login_required,login_user, current_user,logout_user

# Home Route
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts = posts)

# Register Route
@app.route('/register', methods=['GET','POST'])
def register():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        # Get Information
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print("\n",username,password,email)
        # Create an instance of User
        user = User(username,email,password)
        # Open and insert into database
        db.session.add(user)
        # Save info into database
        db.session.commit()

        # Flask Email Sender 
        #msg = Message(f'Thanks for Signing Up! {email}', recipients=[email], sender=("Me", "me@example.com"))
        #msg.body = ('Congrats on signing up! Looking forward to your posts!')
        #msg.html = ('<h1> Welcome to debug_project_app!</h1>' '<p> This will be fun! </p>')
        #assert msg.sender == "Me <me@example.com>"
        

        #mail.send(msg)
    return render_template('register.html', user_form = form)

# Login Form Route
@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html',login_form = form) 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Post Submission Route
@app.route('/posts', methods=['GET','POST'])
@login_required
def posts():
    post = PostForm()
    if request.method == 'POST' and post.validate():
        title = post.title.data
        content = post.content.data
        user_id = current_user.id
        print('\n',title,content)
        post = Post(title,content,user_id)

        db.session.add(post)

        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('posts.html', post = post)

@app.route('/posts/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post = post)


@app.route('/posts/update/<int:post_id>', methods = ['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        print(title,content,user_id)

        # Update will get added to the DB
        post.title = title
        post.content = content
        post.user_id = user_id

        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post_update.html', update_form = form)

@app.route('/posts/delete/<int:post_id>', methods = ['GET','POST', 'DELETE'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))