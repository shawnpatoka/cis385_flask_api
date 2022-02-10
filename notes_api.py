from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)


# dict of notes

NOTES = {
    1: {'title': 'First Note Title', 'body':'This is some note one text. This is some note one text. ',},
    2: {'title': 'Note Two Title', 'body':'Note Two Text. Note Two Text. Note Two Text. ',},
    3: {'title': 'The Third Title', 'body':'Some placeholder text for Note 3.',},
}



# not found handler

def abort_if_note_doesnt_exist(note_id):
    if note_id not in NOTES:
        abort(404, message="Note {} doesn't exist".format(note_id))



parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('body')



# controllers

class Notes(Resource):
    def get(self):
        return NOTES, 200

    def post(self):
        args = parser.parse_args()
        new_note_id = len(NOTES) + 1
        NOTES[new_note_id] = {'title': args['title'], 'body': args['body'], }
        return NOTES[new_note_id], 201
   


class NoteByID(Resource):
    def get(self, id):
        abort_if_note_doesnt_exist(id)
        return NOTES[id]
        

        
    
    # def put(self, note_id):
    #     args = parser.parse_args()
    #     note = {'note': args['note']}
    #     NOTES[note_id] = note
    #     return note, 201

    # def delete(self, note_id):
    #     abort_if_note_doesnt_exist(note_id)
    #     del NOTES[note_id]
    #     return '', 204

class NoteByTitle(Resource):
    def get(self, title):
        for item in NOTES:
            current_note = NOTES[item]
            if current_note['title'] == title:
                return current_note


# routes

api.add_resource(Notes, '/api/v1/notes')
api.add_resource(NoteByID, '/api/v1/notes/<int:id>')
api.add_resource(NoteByTitle, '/api/v1/notes/<string:title>')



if __name__ == '__main__':
    app.run(debug=True)