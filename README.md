# mini_messenger
This is a simple text message application. currently it only can send text 
in real time and save all the messages among users inside the database

## Installation

* Clone this repository
 > https://github.com/mini-M-py/mini_messenger.git

## Install required packages
 `pip install -r requirements.txt`
 * [postgres](https://www.postgresql.org/download/)

## Set up
 * Create a database inside the postgresql
 * Create `.env` file of root directory of porject folder and name environment
    ans following: 
      * database_hostname
      * database_port
      * database_name
      * database_username
      * database_password
      * secret_key
      * algorithm
      * access_token_expire_minutes
      * email
      * password `Don't use your email's password insted use App password 
      provided by your email service provider`

* Start the server `uvicorn main:app --reload`
* Navigate to `http://localhost:8000/docs` in your web browser to access the 
Swagger UI. From here, you can test the API endpoint using the built-in interface.

To run it in https server you have to change the all the http request to https in
`js` files.

## License
 This project is licensed under the MIT License - see the [LICENSE.md](/LICENSE.md) file for details.

## Contributing
pull requests are welcome.For major changes, please open an issue to discuss what you would like change.

