from flask import (Blueprint, flash, g, abort, redirect, render_template, request, url_for)
from werkzeug.exceptions import Aborter

from jreddo.auth import login_required
from jreddo.db import get_db

bp = Blueprint('blog', __name__)



# index view
@bp.route('/')
def index():
  db = get_db()
  posts = db.execute(
    'SELECT p.id, title, body, created, author_id, username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' ORDER BY created DESC'
  ).fetchall()
  
  return render_template('blog/index.html', posts=posts)

# create view
@bp.route('/create', methods=('GET', 'POST'))
def create():
  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    error = None

    if not title:
      error = 'Title is required!!!'
    elif not body:
      error = 'Body is required!!!'
      
    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
      db.commit()
      return redirect(url_for('blog.index'))
  
  return render_template('blog/create.html')


# fetching post
def get_post(id, check_author=True):
  post = get_db().execute(
    'SELECT P.id, title, body, created, author_id, username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' WHERE p.id = ?',
    (id,)
  ).fetchone()
  
  
  if post is None:
    abort(404, f'Post id {id} does not exist!!!')
    
  if check_author and post['author_id'] != g.user['id']:
    abort(403)
    
  return post

# update view
@bp.route('/<int:id>/update', methods=('POST', 'GET'))
@login_required
def update(id):
  post = get_post(id)
  
  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    error = None
    
    
    if not title:
      error = 'Title is required!!!'
    elif not body:
      error = 'Body is required!!!'
      
    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'UPDATE post SET title = ?, body = ?'
        ' WHERE id = ?',
        (title, body, id)
      )
      db.commit()
      return redirect(url_for('blog.index'))
    
  return render_template('blog/update.html', post=post)

# delete view
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
  db = get_db()
  db.execute(
    'DELETE FROM post WHERE id = ?', (id,)
  )
  db.commit()
  return redirect(url_for('blog.index'))