# blog/routes.py
  
from flask import render_template
from app import app
from app.models import Entry, db
from flask import render_template, request
from app.forms import EntryForm
import functools

@app.route("/")
def index():
   all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
   return render_template("homepage.html", all_posts=all_posts)

@app.route("/post/<int:entry_id>", methods=["GET", "POST"])
def post(entry_id):
    if entry_id == 0:
        form = EntryForm()
        errors = None
        if request.method == 'POST':
            if form.validate_on_submit():
                entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
                )
                db.session.add(entry)
                db.session.commit()
            else:
                errors = form.errors
        return render_template("entry_form.html", form=form, errors=errors)
    else:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        errors = None
        if request.method == 'POST':
            if form.validate_on_submit():
                   form.populate_obj(entry)
                   db.session.commit()
            else:
                 errors = form.errors
        return render_template("entry_form.html", form=form, errors=errors)  