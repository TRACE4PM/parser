# Parser

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

### Custom log format

1. Gallica log format:

```log
##320022e99796ca35dab7e63d48fd5e7##France##Angers - - [22/12/1970:00:33:55 +0200] "GET /nom.html HTTP/1.0" 200 100 "-" "-"
```

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name

Choose a self-explaining name for your project.

## Description

Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges

On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals

Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation

Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage

Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support

Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap

If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing

State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment

Show your appreciation to those who have contributed to the project.

## License

For open source projects, say how it is licensed.

## Project status

If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
