import requests     # requests library will allow you to send http requests
from token2 import ACCESS_TOKEN
from textblob import TextBlob    # provide access to common text-processing operations
from textblob.sentiments import NaiveBayesAnalyzer  # returns its result as a named tuple of the form: Sentiment(classification, p_pos, p_neg).
import urllib      # provides a high-level interface for fetching data across the World Wide Web
import colorama   # provide color to the text output
from colorama import Fore,Back, Style  # for style of background and foreground
colorama.init()  # initialize colorama in application

# sandbox user : "jahnvee.sharma"
# friend in sandbox: "shiwani314"
# keyword to search: Python


BASE_URL = 'https://api.instagram.com/v1/'
lists=[]

# list with some default location names and latitude & longitude
location=[
    {
        "name":"Radaur",
        "Lat":"30.0272",
        "Long":"77.1493"
    },
    {
        "name":"Chandigarh",
        "Lat":"30.7333",
        "Long":"76.7794"
    },
    {
        "name":"Mohali",
        "Lat":"30.7046",
        "Long":"76.7179"
    },
    {
        "name":"Yamuna Nagar",
        "Lat":"30.1290",
        "Long":"77.2674"
    },
    {
        "name":"New Delhi",
        "Lat":"28.6139",
        "Long":"77.2090"
    }
        ]


#function declaration to get information about the owner of access token
def self_info():
  request_url = (BASE_URL + "users/self/?access_token=%s") % (ACCESS_TOKEN)
  user_info = requests.get(request_url).json()
  if user_info['meta']['code']==200:
     if len(user_info['data']):
         #display details of user
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
    user_info = requests.get(request_url).json() #retrun the json object as response
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            id_no = user_info['data'][0]['id']
            return id_no
        else:
            return None
    else:
        print 'received code is other than 200,That means your request is unsuccessful'
        exit()


# function will validate the users if their accounts actually exist!
def user_data(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:     # when no user with provided username exist
        print 'User does not exist!'
        exit()
    else:
        request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, ACCESS_TOKEN)
        user_info = requests.get(request_url).json() # response of json object
        if user_info['meta']['code'] == 200: # when request is successful code 200 is received
            if len(user_info['data']): # condition will be true when some data is present
                # display details of user
                print"Username: %s" % (user_info['data']['username'])
                print "followers: %s" % (user_info['data']['counts']['followed_by'])
                print "No. of people in following: %s" % (user_info['data']['counts']['follows'])
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
            image_name = user_med['data'][0]['id'] + ".jpeg"  # image id saved with jpeg extension
            image_url = user_med['data'][0]['images']['standard_resolution']['url']  # to get the url of the post
            urllib.urlretrieve(image_url, image_name)  # retrieve post
            message="image download Successful!"
            print "%s" % (Back.GREEN + Fore.LIGHTWHITE_EX + message)

            print (Style.RESET_ALL)
        else:
            message = "No data present!!"
            print "%s" % (Back.RED+Fore.LIGHTWHITE_EX + message)

            print (Style.RESET_ALL)
            exit()
    else:
        print"status code recieved is other than 200"
    return None


# function to download recent post of the user
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:  # when no user exist with provided username
        print 'User does not exist!'
        exit()
    else:
        request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id,ACCESS_TOKEN)
        user_med = requests.get(request_url).json()
        if user_med['meta']['code'] == 200:
            if len(user_med['data']):
                image_name = user_med['data'][0]['id'] + ".jpeg"  # latest post name
                image_url = user_med['data'][0]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)  # retrieve the post by ts name and url
                message="image download Successful!"
                print "%s" % (Back.GREEN+Fore.LIGHTWHITE_EX + message)  # background of text will be green & text color will be white
                print (Style.RESET_ALL)  # further output won't get affected by the color of previous text
            else:
                message="No data present!!"
                print "%s" % (Back.RED + Fore.LIGHTWHITE_EX + message)   # background of text will be red & text color will be white
                print (Style.RESET_ALL)    # further output won't get affected by the color of previous text
                exit()
        else:
            print"status code recieved is other than 200"
        return None


