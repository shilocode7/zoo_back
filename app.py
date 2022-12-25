from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS, cross_origin
from datetime import datetime, date, time, timezone

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libery.DB.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

# model
######################## ---BOOKS CLASS---  #############################################

class Books(db.Model):
    id = db.Column('book_id', db.Integer, primary_key=True)
    book_name = db.Column(db.String)
    author = db.Column(db.String)
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.Integer)  # 1/2/3
    books = db.relationship('Loans', backref='books')

    def __init__(self, book_name, author, year_published, book_type):
        self.book_name = book_name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type

######################## ---CUSTOMER CLASS---  #############################################


class Customers(db.Model):
    id = db.Column('customer_id', db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    City = db.Column(db.String)
    Age = db.Column(db.Integer)
    customer_mode = db.Column(db.String)
    customers = db.relationship('Loans', backref='customers')

    def __init__(self, customer_name, City, Age, customer_mode):
        self.customer_name = customer_name
        self.City = City
        self.Age = Age
        self.customer_mode = customer_mode

######################## ---LOANS CLASS---  #############################################


class Loans(db.Model):
    id = db.Column("loan_id", db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    Loan_date = db.Column(db.String)
    Return_date = db.Column(db.String)
    loan_moed = db.Column(db.String)

    def __init__(self, customer_id, book_id, Loan_date, Return_date,loan_moed):
        self.customer_id = customer_id
        self.book_id = book_id
        self.Loan_date = Loan_date
        self.Return_date = Return_date
        self.loan_moed = loan_moed



######################## ---BOOKS CRUDE---  #############################################

@app.route('/books', methods=["POST", "GET"])
@app.route('/books/<bid>', methods=["DELETE", "PUT"])
@cross_origin()
def crude_book(bid=0):
    if request.method == 'POST':
        request_data = request.get_json()
        book_name = request_data['book_name']
        author = request_data["author"]
        year_published = request_data["year_published"]
        book_type = request_data["book_type"]
        newBook = Books(book_name, author, year_published, book_type)
        db.session.add(newBook)
        db.session.commit()
        return {"book": "created"}
    if request.method == 'GET':
        res = []
        for book in Books.query.all():
            res.append({"book_name": book.book_name, "id": book.id, "author": book.author,
                       "year_published": book.year_published, "book_type": book.book_type})
        return (json.dumps(res))
    if request.method == 'DELETE':  # not implemented yet
        del_book = Books.query.filter_by(id=bid).first()
        db.session.delete(del_book)
        db.session.commit()
        return {"book": "deleted"}
    if request.method == 'PUT':
        request_data = request.get_json()
        upd_book = Books.query.filter_by(id=bid).first()
        upd_book.book_name = request_data['book_name']
        upd_book.author = request_data["author"]
        upd_book.year_published = request_data["year_published"]
        upd_book.book_type = request_data["book_type"]
        db.session.commit()
        return {"book": "updated"}



######################## ---CUSTOMER CRUDE---  #############################################

@app.route('/customer', methods=["POST", "GET"])
@app.route('/customer/<cid>', methods=["DELETE", "PUT"])
@cross_origin()
def crude_customer(cid=0):
    if request.method == 'POST':
        request_data = request.get_json()
        customer_name = request_data['customer_name']
        City = request_data["City"]
        Age = request_data["Age"]
        customer_mode = request_data["customer_mode"]
        newCustomer = Customers(customer_name, City, Age, customer_mode)
        db.session.add(newCustomer)
        db.session.commit()
        return {"Cutomer": "created"}
    if request.method == 'GET':
        res = []
        for cus in Customers.query.all():
            res.append({"customer_name": cus.customer_name,"id": cus.id, "City": cus.City, "Age": cus.Age, "customer_mode": cus.customer_mode})
        return (json.dumps(res))
    if request.method == 'DELETE':  # not implemented yet customer_mode
        del_customer = Customers.query.filter_by(id=cid).first()
        db.session.delete(del_customer)
        db.session.commit()
        return {"Customer": "deleted"}
    if request.method == 'PUT':
        request_data = request.get_json()
        upd_customer = Customers.query.filter_by(id=cid).first()
        upd_customer.customer_name = request_data['customer_name']
        upd_customer.City = request_data["City"]
        upd_customer.Age = request_data["Age"]
        upd_customer.customer_mode = request_data["customer_mode"]
        db.session.commit()
        return {"book": "updated"}

######################## ---    LOANS CRUDE---  #############################################

@app.route('/loans', methods=["POST", "GET"])
@app.route('/loans/<lid>', methods=["DELETE", "PUT",'PATCH'])
@cross_origin()
def crude_loans(lid=0):
    if request.method == 'POST':
        request_data = request.get_json()
        customer_id = request_data["customer_id"]
        book_id = request_data["book_id"]
        Loan_date = request_data["Loan_date"]
        Return_date = request_data["Return_date"]
        loan_moed = request_data["loan_moed"]
        newLoan = Loans(customer_id, book_id, Loan_date, Return_date,loan_moed)
        db.session.add(newLoan)
        db.session.commit()
        return {"Book":"Loaned Successfully"}
    
    if request.method == 'GET':
        res = []
        for loan,book in db.session.query(Loans,Books).join(Books).all():
            res.append({"id":loan.id,"customer_id":loan.customer_id,"book_id":loan.book_id,"Loan_date":loan.Loan_date,"Return_date":loan.Return_date,"loan_moed":loan.loan_moed,"book_type":book.book_type})
        return (json.dumps(res))
    #customer_id, book_id, Loan_date, Return_date,loan_moed
    if request.method == 'PUT':
        request_data = request.get_json()
        upd_loan = Loans.query.filter_by(id=lid).first()
        upd_loan.loan_moed = request_data["loan_moed"]
        db.session.commit()
        return {"loan": "updated"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
