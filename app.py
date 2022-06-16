from ast import List
from db.database import Post
from followQueries import is_followed
from likeQueries import is_liked
from postQueries import get_post_list
from userQueries import get_user

def get_posts(user_id, post_ids):
    if len(post_ids) == 0:
        return []

    response:List[Post] = list()
    post_list = get_post_list(post_ids)
    for post_id in post_ids:
        if post_id not in post_list:
            response.append(None)
            continue

        post = post_list[post_id]
        post.liked = is_liked(user_id, post.id)
        post.owner = get_user(post.user_id)
        post.owner.followed = is_followed(user_id, post.owner.id)

        response.append(post)

    return response

def merge_posts(list_of_posts):
    postsSet = set()
    uniquePosts = list()
    while len(list_of_posts) > 0:
        posts = list_of_posts.pop()
        while len(posts) > 0:
            post = posts.pop()
            if post.id not in postsSet:
                postsSet.add(post.id)
                uniquePosts.append(post)

    return sorted(uniquePosts, key=lambda post: (post.created_at, post.id), reverse=True)

def main():
    post_list = get_posts(1, [2,12,3])
    print("get_posts")
    print(post_list)

    merged_posts = merge_posts([[Post(4,"description",1,"image",123),Post(3,"description",1,"image",134)], [Post(2,"description",1,"image",124), Post(3,"description",1,"image",134)]])
    print("merge_posts")
    print(merged_posts)

if __name__ == "__main__":
    main()
    