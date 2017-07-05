import requests
from token2 import ACCESS_TOKEN
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import urllib

BASE_URL = 'https://api.instagram.com/v1/'

#sandbox user : "jahnvee.sharma"
# friend in sandbox: "shiwani314"

def self_info():
  request_url = (BASE_URL + "users/self/?access_token=%s") % (ACCESS_TOKEN)
  user_info = requests.get(request_url).json()
  if user_info['meta']['code']==200:
     if len(user_info['data']):
         print "user name=%s"%(user_info['data']['username'])
         print "Full name =%s"%(user_info['data']['full_name'])
         print "Number of posts=%d"%(user_info['data']['counts']['media'])
         print "Number of followers=%d"%(user_info['data']['counts']['followed_by'])
         print"following = %d"%(user_info['data']['counts']['follows'])

     else:
         print"No Such user exist!"
  else:
      print"Error Encountered!!Rrequest not successful"





# function to get user id when a valid username is provided
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            info = user_info['data'][0]['id']
            return info
        else:
            return None
    else:
        print 'received code is other than 200,So your request is unsuccessful'
        exit()

# function will validate the users if their accounts actually exist!
def user_data(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    else:
        request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, ACCESS_TOKEN)
        user_info = requests.get(request_url).json()
        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                print"Username: %s" % (user_info['data']['username'])
                print "followers: %s" % (user_info['data']['counts']['followed_by'])
                print "No. of people you are following: %s" % (user_info['data']['counts']['follows'])
                print "No. of posts: %s" % (user_info['data']['counts']['media'])
            else:
                print "no data found!!"
        else:
            print "Status code other than 200 received!"




# function to download recent post of access token holder
def get_own_post():
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % (ACCESS_TOKEN)
    user_med = requests.get(request_url).json()
    if user_med['meta']['code'] == 200:
        if len(user_med['data']):
            image_name = user_med['data'][0]['id'] + ".jpeg"
            image_url = user_med['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print"image download Successful!"
        else:
            print"user not found!!"
            exit()
    else:
        print"status code recieved is other than 200"
    return None


#function to download recent post of the user
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    else:
        request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id,ACCESS_TOKEN)
        user_med = requests.get(request_url).json()
        if user_med['meta']['code'] == 200:
            if len(user_med['data']):
                image_name = user_med['data'][0]['id'] + ".jpeg"
                image_url = user_med['data'][0]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)
                print"image download Successful!"
            else:
                print"user not found!!"
                exit()
        else:
            print"status code recieved is other than 200"
        return None


#function declaration to get the id of recent post of user
def get_media_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    else:
        request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id, ACCESS_TOKEN)
        user_med = requests.get(request_url).json()
        if user_med['meta']['code'] == 200:
            if len(user_med['data']):
                media_id = user_med['data'][0]['id']
                return media_id
            else:
                print"You don't have access to this media id "
        else:
            return None




# function to check data of owner of access token
def recent_media():
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % (ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print "number of comments on recent post are = %s " % (user_info['data'][0]['comments']['count'])
        else:
            print"user doesn't exist!"
    else:
        print"status code other than 200 recieved!"


#function to get the data on the recent post of user
def recent_med(insta_username):
    user_id=get_user_id(insta_username)
    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print "number of comments on recent post are = %s " % (user_info['data'][0]['comments']['count'])
        else:
            print"user doesn't exist!"
    else:
        print"status code other than 200 recieved!"





#function declaration to get a list of user who have liked the recent post
def get_like_list(insta_username):
    media_ids=get_media_id(insta_username)
    if media_ids == None:
        print 'request to get media ID unsuccessful!'
        exit()
    else:
        request_url = (BASE_URL + "media/%s/likes?access_token=%s") % (media_ids,ACCESS_TOKEN)
        user_med = requests.get(request_url).json()
        item_number=0
        if user_med['meta']['code'] == 200:
            if len(user_med['data']):
                for users in range(0, len(user_med['data'])):
                    print"%d . %s" %(item_number+1,user_med['data'][users]['username'])
                    item_number=item_number+1
            else:
                print"this user doesn't exist"

        else:
            "status code other than 200 received"



#function to like a post of another user
def like_a_post(insta_username):
    media_id = get_media_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

#function declaration to get a list of comment on user's post
def get_comment_list(insta_username):
    media_id = get_media_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,ACCESS_TOKEN)
    comment_list = requests.get(request_url).json()
    item = 0
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            for users in range(0,len(comment_list['data'])):
                print"%d.%s : %s" % (item + 1,comment_list['data'][users]['from']['username'], comment_list['data'][users]['text'])
                item=item+1
        else:
            print"there is no comment on this post!"
    else:
        print "Your don't have access to the comment list of this user. Try again!"

