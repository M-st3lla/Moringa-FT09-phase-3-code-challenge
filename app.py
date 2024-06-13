from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    author = Author(name=author_name)
    magazine = Magazine(name=magazine_name, category=magazine_category)
    article = Article(title=article_title, content=article_content, author_id=author.id, magazine_id=magazine.id)

    '''
        The following is just for testing purposes, 
        you can modify it to meet the requirements of your implmentation.
    '''

    print(f"\nCreated Author: {author}")
    print(f"Created Magazine: {magazine}")
    print(f"Created Article: {article}")


    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid # Use this to fetch the id of the newly created magazine
     author_articles = author.articles()
    print(f"\nArticles by Author {author.name}:")
    for art in author_articles:
        print(art)

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    conn.commit()
    author_magazines = author.magazines()
    print(f"\nMagazines by Author {author.name}:")
    for mag in author_magazines:
        print(mag)

    # Query the database for inserted records. 
    # The following fetch functionality should probably be in their respective models
    
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()
    magazine_articles = magazine.articles()
    print(f"\nArticles in Magazine {magazine.name}:")
    for art in magazine_articles:
        print(art)

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()
     magazine_contributors = magazine.contributors()
    print(f"\nContributors to Magazine {magazine.name}:")
    for contributor in magazine_contributors:
        print(contributor)
    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine["id"], magazine["name"], magazine["category"]))
    magazine_titles = magazine.article_titles()
    print(f"\nArticle Titles in Magazine {magazine.name}:")
    for title in magazine_titles:
        print(title)

    print("\nAuthors:")
    for author in authors:
        print(Author(author["id"], author["name"]))

    print("\nArticles:")
    for article in articles:
        print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))
    contributing_authors = magazine.contributing_authors()
    print(f"\nContributing Authors to Magazine {magazine.name} with more than 2 articles:")
    for author in contributing_authors:
        print(author)

if __name__ == "__main__":
    main()