# function declaration to get user's post with least likes
def get_user_post1(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    else:
            request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id, ACCESS_TOKEN)
            user_med = requests.get(request_url).json()
            if user_med['meta']['code'] == 200:
                if len(user_med['data']):
                    for x in range(0, len(user_med["data"])):
                        num = user_med["data"][x]["likes"]["count"]  # count the number of likes on post
                        lists.append(num)  # add the number in list
                    y = lists.index(min(lists))  # retrieve the index of the smallest number in list
                    image_name = user_med['data'][y]['id'] + ".jpeg"  # retrieve id of the post with least likes
                    image_url = user_med['data'][y]['images']['standard_resolution']['url']
                    urllib.urlretrieve(image_url, image_name)
                    message = "image download Successful!"
                    print "%s" % (Back.GREEN + Fore.LIGHTWHITE_EX + message)  # text with green background and white foreground
                    print (Style.RESET_ALL)  # reset all the styles done using "colorama"
                else:
                    message = "No data present!!"
                    print "%s" % (Back.RED + Fore.LIGHTWHITE_EX+ message)
                    print (Style.RESET_ALL)
                    exit()
            else:
                print"status code recieved is other than 200"
            return None


# function declaration to get the post of the user with particular text in its caption
def get_user_post2(insta_username):
        user_id = get_user_id(insta_username)
        if user_id == None:
            print 'User does not exist!'
            exit()
        else:
            request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id, ACCESS_TOKEN)
            user_med = requests.get(request_url).json()
            if user_med['meta']['code'] == 200:
                keyword = raw_input("what are you searching for ? =")  # take keyword as input that user is searching in post captions
                for ids in range(0, len(user_med["data"])):  # for all the posts
                    if len(user_med["data"][ids]["caption"]):
                        caption_text = str(user_med["data"][ids]["caption"])  # retrieve caption of the post
                        comment = caption_text.split(" ")  # split caption text to form a list
                        if keyword in comment:  # this will search keyword in the list "comment"
                            print "keyword found in post"
                            image_name = user_med['data'][ids]['id'] + ".jpeg"  # post which have keyword in caption
                            image_url = user_med['data'][ids]['images']['standard_resolution']['url']
                            urllib.urlretrieve(image_url, image_name)
                            message = "image download Successful!"
                            print "%s" % (Back.GREEN + Fore.LIGHTWHITE_EX + message)
                            print (Style.RESET_ALL)
                        else:
                            message = "Keyword not found!!"
                            print "%s" % (Back.RED + Fore.LIGHTWHITE_EX + message)
                            print (Style.RESET_ALL)
                    else:
                        message = "This post doesn't have any caption!!"
                        print "%s" % (Back.RED + Fore.LIGHTWHITE_EX + message)
                        print (Style.RESET_ALL)

            else:
                print"status code recieved is other than 200"
            return None


# function declaration to get the recently liked post by the user
def get_user_post3():
    request_url = (BASE_URL + "users/self/media/liked?access_token=%s") % (ACCESS_TOKEN)   # url to get recently liked media by user
    user_med = requests.get(request_url).json()
    if user_med['meta']['code'] == 200:
        if len(user_med['data']):
            like_post = user_med['data'][0]['id'] + ".jpeg"  # as recent post will be on 0 index
            image_url = user_med['data'][0]['images']['standard_resolution']['url']  # url of the post
            urllib.urlretrieve(image_url, like_post)  # retrieve the post with provided name and url
            print Back.GREEN+Fore.LIGHTWHITE_EX+"image download Successful!"
            print (Style.RESET_ALL)
        else:
            print Back.RED+Fore.LIGHTWHITE_EX+"No data present!!"
            print (Style.RESET_ALL)
            exit()
    else:
        print"status code recieved is other than 200"
    return None


# function declaration to get the id of recent post of user
def get_media_id(insta_username):
    user_id = get_user_id(insta_username)  # save the value of id returned by function get_user_id in user_id variable
    if user_id == None:  # when user_id is null
        print 'User does not exist!'
        exit()
    else:   # when user id is there
        request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id, ACCESS_TOKEN)  # this url need user_id and access_token
        user_med = requests.get(request_url).json()
        if user_med['meta']['code'] == 200:
            if len(user_med['data']):
                media_id = user_med['data'][0]['id']
                return media_id
            else:
                print"No data received from this user's post "
        else:
            return None


# function to get number of comments on post of owner of access token
def count_comment():
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % ACCESS_TOKEN
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:

        if len(user_info['data']):
            print "number of comments on recent post are = %s " % (user_info['data'][0]['comments']['count'])  # count number of comments
        else:
            print"user doesn't exist!"
    else:
        print"status code other than 200 received!"