#function declaration to post a comment
def post_a_comment(insta_username):
    media_id = get_media_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"

#function declaration to get the id of comment
def get_comment_id(insta_username):
    media_id = get_media_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, ACCESS_TOKEN)
    comment_list = requests.get(request_url).json()
    item = 0
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            for users in range(0, len(comment_list['data'])):
                print"%d.%s : %s" % (item + 1, comment_list['data'][users]['id'], comment_list['data'][users]['text'])
                item = item + 1
            delete_comment=raw_input("enter the id of the commnet that you want to delete= ")
            return delete_comment
        else:
            print"there is no comment on this post!"
    else:
        print "Your don't have access to the comment list of this user. Try again!"


#function declaration to delete an existing comment from user's post
def delete_negative_comment(insta_username):
    media_id = get_media_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']

                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'



#function declaration to post targeted comments based on caption
def post_targeted_comments():
    tag_name = raw_input("enter the tag you want to search posts of = ")
    request_url = (BASE_URL + "tags/%s/media/recent?access_token=%s") % (tag_name, ACCESS_TOKEN)
    post_tag = requests.get(request_url).json()
    if post_tag['meta']['code'] == 200:
        comment_text = raw_input("Your comment: ")
        payload = {"access_token": ACCESS_TOKEN, "text": comment_text}
        for ids in range(0, len(post_tag["data"])):
            media_id = post_tag["data"][ids]["id"]
            user_name = post_tag["data"][ids]["user"]["username"]
            print "%s media of %s user"%(media_id,user_name)
            request_url = (BASE_URL + 'media/%s/comments') % (media_id)
            print 'POST request url : %s' % (request_url)
            make_comment = requests.post(request_url, payload).json()
            if make_comment['meta']['code'] == 200:
                print "Successfully added a new comment!"
            else:
                print "Unable to add comment. Try again!"


# using media search
def lat_lon():
    lat2 = 30.0272
    long2 = 77.1493
    request_url = (BASE_URL + "media/search?lat=%f&lng=%f&access_token=%s&distance=5000") % (lat2, long2, ACCESS_TOKEN)
    locate = requests.get(request_url).json()
    if locate['meta']['code'] == 200:
        if len(locate['data']):
            keyword = raw_input("what are you searching for ? =")
            comment_text = raw_input("Your comment: ")
            for ids in range(0, len(locate["data"])):
                    caption_text = str(locate["data"][ids]["caption"]["text"])
                    comment = caption_text.split(" ")

                    if keyword in comment:
                        print "keyword found in post"
                        media_id = locate["data"][ids]["id"]
                        payload = {"access_token": ACCESS_TOKEN, "text": comment_text}
                        request_url = (BASE_URL + 'media/%s/comments') % (media_id)
                        make_comment = requests.post(request_url, payload).json()
                        if make_comment['meta']['code'] == 200:
                            print "Successfully added a new comment!"
                        else:
                            print "Unable to add comment. Try again!"
                    else:
                        print"your searched keyword in not in the recent media from this location"
        else:
            print "no data present"
    else:
        print "status code other than 200 received"



def start_bot():
    while True:
        print "\n"
        print "Hey! Welcome to instaBot!"
        print "Select any option to proceed:"
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like a Post\n"
        print "g.Get Comment List\n"
        print "h.Leave a comment on a post\n"
        print "i.Delete negative comments\n"
        print "j.targeted comments based on tags\n"
        print "k.targeted comments based on caption\n"
        print "l.Exit\n"


        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            user_data(insta_username)
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"
                insta_username = raw_input("Enter the username: ")
            else:
                print "That's a valid username"
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"
                insta_username = raw_input("Enter the username: ")
            else:
                print "That's a valid username"
        elif choice=="e":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"
                insta_username = raw_input("Enter the username: ")
            else:
                print "That's a valid username"
        elif choice=="f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"
                insta_username = raw_input("Enter the username: ")
            else:
                print "That's a valid username"
        elif choice=="g":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"
                insta_username = raw_input("Enter the username: ")
            else:
                print "That's a valid username"
        elif choice=="h":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"
                insta_username = raw_input("Enter the username: ")
            else:
                print "That's a valid username"
        elif choice=="i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"
                insta_username = raw_input("Enter the username: ")
            else:
                print "That's a valid username"
        elif choice=="j":
            post_targeted_comments()
        elif choice == "k":
            lat_lon()
        elif choice == "l":
            exit()
        else:
            print "wrong choice"



start_bot()