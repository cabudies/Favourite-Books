from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Books

engine = create_engine("sqlite:///books.db")

Base.metadata.bind = engine

## Use this end point to get all the books
@app.route('/')
@app.route('/products')
def allBooks():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    books = session.query(Books).all()
    return jsonify(books=[i.serialize for i in books])

## use this end point to create a new book
@app.route('/newBook', methods=['GET', 'POST'])
def newBook():
    if request.method == 'POST':
        newBook = Books(
            name=request.form['name'],
            description = request.form['description'],
            img_url = request.form['img_url']
        )
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(newBook)
        session.commit()
        # flash("new book inserted!")
        print("New Book Inserted")
        return jsonify(Book=newBook.serialize)

## use this end point to view specific book
@app.route('/viewBook/<int:book_id>', methods=['GET', 'POST'])
def viewBookById(book_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    book = session.query(Books).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)

## use this end point to view specific book
@app.route('/search')
def viewBookByName():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    name = request.args.get('name', '')
    try:
        book = session.query(Books).filter_by(name=name).one()
        return jsonify(book=book.serialize)
    except:
        return "No record found."

if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port=5000)