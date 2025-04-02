from fastapi import Body, FastAPI
app=FastAPI()
BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]
# print(BOOKS[0].get())


@app.get("/books")
def get_all_books():
    return BOOKS




@app.get("/books/title/{book_title}")
def get_book_by_title(book_title: str):
    print(f"Received book title: {book_title}")
    for book in BOOKS:
        if book.get("title").casefold()==book_title.casefold():
            return book
    return {"error": "Book not found"}


@app.get("/books/author/{book_author}")
def get_category_by_query(category:str,book_author:str):
    books_to_return=[]
    for book in BOOKS:
        if(book.get("category").casefold()==category.casefold() 
           and 
           book.get("author").casefold()==book_author.casefold()):
            books_to_return.append(book)

    return books_to_return

@app.get("/books/by_author/{book_author}")
def get_all_books_by_author_name(book_author:str):
    books_by_author=[]
    for book in BOOKS:
        if(book.get("author").casefold()==book_author.casefold()):
            books_by_author.append(book)

    return books_by_author
        

@app.post("/books/create_book")
def create_book(new_book=Body()):
    return BOOKS.append(new_book)

@app.put("/books/update_book")
def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if(BOOKS[i].get("title").casefold()==updated_book.get("title").casefold()):
            BOOKS[i]=updated_book

@app.delete("/books/delete_book/{book_title}")
def delete_book(book_title:str):
   for i in range(len(BOOKS)):
       if(BOOKS[i].get("title").casefold()==book_title.casefold()):
           BOOKS.pop(i)
           break
       

            


