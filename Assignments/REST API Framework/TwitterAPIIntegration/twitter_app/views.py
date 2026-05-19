import os
import requests
from django.shortcuts import render

def get_twitter_headers():
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
    return {"Authorization": f"Bearer {bearer_token}"}

def index(request):
    tweets = []
    error_message = None
    username = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        if username:
            # Strip @ if user provided it
            if username.startswith("@"):
                username = username[1:]
                
            headers = get_twitter_headers()
            
            # Step 1: Get User ID from Username
            user_url = f"https://api.twitter.com/2/users/by/username/{username}"
            user_response = requests.get(user_url, headers=headers)
            
            if user_response.status_code == 200:
                user_data = user_response.json()
                if "data" in user_data:
                    user_id = user_data["data"]["id"]
                    
                    # Step 2: Get User Tweets
                    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
                    params = {
                        "max_results": 5,
                        "tweet.fields": "created_at,public_metrics",
                        "user.fields": "profile_image_url,username,name",
                        "expansions": "author_id"
                    }
                    tweets_response = requests.get(tweets_url, headers=headers, params=params)
                    
                    if tweets_response.status_code == 200:
                        tweets_data = tweets_response.json()
                        if "data" in tweets_data:
                            raw_tweets = tweets_data["data"]
                            includes = tweets_data.get("includes", {}).get("users", [])
                            
                            user_info = None
                            for u in includes:
                                if u["id"] == user_id:
                                    user_info = u
                                    break
                                    
                            for t in raw_tweets:
                                tweets.append({
                                    "text": t.get("text"),
                                    "created_at": t.get("created_at"),
                                    "metrics": t.get("public_metrics", {}),
                                    "user": user_info
                                })
                        else:
                            error_message = "No tweets found for this user."
                    else:
                        error_message = f"Error fetching tweets: {tweets_response.status_code} - {tweets_response.text}"
                else:
                    error_message = f"User '{username}' not found."
            else:
                error_message = f"Error fetching user: {user_response.status_code} - {user_response.text}"
        else:
            error_message = "Please enter a valid Twitter username."

    return render(request, "twitter_app/index.html", {
        "tweets": tweets,
        "error_message": error_message,
        "username": username
    })
