from ast import List
from tempfile import tempdir
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

def unique_posts(list_of_posts):
    postsSet = set()
    uniquePosts = list()
    while len(list_of_posts) > 0:
        posts = list_of_posts.pop()
        while len(posts) > 0:
            post = posts.pop()
            if post.id not in postsSet:
                postsSet.add(post.id)
                uniquePosts.append(post)
    
    return uniquePosts

def find_first_list(list_of_posts):
    first_index = 0
    first_created_at = list_of_posts[0][0].created_at
    first_id = list_of_posts[0][0].id
    for i in range(len(list_of_posts)):
        if list_of_posts[i][0].created_at <= first_created_at and list_of_posts[i][0].id <= first_id:
            first_created_at = list_of_posts[i][0].created_at
            first_id = list_of_posts[i][0].id
            first_index = i
    
    return first_index

def check_combine(list_of_posts):
    """
    En küçük created_at değerine sahip postun olduğu listenin index'ini bul
    daha sonra bulduğumuz bu liste küçükten büyüğe sırlandığında ilk liste olacak
    daha sonra bu listenin son elemanı ile geri kalan tüm listelerin ilk elemanlarını karşılaştırıyoruz
    eğer bir listenin ilk elemanı bulduğumuz en küçük listenin son elemanından büyükse bu iki listeyi birleştirebiliriz
    """
    combined_list = list()
    not_combined_list = list()
    checked_indexes = set()

    first_index = find_first_list(list_of_posts) # O(n)
    combined_list.append(list_of_posts[first_index])
    checked_indexes.add(first_index)

    while True:
        index = diff = None
        for i in range(len(list_of_posts)):
            if i in checked_indexes:
                continue

            post1 = list_of_posts[first_index][len(list_of_posts[first_index])-1]
            post2 = list_of_posts[i][0]

            diff_created_at = post1.created_at - post2.created_at

            if diff_created_at > 0:
                not_combined_list.append(list_of_posts[i])
                checked_indexes.add(i)
            elif diff is None or diff < diff_created_at:
                diff = diff_created_at
                index = i
                if diff in (0,1):
                    break

        if diff is None:
            break

        combined_list.append(list_of_posts[index])
        checked_indexes.add(index)
        first_index = index
    
    return combined_list, not_combined_list

def combine_posts(list_of_posts):
    combined_posts = list()

    while True:
        combined_list, not_combined_list = check_combine(list_of_posts) # less than O(n)

        if len(combined_list) > 0:
            combined_posts.append(unique_posts(combined_list)) # less than O(n)
            
            if len(not_combined_list) == 0:
                break

            list_of_posts = not_combined_list
        else:
            combined_posts.append(unique_posts(not_combined_list)) # less than O(n)
            break

    return unique_posts(combined_posts) # less than O(n)

def merge_posts_2(list_of_posts):
    combined_posts = combine_posts(list_of_posts) # less than O(n)

    return sorted(combined_posts, key=lambda post: (post.created_at, post.id), reverse=True) # n log(n)

def merge_posts(list_of_posts): # O(n*m) + O(n log(n))
    postsSet = set()
    uniquePosts = list()
    while len(list_of_posts) > 0:
        posts = list_of_posts.pop()
        while len(posts) > 0:
            post = posts.pop()
            if post.id not in postsSet:
                postsSet.add(post.id)
                uniquePosts.append(post)

    return sorted(uniquePosts, key=lambda post: (post.created_at, post.id), reverse=True) # n log (n)

def main():
    post_list = get_posts(1, [2,12,3])
    print("get_posts")
    print(post_list)

    merged_posts = merge_posts([[Post(4,"description",1,"image",123),Post(3,"description",1,"image",134)], [Post(2,"description",1,"image",124), Post(3,"description",1,"image",134)]])
    print("merge_posts")
    print(merged_posts)

    merged_posts_2 = merge_posts_2([[Post(4,"description",1,"image",123),Post(3,"description",1,"image",134)], [Post(2,"description",1,"image",124), Post(3,"description",1,"image",134)]])
    print("merge_posts_2")
    print(merged_posts_2)

if __name__ == "__main__":
    main()
    