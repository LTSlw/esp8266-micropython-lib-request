# esp8266-micropython-lib-request
esp8266 http/https request lib for micropython

## Usage

``` python
import request
```

### Request: class

#### variables

##### Request.method

str, HTTP method: 'GET', 'POST'...

##### headers

dict, Request headers

##### data

data, HTTP data, request() send data when data is not `b''`, even if http method is `GET`

##### proto

str, protocol, suffix`:` shoould be added, e.g., `http:`

##### host

str, host

##### path

str, path

##### port

int, port

##### enable_ssl

bool, decide whether to use SSL

#### functions

##### \_\_init\_\_\(\)

``` python
def __init__(
    self,
    method: str = 'GET',  # HTTP Mothod: GET, POST...
    url: str = '',        # URL, e.g., https://github.com
    params: dict = None,  #  a dict of params
    headers: dict = None, # a dict of http request headers
    data: bytes = None    # data
)
```

header: `Host`, `Content-Length` will be automaticly calculated

##### request(): Response

Do request and return response

## Change log

 - v0.1.1

basic http/https message sending and receiving completed