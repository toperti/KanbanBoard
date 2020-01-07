from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	task = db.Column(db.String(150), unique = True, nullable = False)
	category = db.Column(db.String, nullable = False)

	def __repr__(self):
		return '<Todo %r>' % self.task

class Inpro(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	task = db.Column(db.String(150), unique = True, nullable = False)
	category = db.Column(db.String, nullable = False)

	def __repr__(self):
		return '<Inpro %r>' % self.task

class Completed(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	task = db.Column(db.String(150), unique = True, nullable = False)
	category = db.Column(db.String, nullable = False)

	def __repr__(self):
		return '<Completed %r>' % self.task


@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == "POST":
		task = request.form['content']
		category = request.form['category']
		if category == "Todo":
			new_task = Todo(task = task, category = category)
			db.session.add(new_task)
			db.session.commit()
			return redirect('/')

		elif category == "Inpro":
			new_task = Inpro(task = task, category = category)
			db.session.add(new_task)
			db.session.commit()
			return redirect('/')

		else:
			new_task = Completed(task = task, category = category)
			db.session.add(new_task)
			db.session.commit()
			return redirect('/')

	else:
		todo = Todo.query.all()
		inpro = Inpro.query.all()
		completed = Completed.query.all()
		return render_template('index.html', todo = todo, inpro = inpro, completed = completed)

@app.route('/edit/<string:category>/<int:id>', methods = ['GET', 'POST'])
def edit(category, id):
	if category == 'Todo':
		task = Todo.query.get_or_404(id)
	elif category == 'Inpro':
		task = Inpro.query.get_or_404(id)
	else:
		task = Completed.query.get_or_404(id)

	if request.method == 'POST':
		if request.form['action'] == "Save Edits":
			content = request.form['content']

			post_category = request.form['category']
			if category != post_category:
				if post_category == "Todo":
					db.session.delete(task)
					new_task = Todo(task = content, category = post_category)
					db.session.add(new_task)
					db.session.commit()
					return redirect('/')

				elif post_category == "Inpro":
					db.session.delete(task)
					new_task = Inpro(task = content, category = post_category)
					db.session.add(new_task)
					db.session.commit()
					return redirect('/')

				else:
					db.session.delete(task)
					new_task = Completed(task = content, category = post_category)
					db.session.add(new_task)
					db.session.commit()
					return redirect('/')
			else:
				task.content = content
		else:
			db.session.delete(task)
			db.session.commit()
			return redirect('/')

	else:
		return render_template('edit.html', task = task)

