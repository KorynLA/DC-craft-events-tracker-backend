import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import json
import os
import requests
from dotenv import load_dotenv
import html
import re
from datetime import datetime
from validators import (
    validate_user_input,
    validate_required_user_input_exists
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

INSERT = """INSERT INTO user_submitted_event (name, price, description, link, kids, location_name, date, time, business, email, date_submitted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

if os.path.exists('.env'):
	load_dotenv()
	logger.info("Loaded environment from .env file")
else:
	logger.info("No .env file")

aws_session_token = os.environ['AWS_SESSION_TOKEN']
env = os.environ['ENV']
url=os.environ['PARAMETERS_SECRETS_EXTENSION_URL']

dbname = os.environ['DB_NAME']
user = os.environ['DB_USER']
port = os.environ['DB_PORT']
host = os.environ['DB_HOST']
DB_PASS_KEY=os.environ['DB_PASS_KEY']

def return_error(code, message):
	return {
		"statusCode": code,
		"message": message
	}

def connect_db(pg_connection):
	logger.info("Connecting to database")
	try:
		conn = psycopg2.connect(**pg_connection)
	except psycopg2.Error as e:
		logger.error("Failed database call with code: {} error: {}".format(e.pgcode, e.pgerror))
		return return_error(500, 'Error connecting to database')
	return conn

def sanitize_input(input_str):
	if not input_str:
		return None
	sanitized_str=''
	emoji_pattern = re.compile(
    	"["
    	"\U0001F600-\U0001F64F"
    	"\U0001F300-\U0001F5FF"
    	"\U0001F680-\U0001F6FF"
    	"\U0001F1E0-\U0001F1FF"
    	"]+",
    	flags=re.UNICODE
	)
	sanitized_str = re.sub(r'<script\b[^>]*>(.*?)</script>', '', input_str, flags=re.IGNORECASE)
	sanitized_str= emoji_pattern.sub('', sanitized_str)
	sanitized_str = html.escape(sanitized_str)
	return sanitized_str

def lambda_handler(event, context):
	logger.info('Starting lambda handler')
	password=''
	try:
		url_config=url+"/systemsmanager/parameters/get"
		logger.info("Parameter getter has started with url {}".format(url_config))
		res = requests.get(
    		url_config,
    		headers={"X-Aws-Parameters-Secrets-Token": aws_session_token},
    		params={"name": DB_PASS_KEY, "withDecryption": "true"}
    		)
		password = res.json()['Parameter']['Value']
	except Exception as e:
		logger.error({e})
		return return_error(500, 'Server parameter retrieval error')

	pg_connection = {
		'dbname': dbname,
		'user': user,
		'password': password,
		'port': port,
		'host': host
	}
	conn = connect_db(pg_connection)

	if not isinstance(event, (dict, list)):
		try:
			data = json.loads(event)
		except Exception as e:
			logger.error("Failed json conversion: {} and error: {}".format(e.stackTrace()))
			return return_error(500, 'Conversion error')
	else:
		data = event

	name = sanitize_input(data.get("name", None))
	descrip = sanitize_input(data.get("description", None))
	org = sanitize_input(data.get("organization", None))
	location = sanitize_input(data.get("location", None))

	if not validate_required_user_input_exists(data): 
		return return_error(422, 'Missing required input')
	if not validate_user_input(data, name, descrip, org, location):
		return return_error(422, 'Input entered is invalid')

	time = data.get("time", None)
	price = data.get("price", None)
	link = data.get("link", None)
	kids = data.get("kids", None)
	date = data.get("date", None)
	email = data.get('email', None)
	today = datetime.now().strftime('%Y-%m-%d')

	try:
		with conn.cursor(cursor_factory=RealDictCursor) as cur:
			cur.execute(INSERT, (name, price, descrip, link, kids, location, date, time, org, email, today))
			conn.commit()
			cur.close()
		conn.close()
	except psycopg2.Error as e:
		logger.error("Failed database call with code: {} error: {}".format(e.pgcode, e.pgerror))
		if e.pgcode == "23505":
			return return_error(422, 'The event was already submitted')
		return return_error(500, 'Insert into database failed')
	return {
		"statusCode": 200,
        "body": json.dumps({
            "message": "Successful",
        }, default=str) 
	}