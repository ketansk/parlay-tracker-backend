from fastapi import FastAPI
from ariadne.asgi import GraphQL
from resolvers import query, mutation
from ariadne import make_executable_schema
from dotenv import load_dotenv

load_dotenv()

type_defs = open("schema.graphql").read()
schema = make_executable_schema(type_defs, [query, mutation])

app = FastAPI()
app.mount("/graphql", GraphQL(schema, debug=True))
