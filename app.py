from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)

 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Zoo_Animals.sqlite3'
app.config['SECRET_KEY'] = "random string"
 
db = SQLAlchemy(app)
 
# model
class Animals(db.Model):
    id = db.Column('animals_id', db.Integer, primary_key = True)
    animal = db.Column(db.String(100))
    kind = db.Column(db.String(50))
    size = db.Column(db.String(50))
 
    def __init__(self, animal, kind, size):
        self.animal = animal
        self.kind = kind
        self.size = size
# model
@app.route('/',methods=["POST","GET"])
@app.route('/<aid>',methods=["DELETE","PUT"])
@cross_origin()
def crude_zoo(aid=0): 
    if request.method == 'POST':
        request_data = request.get_json()
        animal = request_data['animal']
        kind= request_data["kind"]
        size= request_data["size"]
        newAnimal= Animals(animal, kind, size)
        db.session.add (newAnimal)
        db.session.commit()
        return "A new animal was addad to zoo"
    if request.method == 'GET':
        res=[]
        for beast in Animals.query.all():
            res.append({"animal":beast.animal,"id":beast.id,"kind":beast.kind, "size":beast.size})
        return  (json.dumps(res))
    if request.method == 'DELETE': #not implemented yet
        del_animal = Animals.query.filter_by(id = aid).first()
        db.session.delete(del_animal)
        db.session.commit()
        return  {"animal":"deleted"}
    if request.method == 'PUT': #not implemented yet
        request_data = request.get_json()
        upd_animal = Animals.query.filter_by(id = aid).first()
        # upd_animal = Animals.query.get(id)
        # print(Animals.query.get(id))
        upd_animal.animal = request_data['animal']
        upd_animal.kind = request_data["kind"]
        upd_animal.size = request_data["size"] 
        return  {"animal":"updated"}
        
 
if __name__ == '__main__':
    with app.app_context():db.create_all()
    app.run(debug = True)
