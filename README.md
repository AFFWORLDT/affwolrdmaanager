# todolist

ToDo-List Using FastAPI and JWT Authentication

### Add .env file with following variables
  - SECRET_KEY=JWT_TOKEN_SECRET_KEY
  - ALGORITHM=HS256
  - ACCESS_TOKEN_EXPIRE_MINUTES= like 1440
  - MONGO_URI=mongodb_url
  - DB_NAME=<database name> like FastAPI-Todo
  
### To run locally

`
  uvicorn app.main:app
`
  
Visit /docs for swagger ui documentation :)
