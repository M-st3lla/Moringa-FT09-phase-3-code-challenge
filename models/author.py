from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        self._id = id
        self._name = name
        if not hasattr(self, '_id') or self._id is None:
            self.save_to_db()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def save_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    def __repr__(self):
        return f'<Author {self.name}>'

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
             SELECT * FROM articles WHERE author_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]) for article in articles]

    def magazines(self):
        from models.magazine import Magazine  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT m.id, m.name, m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        ''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine["id"], magazine["name"], magazine["category"]) for magazine in magazines]



