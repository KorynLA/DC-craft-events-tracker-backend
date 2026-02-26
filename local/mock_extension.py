from flask import Flask, request, jsonify
import os
import boto3

app = Flask(__name__)

# Get endpoint from environment variable (set by docker-compose)
# Use service name "localstack" instead of "localhost" when in Docker
localstack_endpoint = os.environ.get('LOCALSTACK_ENDPOINT', 'http://localhost:4566')

print(f"[Mock Extension] Starting...")
print(f"[Mock Extension] LocalStack endpoint: {localstack_endpoint}")

ssm_client = boto3.client(
    'ssm',
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    endpoint_url=localstack_endpoint 
)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Test LocalStack connection
        ssm_client.describe_parameters(MaxResults=1)
        localstack_status = 'connected'
    except Exception as e:
        localstack_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'service': 'mock-lambda-extension',
        'localstack_endpoint': localstack_endpoint,
        'localstack_status': localstack_status
    })

@app.route('/systemsmanager/parameters/get', methods=['GET'])
def get_parameter():
    """Mock the Lambda extension endpoint"""
    name = request.args.get('name')
    with_decryption = request.args.get('withDecryption', 'false').lower() == 'true'
    
    print(f"[Mock Extension] Request for parameter: '{name}' (withDecryption={with_decryption})")
    
    if not name:
        return jsonify({'error': 'Parameter name is required'}), 400
    
    try:
        response = ssm_client.get_parameter(
            Name=name,
            WithDecryption=with_decryption
        )
        
        param_data = {
            'Parameter': {
                'Name': response['Parameter']['Name'],
                'Type': response['Parameter']['Type'],
                'Value': response['Parameter']['Value'],
                'Version': response['Parameter'].get('Version', 1),
                'ARN': response['Parameter'].get('ARN', f'arn:aws:ssm:us-east-1:000000000000:parameter{name}')
            }
        }
        
        print(f"[Mock Extension] Successfully retrieved: {response['Parameter']['Name']} = {response['Parameter']['Value']}")
        return jsonify(param_data)
        
    except ssm_client.exceptions.ParameterNotFound:
        print(f"[Mock Extension] Parameter not found: '{name}'")
        return jsonify({
            'error': f'Parameter not found: {name}'
        }), 404
        
    except Exception as e:
        print(f"[Mock Extension] Error: {str(e)}")
        return jsonify({
            'error': str(e),
            'localstack_endpoint': localstack_endpoint
        }), 500

if __name__ == '__main__':
    print(f"[Mock Extension] Starting on port 2773...")
    app.run(host='0.0.0.0', port=2773, debug=True)