
from dns.resolver import query
import uvicorn
from fastapi import FastAPI, BackgroundTasks

from search import Searcher
from connector import Database

app = FastAPI()

@app.get('/search')
def search(background_tasks: BackgroundTasks, query_id: int):
    searcher = Searcher()
    authors_to_search = Database.get_authors(query_id)
    background_tasks.add_task(searcher.search, authors_to_search)
    return {'response': {'message': f'Start search authors photos for query #{query_id}'}}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8003)