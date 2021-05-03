# Converts Objects to list of dictionaries
def video_objects_to_response(video_objects):

	video_list = []

	try:
		for video_object in video_objects:
		    
		    temp = {} 
		    temp["published_at"] = str(video_object.published_at)
		    temp["title"] = str(video_object.title)
		    temp["description"] = str(video_object.description)
		    temp["channel_title"] = str(video_object.channel_title)             
		    temp["thumbnail_url"] = str(video_object.thumbnail_url)
		    
		    video_list.append(temp)
	except:
		pass

	return video_list