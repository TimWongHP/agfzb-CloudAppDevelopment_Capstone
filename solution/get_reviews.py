from cloudant.client import Cloudant
from cloudant.error import CloudantException



def main(dict):
    client = Cloudant.iam(
        account_name=dict["COUCH_USERNAME"],
        api_key=dict["IAM_API_KEY"],
        url=dict["COUCH_URL"],
        connect=True,
    )

    my_database = client["reviews"]
    print(my_database)
    try:
        selector = {'dealership': {'$eq': int(dict["dealerId"])}}
        result_by_filter = my_database.get_query_result(
            selector, raw_result=True)

        result = {
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': result_by_filter}

        }
        return result
    except:
        return {
            'statusCode': 404,
            'message': "Something went wrong"
        }

def main(dict):
    try:
        if dict["statusCode"] == 404:
            return {
                "message": "Something went wrong",
                "statusCode": 404
            }
    except Exception:
        res = []
        for doc in dict['body']['data']['docs']:
            res.append({ 
            "id": doc['id'],
            "dealership": doc['dealership'],
            "review": doc['review'],
            "purchase": doc['purchase'],
            "purchase_date": doc['purchase_date'],
            "car_make": doc['car_make'],
            "car_model": doc['car_model'],
            "car_year": doc['car_year'],
            })
        return {"listOfReviews": res}
