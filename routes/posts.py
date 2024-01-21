from fastapi import APIRouter, HTTPException

from models.post import UserPost, UserPostIn, Comment, CommentIn

router = APIRouter()
post_table = {}
comments_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


@router.post("/posts", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.dict()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


@router.get("/post/{post_id}/comments", response_model=list[Comment])
async def get_comments_from_a_post(post_id: int):
    return [
        comment for comment in comments_table.values() if comment['post_id'] == post_id
    ]


@router.post('/comments', response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="item not found")

    data = comment.dict()
    last_record_id = len(comments_table)
    new_comment = {**data, "id": last_record_id}
    comments_table[last_record_id] = new_comment
    return new_comment


@router.get('/posts', response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())
