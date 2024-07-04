from pydantic import BaseModel, Field
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, Request
from typing import Union, Optional, List, Dict
import random
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os
from . import models, database, schemas, utils
from .database import engine, get_sql_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

models.base.metadata.create_all(bind=engine)



#TODO: youtube: 6:45:0

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