# function to get number of comments on the recent post of the user
def count_comment_user(insta_username):
    user_id=get_user_id(insta_username)
    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print "number of comments on recent post are = %s " % (user_info['data'][0]['comments']['count'])
        else:
            print"user doesn't exist!"
    else:
        print"status code other than 200 received!"


# function declaration to get a list of user who have liked the recent post
# the list will include likes of only those users' posts who are already in the friend list of user in Sandbox mode
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
                    item_number = item_number+1
            else:
                print"No data present for this post!"

        else:
            "status code other than 200 received"


# function to like a post of another user
# function will include likes on only those users's post who are already in the friend list of user in Sandbox mode
def like_a_post(insta_username):
    media_id = get_media_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)  # url to get media
    payload = {"access_token": ACCESS_TOKEN}  # to carry information on network
    print 'POST request url : %s' % request_url
    post_a_like = requests.post(request_url, payload).json()  # requests that a web server accept the data enclosed in the body of the request message
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


# function declaration to get a list of comment on user's post
# the list will include comments of only those users' posts who are already in the friend list of user in Sandbox mode
def get_comment_list(insta_username):
    media_id = get_media_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,ACCESS_TOKEN)
    comment_list = requests.get(request_url).json()
    item = 0
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            print "media id = %s" % media_id  # print media
            for users in range(0,len(comment_list['data'])):
                print"%d.%s : %s" % (item + 1,comment_list['data'][users]['from']['username'], comment_list['data'][users]['text'])
                item=item+1
        else:
            print"there is no comment on this post!"
    else:
        print "Your don't have access to the comment list of this post. Try again!"


# function declaration to make a comment on recent post of the user
# the list will include comment on only those users' post who are already in the friend list of user in Sandbox mode
def post_a_comment(insta_username):
    media_id = get_media_id(insta_username)
    comment_text = raw_input("Your comment: ")
    text=comment_text.split(" ")
    if comment_text != "":
        if len(text)>50:
            print "Unable to add a comment with length more than 50 words!!"
        else:
            payload = {"access_token": ACCESS_TOKEN, "text": comment_text}
            request_url = (BASE_URL + 'media/%s/comments') % media_id
            print 'POST request url : %s' % request_url

            make_comment = requests.post(request_url, payload).json()
            if make_comment['meta']['code'] == 200:
                print "Successfully added a new comment on media id =%s" % media_id
            else:
                print "Unable to add comment. Try again!"
    else:
        print"empty comment cann't be posted!!"


# function declaration to delete an existing comment from user's post
def delete_negative_comment(insta_username):
    media_id = get_media_id(insta_username)  # get recent post id of user
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']  # get text of comments

                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())  # analysis of comments by TextBlob
                if (blob.sentiment.p_neg > blob.sentiment.p_pos ):  # p_pos and p_neg are default attributes of sentiment to calculate positive and negative strength in text
                    print 'Negative comment : %s' % comment_text
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()  # delete request to delete the item given in argument

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive or neutral comment : %s\n' % comment_text
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


# function declaration to post targeted comments based on tags in caption
def post_targeted_comments():
    tag_name = raw_input("enter the tag you want to search posts of = ")
    request_url = (BASE_URL + "tags/%s/media/recent?access_token=%s") % (tag_name, ACCESS_TOKEN)
    post_tag = requests.get(request_url).json()
    if post_tag['meta']['code'] == 200:
        comment_text = raw_input("Your comment: ")  # take tag as input
        payload = {"access_token": ACCESS_TOKEN, "text": comment_text}
        for ids in range(0, len(post_tag["data"])):
            media_id = post_tag["data"][ids]["id"]
            user_name = post_tag["data"][ids]["user"]["username"]
            print "%s media of %s user"%(media_id,user_name)
            request_url = (BASE_URL + 'media/%s/comments') % (media_id)  # request url to make a comment on post
            print 'POST request url : %s' % (request_url)
            make_comment = requests.post(request_url, payload).json()  # web server accept the data enclosed in the body of the request message
            if make_comment['meta']['code'] == 200:
                print Back.GREEN+Fore.LIGHTWHITE_EX+"Successfully added a new comment!"
                print (Style.RESET_ALL)
            else:
                print Back.RED+Fore.LIGHTWHITE_EX+ "Unable to add comment. Try again!"
                print (Style.RESET_ALL)
    else:
        print "Status code recieved is other than 200!"


