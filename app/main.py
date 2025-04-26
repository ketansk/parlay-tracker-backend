from fastapi import FastAPI
from ariadne.asgi import GraphQL
from app.graphql.resolvers.resolvers import query, mutation
from ariadne import make_executable_schema, snake_case_fallback_resolvers
from dotenv import load_dotenv

load_dotenv()

type_defs = open("app/graphql/schema.graphql").read()
schema = make_executable_schema(type_defs, [query, mutation], snake_case_fallback_resolvers)

app = FastAPI()
app.mount("/graphql", GraphQL(schema, debug=True))
