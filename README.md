# Parser

This project is part of the [TRACE4PM stack](https://github.com/TRACE4PM)  and is intended to be used with the TRACE4PM API.
The parser can also be used locally, as demonstrated in the `dev.py` file for development purposes.


## Example of log format :

1. Apache Common Log Format (CLF):

```log
127.0.0.1 - - [22/Dec/1970:00:33:55 +0200] "GET /nom.html HTTP/1.0" 200 100
```

2. Apache Combined Log Format:

```log
127.0.0.1 - - [22/Dec/1970:00:33:55 +0200] "GET /nom.html HTTP/1.0" 200 100 "-" "-"
```

3. Nginx default log format:

```log
127.0.0.1 - - [22/Dec/1970:00:33:55 +0200] "GET /nom.html HTTP/1.0" 200 100 "-" "-"
```

4. AWS ELB access log format:

```log
1970-12-22T00:33:55.000Z my-loadbalancer 127.0.0.1:80 - -1 -1 -1 200 -1 100 0 0 "GET http://nom.html HTTP/1.0"
```

5. Microsoft IIS log format:

```log
1970-12-22 00:33:55 127.0.0.1 GET /nom.html - 80 - ::1 HTTP/1.0 - 200 0 100
```

6. JSON log format:

```json
{
  "timestamp": "1970-12-22T00:33:55+02:00",
  "remote_addr": "127.0.0.1",
  "user_agent": "-",
  "request_method": "GET",
  "request_uri": "/nom.html",
  "http_version": "HTTP/1.0",
  "response_status": 200,
  "body_bytes_sent": 100
}
```