# function declaration for targeted comments based on caption
def lat_lon(lat1,long1):
    request_url = (BASE_URL + "media/search?lat=%f&lng=%f&access_token=%s&distance=5000") % (lat1, long1, ACCESS_TOKEN)
    locate = requests.get(request_url).json()
    if locate['meta']['code'] == 200:
        if len(locate['data']):
            keyword = raw_input("what are you searching for ? =") #keyword input by user that he want to search post with
            comment_text = raw_input("Your comment: ")
            comment=comment_text.split(" ")
            if comment_text!= "" and len(comment) != 0:
                for ids in range(0, len(locate["data"])):
                    if len(locate['data'][ids]["caption"]["text"]):
                        caption_text = str(locate["data"][ids]["caption"]["text"])  # retrieve caption text of the post
                        comment = caption_text.split(" ")  # split the comment text and store them in a list "comment"
                        if keyword in comment:
                            print "keyword found in post"
                            media_id = locate["data"][ids]["id"]
                            payload = {"access_token": ACCESS_TOKEN, "text": comment_text}  # take comment text to network
                            request_url = (BASE_URL + 'media/%s/comments') % media_id
                            make_comment = requests.post(request_url, payload).json()  # post request to make a comment on the post
                            if make_comment['meta']['code'] == 200:
                                print "Successfully added a new comment!"
                            else:
                                print "Unable to add comment. Try again!"
                        else:
                            print"your searched keyword in not in the recent media from this location"
            else:
                print" Comment text is empty! "
        else:
            print "no data present"
    else:
        print "status code other than 200 received"


# function declaration to get the location latitude and longitude of user's choice and pass these values for targeted comment
def get_loc():
    item = 0
    for num in range(0, len(location)):  # length of list "location"
        print "%d.%s" % (item + 1, location[num]["name"])  # print the value of name key from sub-directory of list items
        item = item + 1

    choice = raw_input("select your area number =")
    if choice == "1":
        lat1 = float(location[0]["Lat"])
        long1 = float(location[0]["Long"])
        lat_lon(lat1, long1)      # call function post comment based on location latitude and longitude provided in arguments
    elif choice == "2":
        lat1 = float(location[1]["Lat"])
        long1 = float(location[1]["Long"])
        lat_lon(lat1, long1)
    elif choice == "3":
        lat1 = float(location[2]["Lat"])
        long1 = float(location[2]["Long"])
        lat_lon(lat1, long1)
    elif choice == "4":
        lat1 = float(location[3]["Lat"])
        long1 = float(location[3]["Long"])
        lat_lon(lat1, long1)
    elif choice == "5":
        lat1 = float(location[4]["Lat"])
        long1 = float(location[4]["Long"])
        lat_lon(lat1, long1)
    else:
        print "Wrong input"
    return None


