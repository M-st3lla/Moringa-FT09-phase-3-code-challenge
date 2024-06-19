
from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self._id = id
        self._name = name
        self._category = category
        if not hasattr(self, '_id') or self._id is None:
            self.save_to_db()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.update_db()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value
        self.update_db()

    def save_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    def update_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET name = ?, category = ? WHERE id = ?', (self._name, self._category, self._id))
        conn.commit()
        conn.close()

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles WHERE magazine_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]) for article in articles]

    def contributors(self):
        from models.author import Author  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT a.id, a.name FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author["id"], author["name"]) for author in authors]

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title FROM articles WHERE magazine_id = ?
        ''', (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return [title["title"] for title in titles]

    def contributing_authors(self):
        from models.author import Author  # Importing within the method
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.name FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id, a.name
            HAVING COUNT(ar.id) > 2
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author["id"], author["name"]) for author in authors]
