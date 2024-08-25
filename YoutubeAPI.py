from googleapiclient.discovery import build
from bertopic import BERTopic
 
api_key = 'AIzaSyClqafjpykaR3OqmMDgghLF9YcifZ9A6QE'
 
def video_comments(video_id):
    # dictionary for storing replies
    replies = {}
    
    comments = []

    list = []
 
    # creating youtube resource object
    youtube = build('youtube', 'v3',
                    developerKey=api_key)
 
    # retrieve youtube video results
    video_response=youtube.commentThreads().list(
    part='snippet,replies',
    videoId=video_id
    ).execute()
    # iterate video response
    while video_response:
       
        # extracting required info
        # from each result object 
        for item in video_response['items']:    

            replyList = []
           
            # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
             
            # counting number of reply of comment
            replycount = item['snippet']['totalReplyCount']

            listItem = comment
            # if reply is there
            if replycount>0:
               
                # iterate through all reply
                for reply in item['replies']['comments']:
                   
                    # Extract reply
                    reply = reply['snippet']['textDisplay']
                    comment += reply
                    # Store reply is list
                    replyList.append(reply)
            replies[comment] = replyList
            comments.append(comment)
            list.append(listItem)
            # print comment with list of reply
            print(comment, replyList, end = '\n\n')
 
        # Again repeat
        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = video_id,
                      pageToken = video_response['nextPageToken']
                ).execute()
        else:
            break
        
    docs = list
    topic_model = BERTopic()
    topics, probs = topic_model.fit_transform(docs)
    info_df = topic_model.get_topic_info()
    print(info_df.to_markdown())
    fig = topic_model.visualize_topics()
    fig.write_html("./Visual.html")
    fig2 = topic_model.visualize_hierarchy()
    fig2.write_html("./Hierarchy.html")
 
# Enter video id
video_id = "hCW2NHbWNwA"#"KSbxwbLkhCQ"
 
# Call function
video_comments(video_id)
