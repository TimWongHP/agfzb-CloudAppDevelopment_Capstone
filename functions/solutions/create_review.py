import sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException

def main(dict):
    client = Cloudant.iam(
        account_name=dict["COUCH_USERNAME"], 
        api_key=dict["IAM_API_KEY"],
        url=dict["COUCH_URL"],
        connect=True, 
    )
    
    db = client["reviews"]
    new_review = db.create_document(dict["review"])   
    
    if new_review.exists():
        result = {
            "headers": {"Content-Type": "application/json"},
            "body": {"message": "Review posted successfully."}
        }
    
        print(new_review)
        return result
        
    else: 
        error_json = {
            "statusCode": 500,
            "message": "Could not post review due to server error."
        }
        return error_json
