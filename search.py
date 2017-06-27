import requests
import urllib
from token import access_token

BASE_URL = 'https://api.instagram.com/v1/'

#function to get user id when a valid username is provided
def user_id(insta_username):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, access_token)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()
  if user_info['meta']['code'] == 200:
      if len(user_info['data']):
          info= user_info['data'][0]['id']
          return info
      else:
          return None
  else:
      print 'received code is other than 200,So your request is unsuccessful'
      exit()

#function will validate the users if their accounts actually exist!
def user_data(insta_username):
    user_ids = user_id(insta_username)
    if user_ids == None:
        print 'User does not exist!'
        exit()
    else:
        request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_ids, access_token)
        #print 'GET request url : %s' % (request_url)
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

#function to get the data on the recent post of user
def recent_med(insta_username):
    user_ids=user_id(insta_username)
    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_ids,access_token)
   # print "GET request url : %s" % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print "number of comments on recent post are = %s " % (user_info['data'][0]['comments']['count'])
        else:
            print"user doesn't exist!"
    else:
        print"status code other than 200 recieved!"



#function to download recent post of access token holder
def get_post():
        request_url=(BASE_URL +"users/self/media/recent/?access_token=%s")%(access_token)
        user_med=requests.get(request_url).json()
        if user_med['meta']['code']==200:
            if len(user_med['data']):
                image_name=user_med['data'][0]['id']+".jpeg"
                image_url = user_med['data'][0]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url,image_name)
                print"image download Successful!"
            else:
                print"user not found!!"
                exit()
        else:
            print"status code recieved is other than 200"
        return None

#function to download recent post of the user
def get_user_post(insta_username):
    user_ids = user_id(insta_username)
    if user_ids == None:
        print 'User does not exist!'
        exit()
    else:
        request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_ids,access_token)
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


#recent_med('jahnvee.sharma')
get_post()
#get_user_post('pooja_bharti_arya')

