from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)


# dict of notes

NOTES = {
    'note1': {'note': 'This is some example note text.'},
    'note2': {'note': 'This is even more example note text.'},
}



# not found handler

def abort_if_note_doesnt_exist(note_id):
    if note_id not in NOTES:
        abort(404, message="Note {} doesn't exist".format(note_id))



parser = reqparse.RequestParser()
parser.add_argument('note')



# controllers

class Notes(Resource):
    def get(self):
        return NOTES, 200

    def post(self):
        args = parser.parse_args()
        note_id = int(max(NOTES.keys()).lstrip('note')) + 1
        note_id = 'note%i' % note_id
        NOTES[note_id] = {'note': args['note']}
        return NOTES[note_id], 201
   


class Note(Resource):
    def get(self, note_id):
        abort_if_note_doesnt_exist(note_id)
        return NOTES[note_id]
    
    def put(self, note_id):
        args = parser.parse_args()
        note = {'note': args['note']}
        NOTES[note_id] = note
        return note, 201

    def delete(self, note_id):
        abort_if_note_doesnt_exist(note_id)
        del NOTES[note_id]
        return '', 204



# routes

api.add_resource(Notes, '/api/v1/notes')
api.add_resource(Note, '/api/v1/notes/<note_id>')



if __name__ == '__main__':
    app.run(debug=False)