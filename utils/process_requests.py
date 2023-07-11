from requests import Session,Response

session = Session()
session.headers = {'user-agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def handle_response(response:Response) : 
    if response.status_code == 200 : 
        return response.text
    
def make_request(url,method="GET",params=None,data=None,proxies=None):
    if method == "POST" : 
        response =session.get(url=url,
                              data=data,
                              params=params)
    else : 
        response =session.get(url=url,
                              data=data,
                              params=params)
        
    return handle_response(response=response)

