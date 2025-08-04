from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import cast, List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# --------------------------------------------create a post----------------------

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})")
    # #above method will technically work but is vunerable to sql injection
    # cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''', (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    # print(post.model_dump())
    # new_post = models.Tweet(title=post.title, content=post.content, published=post.published)
    print(user_id)
    new_post = models.Tweet(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# --------------------------------------------get all posts----------------------

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Tweet).all()
    # print(posts)
    return posts

# --------------------------------------------get latest post----------------------
# @router.get("/posts/latest")       # important : order of routes matters here
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"data": [post]}

# --------------------------------------------get a post by id----------------------
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):          # automatic validation and good error message if validation fails instead of showing crashing error messages
    # # print(id)
    # # print(type(id))
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''', (id,))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    # return {"data": post}
    
    post = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    return post
    



# --------------------------------------------delete----------------------

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (id,))
    # delete_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Tweet).filter(models.Tweet.id == id)
    post = post_query.first()
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# --------------------------------------------create a post----------------------

@router.put("/{id}", status_code=status.HTTP_200_OK,response_model=schemas.PostResponse)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # print(post)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # return {"data": updated_post}

    post_query = db.query(models.Tweet).filter(models.Tweet.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    
    # post_query.update({'title':'hey this is my updated title', 'content': 'this is my updated content'}, synchronize_session=False)
    post_query.update(cast(dict, new_post.model_dump()), synchronize_session=False)
    db.commit()
    updated_post = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    return updated_post

# --------------------------------------------test route for orm----------------------


@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Tweet).all()
    print(posts)
    return {"data": posts}