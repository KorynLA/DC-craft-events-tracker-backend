import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import json
import os
import requests
from dotenv import load_dotenv
import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.client import Redis
from redis.exceptions import (
   BusyLoadingError,
   RedisError
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
CACHE_KEY='event_table:all'

if os.path.exists('.env'):
	load_dotenv()
	logger.info("Loaded environment from .env file")
else:
	logger.info("No .env file")

aws_session_token=os.environ['AWS_SESSION_TOKEN']
URL=os.environ['PARAMETERS_SECRETS_EXTENSION_URL']

REDIS_URL=os.environ['REDIS_URL']
REDIS_PORT=os.environ['REDIS_PORT']
REDIS_USERNAME=os.environ['REDIS_USERNAME']
REDIS_PASS_KEY=os.environ['REDIS_PASS_KEY']
def return_error(code, message):
	return {
		"statusCode": code,
		"message": message
	}

def connect_redis(password):
	logger.info("Connecting to Redis")
	logger.info(REDIS_URL)
	retry=Retry(ExponentialBackoff(), 3)
	try:
		r=redis.Redis(host=REDIS_URL, port=REDIS_PORT, password=password, username=REDIS_USERNAME, ssl=False, decode_responses=True, retry=retry, retry_on_error=[BusyLoadingError, RedisError])
	except Exception as e:
		logger.error("Failed to connect to redis: {}".format(e))
		return return_error(500, 'Error connecting to Redis')

	logger.info(r.ping())
	return r

def get_cached_data(r):
	try:
		logger.info(r.ping())
		data=r.get(CACHE_KEY)
		return data
	except Exception as e:
		logger.error("Failed to get from to redis: {}".format(e))
		return return_error(500, 'Error getting from Redis')

def get_aws_pass(password):
	try:
		url_config=URL+"/systemsmanager/parameters/get"
		logger.info("Parameter getter has started with url {}".format(url_config))
		res = requests.get(
    		url_config,
    		headers={"X-Aws-Parameters-Secrets-Token": aws_session_token},
    		params={"name": password, "withDecryption": "true"}
    		)
		found_password=res.json()['Parameter']['Value']
	except Exception as e:
		logger.error({e})
		return return_error(500, 'Server parameter retrieval error')
	return found_password

def lambda_handler(event, context):
	logger.info('Starting lambda handler')
	red_password=get_aws_pass(REDIS_PASS_KEY)
	
	r=connect_redis(red_password)
	cached_records=get_cached_data(r)
	if cached_records:
		return {
			"statusCode": 200,
        	"body": json.dumps({
            	"message": "Successful",
            	"found_events": json.loads(cached_records)
        	}, default=str) 
		}
	else:
		return return_error(500, 'No cached data found')
