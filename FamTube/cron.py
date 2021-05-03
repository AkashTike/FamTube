from apiclient.discovery import build
from FamTube.constants import *
import json
import datetime
from FamTube.models import *

def FetchVideosAndStore():

	print("INSIDE")

	from apiclient.discovery import build
	from FamTube.constants import API_KEYS, QUERY, INTERVAL_MINUTES
	import json
	import datetime
	from FamTube.models import Video

	try:
		is_api_key_valid = False

		for API_KEY in API_KEYS:

			youtube = build('youtube','v3',developerKey=API_KEY)

			# Fetch all videos published in this interval 
			new_interval_start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=INTERVAL_MINUTES)
			new_interval_start_time_string = str(new_interval_start_time.strftime("%Y-%m-%dT%H:%M:%SZ"))

			request = youtube.search().list(q=QUERY,part="snippet",type="video",order="date",publishedAfter=new_interval_start_time_string,maxResults=50)

			try:
				data = request.execute()

				for video in data["items"]:

					published_at = str(video["snippet"]["publishedAt"])
					published_at = datetime.datetime.strptime(published_at,'%Y-%m-%dT%H:%M:%SZ')
					title = str(video["snippet"]["title"])
					description = str(video["snippet"]["description"])
					channel_title = str(video["snippet"]["channelTitle"])
					thumbnail_url = str(video["snippet"]["thumbnails"]["default"]["url"])

					Video.objects.create(
						published_at=published_at,
						title=title,
						description=description,
						channel_title=channel_title,
						thumbnail_url=thumbnail_url)

				# Project whose API_KEY has not exceeded the quota
				is_api_key_valid = True
				break

			except Exception as error:

				print("ERROR: ", str(error))
				http_error = error.__dict__
				reason = str(http_error["error_details"][0]["reason"])
				print("ERROR: ", reason)

		if(is_api_key_valid == False):
			print("ERROR: Could Not Fetch Videos")

	except Exception as e:
		print("Some Error Occurred: " + str(e))