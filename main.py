import requests
import urllib
from token import access_token


BASE_URL = 'https://api.instagram.com/v1/'

def self_info():
  request_url = (BASE_URL + "users/self/?access_token=%s") % (access_token)
  #print "GET request url : %s" % (request_url)
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

#function to check data on owner of access token
def recent_media():
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % (access_token)
    #print "GET request url : %s" % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print "number of comments on recent post are = %s "%(user_info['data'][0]['comments']['count'])
        else:
            print"user doesn't exist!"
    else:
        print"status code other than 200 recieved!"


#self_info()
recent_media()
