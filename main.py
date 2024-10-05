import uvicorn
from fastapi import FastAPI
from python.Search import Searcher
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_manager = Searcher()

#data_manager.update_data_set()
data_manager.load_data()

@app.get('/')
async def home():
    return {"Data": "Hello World"}

@app.get('/search-by-function/{function_name}/')
async def search_by_function(function_name: str, page: Optional[int] = 0, page_size: Optional[int] = 100, ascending: Optional[bool] = False, sort_key: Optional[str] = 'value'):
    result = data_manager.search_by_function(function_name=function_name, ascending=ascending, page_size=page_size, page=page, key=sort_key)

    return {"amendments": result['amendments'],
            "quantity": result['quantity'],
            "total_value": result['total_value']}

@app.get('/search-by-local/{local_name}/')
async def search_by_local(local_name: str, page: Optional[int] = 0, page_size: Optional[int] = 100, ascending: Optional[bool] = False, sort_key: Optional[str] = 'value'):
    result = data_manager.search_by_local(local_name=local_name, ascending=ascending, page_size=page_size, page=page, key=sort_key)

    return {"amendments": result['amendments'],
            "quantity": result['quantity'],
            "total_value": result['total_value']}

@app.get('/search-by-author/{author_name}/')
async def search_by_author(author_name: str, page: Optional[int] = 0, page_size: Optional[int] = 100, ascending:Optional[bool] = False, sort_key: Optional[str] = 'value'):    
    result = data_manager.search_by_author(author_name=author_name, ascending=ascending, page_size=page_size, page=page, key=sort_key)

    return {"amendments": result['amendments'],
            "quantity": result['quantity'],
            "total_value": result['total_value']}
    
    
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
