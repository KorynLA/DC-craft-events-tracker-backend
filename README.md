# About the Project
Project that gets events from a postgres database or redis, and inserts events into a database using lambdas. 
# Technologies
- [Docker](https://www.docker.com/): Either Docker Desktop or Docker Engine can be used. This setup will use Docker Desktop.
  - [Docker Desktop](https://docs.docker.com/desktop/)
  - [Docker Engine](https://docs.docker.com/engine/)
- [SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html)
- [Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Redis](https://redis.io/docs/latest/get-started/)
- [Python3](https://www.python.org/)
- [Pytest](https://docs.pytest.org/en/stable/)
- [LocalStack](https://docs.localstack.cloud/aws/services/lambda/)

# Running the Lambdas Locally
## Build the Lambda
1. Go to the root directory
2. chmod +x build_lambdas.sh
3. run ./build_lambdas.sh
   - Zips all of the lambda functions so they can be ran using localstack

## Run the Lambda
1. Open Docker Desktop
   - Starts Docker Engine
2. Go to the root directory
3. cp .env.local .env
   - Update .env.local with your values and copy over to .env which will be used both in Docker and the lambda functions.
5. docker compose up
   - If the images were built, and no changes were made to the docker files use this command to start the service.
   - Add --build at the end of the command if the images weren't previously built.
6. aws --endpoint-url=http://localhost:4566 ssm put-parameter --name {ssm_name) --value {local_db_password_value} --type SecureString
   - Adds the password that will be used for the Postgres database or Redis database you are testing. SSM is used in the Lambda to prevent hardcoding the password. If you are using both Redis and Postgres, you will need to run this twice. Once for Postgres and once for Redis.
     - Update {ssm_name} with the name of the key in the .env file under DB_PASS_KEY or REDIS_PASS_KEY variable.
     - Update {password_value} with the same password that is encoded in the docker-compose.yml under POSTGRES_DB or use the same password for Redis after adding the requirement in docker-compose.yml.
7. [Build the Lambda](#build-the-lambda)
8.  aws --endpoint-url=http://localhost:4566 lambda create-function   --runtime python3.11   --handler {program_name}.{program_lambda_handler_name}   --role arn:aws:iam::000000000000:role/lambdarole   --zip-file fileb://{zip_name}  --function-name {function_name}
    - The function name {function_name} will be used in the next command. This is the function that will be invoked. An example name that could be used is "test."
8.  aws --endpoint-url=http://localhost:4566 lambda invoke --cli-binary-format raw-in-base64-out --function-name {function_name} response.json
    - Once the function has been called the result will be put in response.json

# Testing
## Unit Tests
1. cd DC-craft-events-tracker-backend
   - Go to the root directory of the project
2. pip install pytest
   - Install pytest to run the unit tests
3. pytest
   - Runs the unit tests
