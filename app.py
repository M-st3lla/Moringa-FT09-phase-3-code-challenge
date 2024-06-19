from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    #user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    author = Author(name=author_name)
    magazine = Magazine(name=magazine_name, category=magazine_category)
    article = Article(title=article_title, content=article_content, author_id=author.id, magazine_id=magazine.id)


    print(f"\nCreated Author: {author}")
    print(f"Created Magazine: {magazine}")
    print(f"Created Article: {article}")


    author_articles = author.articles()
    print(f"\nArticles by Author {author.name}:")
    for art in author_articles:
        print(art)


    author_magazines = author.magazines()
    print(f"\nMagazines by Author {author.name}:")
    for mag in author_magazines:
        print(mag)


    magazine_articles = magazine.articles()
    print(f"\nArticles in Magazine {magazine.name}:")
    for art in magazine_articles:
        print(art)


    magazine_contributors = magazine.contributors()
    print(f"\nContributors to Magazine {magazine.name}:")
    for contributor in magazine_contributors:
        print(contributor)


    magazine_titles = magazine.article_titles()
    print(f"\nArticle Titles in Magazine {magazine.name}:")
    for title in magazine_titles:
        print(title)


    contributing_authors = magazine.contributing_authors()
    print(f"\nContributing Authors to Magazine {magazine.name} with more than 2 articles:")
    for author in contributing_authors:
        print(author)

if __name__ == "__main__":
    main()
