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

# Running the Lambdas Locally
## Build the Lambda
### Get Lambda
### Cache Lambda
### Create Lambda
## Run the Lambda
1. Open Docker Desktop
   - Starts Docker Engine
2. docker compose up
   - If the images were built, and no changes were made to the docker files use this command to start the service.
   - Add --build at the end of the command if the images weren't previously built.
4. aws --endpoint-url=http://localhost:4566 ssm put-parameter --name {ssm_name) --value {password_value} --type SecureString
   - Adds the password that will be used for the Postgres database you are testing. SSM is used in the Lambda to prevent hardcoding the password.
     - Update {ssm_name} with the name of the key in the .env file under DB_PASS_KEY variable.
     - Update {password_value} with the same password that is encoded in the docker-compose.yml under POSTGRES_DB.

# Testing
## Unit Tests
1. cd DC-craft-events-tracker-backend
   - Go to the root directory of the project
2. pip install pytest
   - Install pytest to run the unit tests
3. pytest
   - Runs the unit tests
