from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

app = Flask(__name__)

from sqlalchemy import create_engine
## ORM - Object Relation Mapping
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Books

engine = create_engine("sqlite:///books.db")

Base.metadata.bind = engine

## Use this end point to get all the books
@app.route("/")
@app.route('/products')
def homePage():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    books = session.query(Books).all()
    return render_template('index.html', books=books)

## use this end point to create a new book
@app.route('/newBook', methods=['GET', 'POST'])
def newBook():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newBook = Books(
            name=request.form['name'],
            description = request.form['description'],
            img_url = request.form['img_url']
        )
        session.add(newBook)
        session.commit()
        flash("new book inserted!")
        return redirect(url_for('homePage'))
    else:
        return render_template('newbook.html')

## use this end point to view specific book
@app.route('/viewBook/<int:book_id>/', methods=['GET', 'POST'])
def viewBookById(book_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    book = session.query(Books).filter_by(id=book_id).one()
    return render_template('singleBook.html', book=book)

## use this end point to view specific book
@app.route('/search')
def viewBookByName():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    name = request.args.get('name', '')
    try:
        books = session.query(Books).filter_by(name=name).all()
        return render_template('viewAllBooks.html', books=books)
    except:
        books = []
        return render_template('viewAllBooks.html', books=books)

@app.route("/users")
def allUsers():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    users = session.query(User).all()
    return render_template('allusers.html', users = users)

# TODO 4: Create route for newUser function here
@app.route('/newUser', methods=['GET', 'POST'])
def newUser():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newUser = User(
            name=request.form['name'],
            favourite_book_id = '0'
        )
        session.add(newUser)
        session.commit()
        flash("new user created!")
        return redirect(url_for('allUsers'))
    else:
        return render_template('newUser.html')

@app.route("/singleUser/<int:user_id>")
def singleUser(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    single_user = session.query(User).filter_by(id=user_id).one()
    if (single_user.favourite_book_id != None):
        book_list = single_user.favourite_book_id.split(',')
        book_list = list(map(lambda x: int(x), book_list))
        favourite_books = session.query(Books).filter(Books.id.in_(book_list)).all()
        books = session.query(Books).filter(Books.id.notin_(book_list)).all()
    else:
        favourite_books = []
        books = session.query(Books).all()
    return render_template('singleUser.html', single_user=single_user,
                           favourite_books=favourite_books, books=books)

@app.route("/singleUser/<int:user_id>/favourites")
def singleUserFavourites(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    single_user = session.query(User).filter_by(id=user_id).one()
    if (single_user.favourite_book_id != None):
        favourite_books = session.query(Books).filter_by(id = single_user.favourite_book_id).all()
        return render_template('singleUser.html', single_user = single_user, favourite_books = favourite_books)
    else:
        return render_template('singleUser.html', single_user=single_user)

@app.route("/setfavourite/<int:user_id>/<int:book_id>")
def setFavourite(user_id, book_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    single_user = session.query(User).filter_by(id=user_id).one()
    updated_list: str
    if (single_user.favourite_book_id != None):
        updated_list = single_user.favourite_book_id + "," + str(book_id)
    else:
        updated_list = str(book_id)
    single_user.favourite_book_id = updated_list
    session.add(single_user)
    session.commit()
    return redirect(url_for('singleUser', user_id=single_user.id))

@app.route("/removeFromFavourites/<int:user_id>/<int:book_id>")
def removeFromFavourites(user_id, book_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    single_user = session.query(User).filter_by(id=user_id).one()
    favourites_list = single_user.favourite_book_id.split(',')
    favourites_list = list(map(lambda x: int(x), favourites_list))
    favourites_list.remove(book_id)
    if (len(favourites_list) > 0):
        favourites_list = list(map(lambda x: str(x), favourites_list))
        updated_list = ",".join(favourites_list)
        single_user.favourite_book_id = updated_list
    else:
        single_user.favourite_book_id = '0'
    session.add(single_user)
    session.commit()
    return redirect(url_for('singleUser', user_id=single_user.id))


if __name__ == "__main__":
    app.secret_key = 'random_key_1234@flask'
    app.debug = True
    ## host address for testing before deploying
    app.run(host='127.0.0.1', port=4300)