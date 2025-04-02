from typing import Optional
from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel,Field
from starlette import status
app=FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    published_date:str


    def __init__(self,id,title,author,description,rating,published_date):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.published_date=published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create",default=None)
    title:str=Field(min_length=3)
    author:str=Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=0,lt=6)
    published_date:str=Field(min_length=4)

    model_config={
        "json_schema_extra":{
            "example":{
                "title":"A new book",
                "author":"Aditya Karekar",
                "description":"A new description of the book",
                "rating":"5",
                "published_date":"2021"
            }
        }
    }


BOOKS=[
    Book(1,"Computer Science","Aditya Karekar","A very nice book!",5,"2012"),
    Book(2,"Master Endpoints","Aditya Karekar","An awesome book!",5,"2014"),
    Book(3,"Be fast with FastAPI","Aditya Karekar","An awesome book!",5,"2016"),
    Book(4,"HP1","Author 1","Book Description",2,"2016"),
    Book(5,"HP2","Author 2","Book Description",3,"2020"),
    Book(6,"HP3","Author 3","Book Description",4,"2021")
]

@app.get("/books",status_code=status.HTTP_200_OK)
def get_all_books():
    return BOOKS





@app.get("/books/{book_by_id}",status_code=status.HTTP_200_OK)
def get_book_by_id(book_by_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_by_id:
            return book
    
    raise HTTPException(status_code=404,detail="Item not found")
        
@app.get("/books/get_book_by_rating/",status_code=status.HTTP_200_OK)
def get_book_by_rating(book_rating:int=Query(lt=6,gt=0)):
    read_books_by_rating=[]
    for book in BOOKS:
        if(book.rating==book_rating):
            read_books_by_rating.append(book)
    
    return read_books_by_rating

@app.get("/books/pusblished_year/{pusblished_year}",status_code=status.HTTP_200_OK)
def get_book_by_published_year(pusblished_year:str):
        book_by_published_year=[]
        for book in BOOKS:
            if(book.published_date==pusblished_year):
                book_by_published_year.append(book)
        
        return book_by_published_year
        

@app.post("/books/create_book",status_code=status.HTTP_201_CREATED)
def create_book(book_request:BookRequest):
    new_book=Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
def update_book(book:BookRequest):
    book_changed=False
    for i in range(0,len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book
            book_changed=True
    
    if(book_changed==False):
        raise HTTPException(status_code="404",detail="Item not found")

@app.delete("/books/delete_book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id:int=Path(gt=0)):
    book_changed=False
    for i in range(len(BOOKS)):
        if(BOOKS[i].id==book_id):
            BOOKS.pop(i)
            book_changed=True
            break
    if(book_changed==False):
        raise HTTPException(status_code="404",detail="Item not found")




def find_book_id(book:Book):
    if(len(BOOKS)>0):
        book.id=BOOKS[-1].id+1
    else:
        book.id=1
    
    return book