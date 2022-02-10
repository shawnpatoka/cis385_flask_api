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



# not found handlers

def abort_if_note_doesnt_exist(note_id):
    if note_id not in NOTES:
        abort(404, message="Note {} doesn't exist".format(note_id))

def abort_if_note_doesnt_exist_by_title(title):
    titles = []
    # add note titles to a list
    for note in NOTES:
        temp = NOTES[note]
        titles.append(temp['title'])
    
    # search to see if given title is in titles list. If not, raise a 404
    if title not in titles:
        abort(404, message="Note '{}' doesn't exist".format(title))



# setting args

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
        return new_note_id, 201
   


class NoteByID(Resource):
    def get(self, id):
        abort_if_note_doesnt_exist(id)
        return NOTES[id], 200
        
    def put(self, id):
        abort_if_note_doesnt_exist(id)
        args = parser.parse_args()
        note = {'title': args['title'], 'body': args['body'], }
        NOTES[id] = note
        return note, 201

    def delete(self, id):
        abort_if_note_doesnt_exist(id)
        del NOTES[id]
        return "BLAH", 204



class NoteByTitle(Resource):
    def get(self, title):
        abort_if_note_doesnt_exist_by_title(title)
        for num in NOTES:
            current_note = NOTES[num]
            print(current_note)
            if current_note['title'] == title:
                return current_note, 200

    def put(self, title):
        abort_if_note_doesnt_exist_by_title(title)
        for num in NOTES:
            current_note = NOTES[num]
            if current_note['title'] == title:
                args = parser.parse_args()
                updated_info = {'title': args['title'], 'body': args['body'], }
                NOTES[num] = updated_info
                return NOTES[num], 201




# routes

api.add_resource(Notes, '/api/v1/notes')
api.add_resource(NoteByID, '/api/v1/notes/<int:id>')
api.add_resource(NoteByTitle, '/api/v1/notes/<string:title>')



if __name__ == '__main__':
    app.run(debug=True)