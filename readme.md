5:28:20


Schema/Pydantic Models define the structure of a request and response

This ensures that when a user wants to create a post, the request will only go through if it has a title and content in the body

Request and response should be in the defined model/schema


SQLAlchemy models: Responsible for defining the columns of the post table within postgres. Used to create, query, update the entries in the database    


Pydantic only works with dictionaries, not sqlalchemy models