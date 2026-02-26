import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import json
import os
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
SELECT_ALL="Select name, time, price, description, link, craft,kids, date, business, location_name, address, city, state, zip from event LEFT JOIN location on event.location_id=location.id;"

if os.path.exists('.env'):
	load_dotenv()
	logger.info("Loaded environment from .env file")
else:
	logger.info("No .env file")

aws_session_token=os.environ['AWS_SESSION_TOKEN']
URL=os.environ['PARAMETERS_SECRETS_EXTENSION_URL']

DB_NAME=os.environ['DB_NAME']
USER=os.environ['USER']
PORT=os.environ['PORT']
HOST=os.environ['HOST']
DB_PASS_KEY=os.environ['DB_PASS_KEY']

def return_error(code, message):
	return {
		"statusCode": code,
		"message": message
	}

def connect_db(pg_connection):
	logger.info("Connecting to database")
	try:
		conn=psycopg2.connect(**pg_connection)
	except Exception as e:
		logger.error("Failed to connect to database with code: {} and error: {}".format(e.pgcode, e.pgerror))
		return return_error(500, 'Error connecting to database')
	return conn

def get_aws_pass(password):
	try:
		url_config=URL+"/systemsmanager/parameters/get"
		logger.info("Parameter getter has started with url {}".format(url_config))
		res = requests.get(
    		url_config,
    		headers={"X-Aws-Parameters-Secrets-Token": aws_session_token},
    		params={"name": password, "withDecryption": "true"}
    		)
		found_pass=res.json()['Parameter']['Value']
	except Exception as e:
		logger.error({e})
		return return_error(500, 'Server parameter retrieval error')
	return found_pass

def lambda_handler(event, context):
	logger.info('Starting lambda handler')
	db_password=get_aws_pass(DB_PASS_KEY)

	pg_connection = {
		'dbname': DB_NAME,
		'user': USER,
		'password': db_password,
		'port': PORT,
		'host': HOST
	}

	conn = connect_db(pg_connection)
	result=[]
	try:
		with conn.cursor(cursor_factory=RealDictCursor) as cur:
			cur.execute(SELECT_ALL)
			records = cur.fetchall()
			cur.close()
		conn.close()
	except psycopg2.Error as e:
		logger.error("Failed database call with code: {} and error: {}".format(e.pgcode, e.pgerror))
		return return_error(500, 'Retrieval from database failed')
	return {
		"statusCode": 200,
	       "body": json.dumps({
	           "message": "Successful",
	           "found_events": records
	       }, default=str) 
	}