# function declaration to start the InstaBot
def start_bot():
    while True:  #loop will continue to execute till user enter the exit key (here its "l")
        print "\n"

        print "Select any option to proceed:\n"
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
            self_info()  # call function to get details of sandbox user
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username) > 0 and insta_username.isspace() == False:   # condition will be true when username is not null and there is no space in username
                if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):  # when stated symbols are encountered in username
                    print "Invalid entry. Please enter a Valid Name!"
                    insta_username = raw_input("Enter the username: ")
                    if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                        print "Invalid entry. Please try later!"
                        exit()  # exit when special symbols got ecountered again in username
                    else:
                        user_data(insta_username)
                else:
                    user_data(insta_username)
            else:
                message="invalid username!"
                print "%s"%(Back.RED+ Fore.LIGHTWHITE_EX  + message)
                print (Style.RESET_ALL)
        elif choice == "c":
            get_own_post()  # function calling to get the recent post of sandbox user
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            print "1. latest media of user"
            print "2. media with least likes"
            print "3. media with particular text as keyword"
            print "4. recently liked media by user"
            choose=raw_input("Choose medium to get post: ")   # take numeric input to choose from above list
            if choose=="1":
                if len(insta_username) > 0 and insta_username.isspace() == False:
                    if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):  # condition will be true when username is not null and there is no space in username
                        print "Invalid entry. Please enter a Valid Name!"
                        insta_username = raw_input("Enter the username: ")
                        if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                            print"invalid entry! try again later!"
                            exit()
                        else:
                            get_user_post(insta_username)
                    else:
                        get_user_post(insta_username)
                else:
                    message = "invalid username!"
                    print "%s" % (Back.RED+Fore.WHITE + message)
                    print (Style.RESET_ALL)
            elif choose=="2":
                if len(insta_username)>0 and insta_username.isspace()==False:  # condition will be true when username is not null and there is no space in username
                    if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                        print "Invalid entry. Please enter a Valid Name!"
                        insta_username = raw_input("Enter the username: ")
                        if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                            print"invalid entry! try again later!"
                            exit()
                        else:
                            get_user_post1(insta_username)
                    else:
                        get_user_post1(insta_username)
                else:
                    print "please enter a valid username!!"

            elif choose == "3":
                if len(insta_username) > 0 and insta_username.isspace() == False:   # condition will be true when username is not null and there is no space in username
                    if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                        print "Invalid entry. Please enter a Valid Name!"
                        insta_username = raw_input("Enter the username: ")
                        if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                            print"invalid entry! try again later!"
                            exit()
                        else:
                            get_user_post2(insta_username)
                    else:
                        get_user_post2(insta_username)
                else:
                    message = "invalid username!"
                    print "%s" % (Back.RED+Fore.LIGHTWHITE_EX + message)   # condition will be true when username is not null and there is no space in username
                    print (Style.RESET_ALL)
            elif choose=="4":
                get_user_post3()
            else:
                print"wrong input!"

        elif choice=="e":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username) > 0 and insta_username.isspace() == False:
                if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    print "Invalid entry. Please enter a Valid Name!"
                    insta_username = raw_input("Enter the username again: ")
                    if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                        print "Invalid entry. Please try later!"
                        exit()
                    else:
                        get_like_list(insta_username)
                else:
                    get_like_list(insta_username)
            else:
                print Fore.LIGHTWHITE_EX+Back.RED+"Please enter a valid username"
                print (Style.RESET_ALL)
        elif choice=="f":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username) > 0 and insta_username.isspace() == False:  # condition will be true when username is not null and there is no space in username
                if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    print "Invalid entry. Please enter a Valid Name!"
                    insta_username = raw_input("Enter the username: ")
                    if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                        print "Invalid entry. Please try later!"
                        exit()
                    else:
                        like_a_post(insta_username)
                else:
                    like_a_post(insta_username)
            else:
                print Fore.LIGHTWHITE_EX + Back.RED + "Please enter a valid username"
                print (Style.RESET_ALL)
        elif choice=="g":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username) > 0 and insta_username.isspace() == False:  # condition will be true when username is not null and there is no space in username
                if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    print "Invalid entry. Please enter a Valid Name!"
                    insta_username = raw_input("Enter the username: ")
                    if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                        print "Invalid entry. Please try later!"
                        exit()
                    else:
                        get_comment_list(insta_username)
                else:
                    get_comment_list(insta_username)
            else:
                print Fore.LIGHTWHITE_EX + Back.RED + "Please enter a valid username"
                print (Style.RESET_ALL)
        elif choice=="h":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username) > 0 and insta_username.isspace() == False:  # condition will be true when username is not null and there is no space in username
                if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    print "Invalid entry. Please enter a Valid Name!"
                    insta_username = raw_input("Enter the username: ")
                    if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                        print "Invalid entry. Please try later!"
                        exit()
                    else:
                        post_a_comment(insta_username)
                else:
                    post_a_comment(insta_username)
            else:
                print Fore.LIGHTWHITE_EX + Back.RED + "Please enter a valid username"
                print (Style.RESET_ALL)
        elif choice=="i":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username) > 0 and insta_username.isspace() == False:  # condition will be true when username is not null and there is no space in username
                if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    print "Invalid entry. Please enter a Valid Name!"
                    insta_username = raw_input("Enter the username: ")
                    if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                        print "Invalid entry. Please try later!"
                        exit()
                    else:
                        delete_negative_comment(insta_username)
                else:
                    delete_negative_comment(insta_username)
            else:
                print Fore.LIGHTWHITE_EX+ Back.RED + "Please enter a valid username"
                print (Style.RESET_ALL)
        elif choice == "j":
            post_targeted_comments()
        elif choice == "k":
            get_loc()
        elif choice == "l":
            exit()  #exit from application
        else:
            print "wrong choice"


print "Hey! Welcome to instaBot!"   # execution starts from here
start_bot()   # function calling to start the InstaBot