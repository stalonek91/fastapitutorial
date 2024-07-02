


@app.post("/users/add", response_model=schemas.User_return, status_code=status.HTTP_201_CREATED)
def users_add(user: schemas.User_create, db: Session = Depends(get_sql_db)):

    try:
        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password

        new_user = models.User(
            **user.model_dump()
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

    return new_user