import json

def handler(request):
    print(f"Request method: {request.method}")
    print(f"Request path: {request.path}")
    print(f"Request headers: {dict(request.headers)}")
    
    if request.method == 'POST':
        try:
            body = request.body
            print(f"Request body: {body}")
            data = json.loads(body) if body else {}
            print(f"Parsed data: {data}")
        except Exception as e:
            print(f"Error parsing body: {e}")
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Test endpoint working',
            'method': request.method,
            'path': request.path
        })
    }
