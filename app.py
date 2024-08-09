from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/myblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts, is_user_admin=is_user_admin())

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post, is_user_admin=is_user_admin())

@app.route('/admin')
def admin():
    if is_user_admin():
        posts = Post.query.all()
        return render_template('admin.html', posts=posts, is_user_admin=is_user_admin())
    else:
        return redirect(url_for('home'))

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('admin'))

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if is_user_admin():
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()

    return redirect(url_for('admin'))

@app.route('/view_posts')
def view_posts():
    posts = Post.query.all()
    return render_template('view_posts.html', posts=posts, is_user_admin=is_user_admin())

def is_user_admin():
   
    return True  

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


