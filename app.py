import flask
import flask_sqlalchemy
import datetime
import pickle

app = flask.Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = flask_sqlalchemy.SQLAlchemy(app)

class Array(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    uploaded = db.Column(db.DateTime)
    data = db.Column(db.String)

    def serialize(self, data=True):
        serialized = {
            'id'      : self.id,
            'name'    : self.name,
            'uploaded': self.uploaded.isoformat()
        }
        if data:
            serialized['data'] = pickle.loads(self.data)
        return serialized

db.create_all()

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/array', methods=['GET', 'POST', 'DELETE'])
def array():
    r = flask.request.get_json()
    if flask.request.method == 'POST':
        db.session.add(Array(name=r['name'], data=pickle.dumps(r['data']), uploaded=datetime.datetime.now()))
        db.session.commit()
        return flask.jsonify(success=True), 201
    elif flask.request.method == 'GET':
        found = Array.query.get(r['id'])
        if found:
            return flask.jsonify(data=found.serialize(), success=True)
        else:
            return flask.jsonify(success=False), 404
    elif flask.request.method == 'DELETE':
        found = Array.query.filter_by(id=r['id'])
        if found:
            found.delete()
            db.session.commit()
            return flask.jsonify(success=True)
        else:
            return flask.jsonify(success=False), 404

@app.route('/api/arrays', methods=['GET'])
def arrays():
    r = [a.serialize(data=False) for a in db.session.query(Array).options(db.defer('data'))]
    return flask.jsonify(data=r, success=True)

if __name__ == '__main__':
    app.run()

