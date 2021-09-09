import requests
import json

followers_file = open("followers.txt", "w+", encoding="utf-8")
following_file = open("following.txt", "w+", encoding="utf-8")


brief_dict = {}

cookie = '' #Here Paste Your Twitter Cookie

authorization = '' #Here Paste your Authoriaztion Token

csrf_token = '' #Here Paste your CSRF Token


#Check Documentation to find out how to get his values.

#Extracts the Information from the API Repsonse  & Store it in followers.txt & following.txt
def infoExtractor(JSONpayload, index, typeRequest):
    if(typeRequest == "followers_timeline"):
        file = followers_file
    else:
        file = following_file
    if(JSONpayload["data"]["user"][typeRequest]["timeline"]["instructions"][index]['type'] == "TimelineAddEntries"):
        userInfo= JSONpayload["data"]["user"][typeRequest]["timeline"]["instructions"][index]['entries']
        for i in range(0,len(userInfo)-2):
            brief_dict["name"] = str(userInfo[i]["content"]["itemContent"]["user"]["legacy"]["name"])
            brief_dict["screen_name"] = str(userInfo[i]["content"]["itemContent"]["user"]["legacy"]["screen_name"])
            brief_dict["verified"] = str(userInfo[i]["content"]["itemContent"]["user"]["legacy"]["verified"])
            file.write(json.dumps(brief_dict) + "\n")
        return userInfo[len(userInfo)-2]['content']['value']
    elif(JSONpayload["data"]["user"][typeRequest]["timeline"]["instructions"][index]['type'] == "TimelineTerminateTimeline"):
        userInfo= JSONpayload["data"]["user"][typeRequest]["timeline"]["instructions"][index+1]['entries']
        for i in range(0,len(userInfo)-2):
            brief_dict["name"] = str(userInfo[i]["content"]["itemContent"]["user"]["legacy"]["name"])
            brief_dict["screen_name"] = str(userInfo[i]["content"]["itemContent"]["user"]["legacy"]["screen_name"])
            brief_dict["verified"] = str(userInfo[i]["content"]["itemContent"]["user"]["legacy"]["verified"])
            file.write(json.dumps(brief_dict) + "\n")
        return ""

#Sends the API request to the Twitter Servers
def runProgram(option,header_option, user_id,count):
    headers = {
        "authority": "twitter.com",
        "authorization": authorization,
        "x-twitter-client-language": "en",
        "x-csrf-token": csrf_token,
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-active-user": "yes",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45",
        "content-type": "application/json",
        "accept": "*/*",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://twitter.com/TheShreyder/"+option,
        "accept-language": "en-US,en;q=0.9",
        "cookie": cookie
    }

    if(option == "followers"):
        payload = requests.get(
            'https://twitter.com/i/api/graphql/86vlEx-ifXptbl2JmLfxHg/Followers?variables=%7B%22userId%22%3A%22'+user_id+'%22%2C%22count%22%3A'+count+'%2C%22withHighlightedLabel%22%3Afalse%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withTweetResult%22%3Afalse%2C%22withUserResults%22%3Afalse%2C%22withNonLegacyCard%22%3Atrue%7D',
             headers=headers, timeout=2300).text
    else:
        payload = requests.get(
            "https://twitter.com/i/api/graphql/taJbMVFxNBcULs8aHwX3cg/Following?variables=%7B%22userId%22%3A%22"+user_id+"%22%2C%22count%22%3A"+count+"%2C%22withHighlightedLabel%22%3Afalse%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withTweetResult%22%3Afalse%2C%22withUserResults%22%3Afalse%2C%22withNonLegacyCard%22%3Atrue%7D",
            headers=headers, timeout=2300).text


    firstCursor = infoExtractor(json.loads(payload), 2, header_option).split("|")

    while (True):
        if (option == "followers"):
            payload = requests.get(
                'https://twitter.com/i/api/graphql/86vlEx-ifXptbl2JmLfxHg/Followers?variables=%7B%22userId%22%3A%22'+user_id+'%22%2C%22count%22%3A'+count+'%2C%22cursor%22%3A%22' +
                firstCursor[0] + '%7C' + firstCursor[
                    1] + '%22%2C%22withHighlightedLabel%22%3Afalse%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withTweetResult%22%3Afalse%2C%22withUserResults%22%3Afalse%2C%22withNonLegacyCard%22%3Atrue%7D',
                headers=headers, timeout=2300).text
        else:
            payload = requests.get(
                'https://twitter.com/i/api/graphql/taJbMVFxNBcULs8aHwX3cg/Following?variables=%7B%22userId%22%3A%22'+user_id+'%22%2C%22count%22%3A'+count+'%2C%22cursor%22%3A%22' +
                firstCursor[0] + '%7C' + firstCursor[
                    1] + '%22%2C%22withHighlightedLabel%22%3Afalse%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withTweetResult%22%3Afalse%2C%22withUserResults%22%3Afalse%2C%22withNonLegacyCard%22%3Atrue%7D',
                headers=headers, timeout=2300).text

        firstCursor = infoExtractor(json.loads(payload), 0, header_option)
        if (firstCursor == ""):
            break
        else:
            firstCursor = firstCursor.split("|")

if __name__ == "__main__":
    if((cookie == '' or authorization=='' or csrf_token=='') and 1!=1):
        print("Pls Check the Cookie, Authorization & csrf token in the Code. Check the Documentation to know how ot get them")
    else:
        first_header = {
            "authority": "twitter.com",
            "authorization": authorization,
            "x-twitter-client-language": "en",
            "x-csrf-token": csrf_token,
            "x-guest-token": "1371160710940561409",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50",
            "content-type": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "cookie": cookie
        }
        screen_name = input("Enter the UserName:")

        payload = requests.get(
            "https://twitter.com/i/api/graphql/hc-pka9A7gyS3xODIafnrQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22" + screen_name + "%22%2C%22withHighlightedLabel%22%3Atrue%7D",
            headers=first_header).text

        try:
            user_payload = json.loads(payload)
            user_id = user_payload['data']['user']['rest_id']
            followers_count = user_payload['data']['user']['legacy']['followers_count']
            following_count = user_payload['data']['user']['legacy']['friends_count']

            if (followers_count > 12000):
                followers_count_limit = 12000 - 100
            else:
                followers_count_limit = followers_count - 4

            if (following_count > 12000):
                following_count_limit = 12000 - 100
            else:
                following_count_limit = following_count - 4

            followers_count_limit = 1000
            following_count_limit = 1000

            print("Followers", followers_count)
            runProgram("followers", "followers_timeline", user_id, str(followers_count - 1))
            print("Following", following_count)
            runProgram("following", "following_timeline", user_id, str(following_count - 1))
        except Exception as e :
            print("Error: "+str(e))
            print("Pls Check the Username or all token, if still error, then post in the repo.")