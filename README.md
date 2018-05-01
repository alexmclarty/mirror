# Mirror

A simple app that allows you to create mock endpoints on the fly which can be useful for testing APIs.

Also includes some endpoints useful for testing Open ID Connect integrations.

# How to run

Build the docker image with:

`docker build -t mirror .`

and run a container with:

`docker run -p 6001:6001 mirror`

The app will be available at `localhost:6001`.

To run locally setup a virtual environment, activate and install dependencies with `pip install -r requirements.txt`. 
`app.py` is the entrypoint.

Setting the environment variable `DEBUG` to run the app in debug mode and see a stacktrace.


## Running tests

Run:

`docker run mirror python tests.py`

Test output will be on the command line.

# How to use

* Send a POST request to `/register` with a description of the endpoint you want in this format:

```json
{
  "endpoint": "/cheese",
  "methods": ["GET"],
  "status_code": 200,
  "json_response": "{"type": "cheese"}"
}
``` 

* List all endpoints by sending a request to `/list`
* Shutdown the app by sending a request to `/shutdown` 

Fake Open ID routes here:

* `/get_code`
* `/connect/token`
* `/get_key`

See https://connect2id.com/learn/openid-connect for more information.

Enjoy programmatic mock API creation!

# TODO

* Better responses
    * Set HTML/JSON response
    * Set Headers
* Timeouts
* Delete endpoints
* Send broken responses/ignore problems with JSON formatting
* Different size responses