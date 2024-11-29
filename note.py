from datetime import datetime

# Класс заметки объявляем
class Note:
    def __init__(self, note_id, title, content, timestamp=None):
        self.id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }

    def update_from_dict(self, data):

        self.title = data.get('title', self.title)
        self.content = data.get('content', self.content)
        self.timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')


def note_from_dict(data):
    return Note(
        note_id=data['id'],
        title=data['title'],
        content=data['content'],
        timestamp=data['timestamp']
    )
