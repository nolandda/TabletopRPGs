#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import pprint
import time
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def print_response(response):
  pp = pprint.PrettyPrinter(indent=2)
  for curitm in response['items']:
    if curitm['id']['kind'] == 'youtube#video':
      pp.pprint(curitm['id']['videoId'])
    else:
      pp.pprint('NoIdType = ' + curitm['id']['kind'])

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def search_list_by_keyword(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.search().list(
    **kwargs
  ).execute()

  return response;


def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

def log_ids(response, afile):
  #pp = pprint.PrettyPrinter(indent=2)
  for curitm in response['items']:
    if curitm['id']['kind'] == 'youtube#video':
      afile.write(curitm['id']['videoId'] + '\n')
    else:
      print('Error: Bad Id Type ' + curitm['id']['kind'])
      #pp.pprint('NoIdType = ' + curitm['id']['kind'])
  afile.flush()


  
if __name__ == '__main__':
  VID_COUNT_GOAL = 120000
  wordset = load_words()

  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  client = get_authenticated_service()

  total_vids = 0
  vid_count = 0
  with open('video_ids.txt', 'a') as vid_file:
    for curword in wordset:
      if len(curword) < 5:
        print('--> skipping [' + curword + ',' + str(len(curword)) + ']')
        continue
      else:
        print('-----------------[' + curword + ',' + str(len(curword)) + ']-----------------')

        theset = search_list_by_keyword(client,
                                        part='snippet',
                                        maxResults=50,
                                        q=curword,
                                        type='video')
        vid_count = len(theset['items'])
        print('Logging ' + str(vid_count) + ' ids')
        log_ids(theset, vid_file)
        total_vids += vid_count
      if total_vids > VID_COUNT_GOAL:
        break
      time.sleep(5)

