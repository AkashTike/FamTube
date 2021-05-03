from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.views import APIView
from FamTube.models import *
from FamTube.utils import *
import re
from django.db.models import Q
from django.shortcuts import render
from apiclient.discovery import build
import json
import datetime
from FamTube.constants import API_KEYS
from django.core.paginator import Paginator

import logging
import sys
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import traceback

from rest_framework.status import (HTTP_200_OK,
                                   HTTP_202_ACCEPTED,
                                   HTTP_208_ALREADY_REPORTED,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_412_PRECONDITION_FAILED,
                                   HTTP_409_CONFLICT,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_403_FORBIDDEN,
                                   HTTP_500_INTERNAL_SERVER_ERROR)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

# PAGE SECTION BELOW

def DashboardPage(request):
    return render(request,'FamTube/dashboard.html')

# API SECTION BELOW

class GetAllVideosAPI(APIView):

    """
        
    This API returns all the stored videos for a particular search query "news"

    Request Parameters: **page**

    Request Example:

        {
            "page": 1
        }

    Note: **page** is an positive integer
    
    
    Response: **videos** and **next_page**

    Response Example:

        {
            "videos": [
                {
                    "published_at": "2021-05-03 11:11:36",
                    "title": "ሰኞ ሚያዝያ 25 /2013 የስፖርት ዜና  Ethiopian sport news today | arif sport news mensur abdulkeni",
                    "description": "",
                    "channel_title": "Arif Sport Ethiopia",
                    "thumbnail_url": "https://i.ytimg.com/vi/z1adUASNh_E/default.jpg"
                },
                ...
                ...
                ...
            ],
            "next_page" : true
        }

    Note: **videos** list will be of length less than equal to 50. 
    **next_page** will be false when there are would be no more pages left.

    """

    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)

    def get(self, request, *args, **kwargs):

        response = {}
        status = HTTP_500_INTERNAL_SERVER_ERROR

        try:
            data = request.GET
            video_objects = Video.objects.all().order_by('-published_at')
            paginator_object = Paginator(video_objects, 12)
            page_num = min(int(data.get('page',1)),paginator_object.num_pages)
            response["next_page"] = True
            if(page_num == paginator_object.num_pages):
                response["next_page"] = False
                
            response["videos"] = video_objects_to_response(paginator_object.page(page_num))
            status = HTTP_200_OK

        except Exception as e:
            print("ERROR IN GetAllVideos", str(e))

        return Response(data=response,status=status)

GetAllVideos = GetAllVideosAPI.as_view()



class SearchAPI(APIView):

    """
        
    This API returns searched results from all the stored videos.

    Request Parameters: **page**

    Request Example:

        {
            "page": 1,
            "query": "news modi"
        }

    Note: **page** is an positive integer. If **query** is empty, the result will consists of all videos
    
    
    Response: **videos** and **next_page**

    Response Example:

        {
            "next_page": false,
            "videos": [
                {
                    "published_at": "2021-05-03 10:15:53",
                    "title": "Today Breaking News ! आज 2 मई 2021 के मुख्य समाचार बड़ी खबरें लॉकडाउन भारत बंद PM Modi news",
                    "description": "",
                    "channel_title": "PMC News",
                    "thumbnail_url": "https://i.ytimg.com/vi/hNERIAh8hiQ/default.jpg"
                },
                ...
                ...
                ...
            ],
            "next_page" : true
        }

    Note: **videos** list will be of length less than equal to 50. 
    **next_page** will be false when there are would be no more pages left.

    Note:

    1. Order of words does not matter
    2. Special Characters won't affect the result
    3. Cases won't matter
    4. Incomplete but correct substrings will still work (Instead of **election**, you could miswrite as **ection**) 

    """

    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        status = HTTP_500_INTERNAL_SERVER_ERROR

        try:
            data = request.data
            query = data.get("query","")
            query = query.split()
            new_query = []
            for word in query:
                # Splitting by special characters and extending query list 
                new_query.extend(re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', word))
            video_objects = Video.objects.all()
            for word in new_query:
                # For each query word, search if it is present in title or description of any videos
                video_objects = video_objects.filter(Q(title__icontains = word) | Q(description__icontains = word))
            video_objects = video_objects.order_by('-published_at')
            paginator_object = Paginator(video_objects, 12)
            page_num = min(int(data.get('page',1)),paginator_object.num_pages)
            response["next_page"] = True
            if(page_num == paginator_object.num_pages):
                response["next_page"] = False
            response["videos"] = video_objects_to_response(paginator_object.page(page_num))
            status = HTTP_200_OK

        except Exception as e:
            print("ERROR IN SearchAPI", str(e))

        return Response(data=response,status=status)

Search = SearchAPI.as_view()