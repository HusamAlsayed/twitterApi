import hmac
import sys
import urllib.parse as urllib_parse
from urllib.parse import urlencode
import hashlib
import base64
import time
from random import getrandbits
import requests

class Twitter:
    def __init__(self,consumer_key,consumer_secret,access_token, access_secret_token):
        '''
            currently only version 1.1 standard are supported .
        '''
        self.endpoints = 'https://api.twitter.com/1.1'
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret_token = access_secret_token


    def get_tweets(self,query,max_result = 100,result_type = 'recent',language = 'en'):
        url = self.endpoints + '/search/tweets.json'
        encodes = self.encode_params(url,'GET',{'q':query,'count':max_result,'result_type' : result_type,'lang':language})
        return requests.get(f'{url}?{encodes}')


    def encode_params(self, base_url, method, params):
        params = params.copy()

        params['oauth_token'] = self.access_token
        params['oauth_consumer_key'] = self.consumer_key
        params['oauth_signature_method'] = 'HMAC-SHA1'
        params['oauth_version'] = '1.0'
        params['oauth_timestamp'] = str(int(time.time()))
        params['oauth_nonce'] = str (getrandbits(64))

        enc_params = self.urlencode_noplus(sorted(params.items()))

        key = self.consumer_secret + "&" + urllib_parse.quote(self.access_secret_token, safe='~')

        message = '&'.join(
            urllib_parse.quote(i, safe='~') for i in [method.upper(), base_url, enc_params])

        signature = (base64.b64encode(hmac.new(
                    key.encode('ascii'), message.encode('ascii'), hashlib.sha1)
                                      .digest()))
        return enc_params + "&" + "oauth_signature=" + urllib_parse.quote(signature, safe='~')


    def urlencode_noplus(self,query):
        return urlencode(query, safe='~').replace("+", "%20")
