from flask import Flask,render_template,request,flash,redirect,url_for
from datetime import datetime
from flask_sqlalchemy import  SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, TextAreaField
app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class PostForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	content = TextAreaField('Content',validators=[DataRequired()])
	submit = SubmitField('submit')


class Post(db.Model):
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	title = db.Column(db.String(100),nullable=False,default=datetime.utcnow)
	date_posted = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text,nullable=False)

	def __repr__(self):
		return "Post('{0}','{1}')".format(self.title,self.date_post)


class Comment(db.Model):
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	title = db.Column(db.String(50),nullable=False,default=datetime.utcnow)
	date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	content = db.Column(db.Text,nullable=False)

	def __repr__(self):
		return "Comment('{0}','{1}')".format(self.title,self.date_post)


@app.route("/")
@app.route("/home")
def text():
	posts = Post.query.all()
	return render_template("index.html",posts=posts)


@app.route("/post",methods=['GET','POST'])
def post():
	posts = Post.query.all()
	form = PostForm()
	if request.method == "POST":
		post = Post(title=form.title.data,content=form.content.data)
		db.session.add(post)
		db.session.commit()
		flash('your post has been created!','success')
		return redirect('home')
	return render_template('post.html',title="New post",form=form,posts=posts)


@app.route('/post/<int:post_id>',methods=['GET','POST'])

def post_id(post_id):
	post = Post.query.get_or_404(post_id)
	form=PostForm()
	comment = Comment(title=form.title.data,content=form.content.data)
	if request.method == "POST":
		db.session.add(comment)
		db.session.commit()
	return render_template("post_id.html",title=post.title,post=post,comment=comment,form=form)
	

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')