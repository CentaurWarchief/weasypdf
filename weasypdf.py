import tornado.ioloop
import tornado.web
import json
import urllib2

class WeasyPDF(tornado.web.RequestHandler):
    def post(self):
        try:
            payload = json.loads(self.request.body)
        except ValueError, e:
            self.set_status(400)
            self.finish()
            return

        headers = {
            "Accept": "text/html"
        }

        if not "url" in payload or payload['url'] == "":
            self.set_status(400)
            self.finish()
            return

        # relay both `Authorization` and `User-Agent` headers
        authorization = self.request.headers.get('Authorization')
        ua = self.request.headers.get('User-Agent')

        if authorization != None:
            headers['Authorization'] = authorization

        if ua != None:
            headers['User-Agent'] = ua

        req = urllib2.Request(payload['url'], headers=headers)
        res = urllib2.urlopen(req).read()

        # (...)

    def write_error(self, status_code, **kwargs):
        self.clear()
        self.set_status(status_code)

        if status_code == 405:
            self.add_header("Allow", "POST")

        self.finish()

def main():
    weasypdf = tornado.web.Application([
        (r"/", WeasyPDF),
    ])

    weasypdf.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()