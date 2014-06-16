# python imports
import os
import json
import urllib2
import urlparse

# Setup third party libraries
import sys
sys.path.insert(0, 'third-party')

# import third party libraries
from bs4 import BeautifulSoup

# import frameworks
import webapp2
import jinja2


# Setup jinja environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())


class APIHandler(webapp2.RequestHandler):
    def get(self):

        self.response.headers['Content-Type'] = 'text/json'

        link = self.request.get("link")

        url_components = urlparse.urlparse(link)

        # If no scheme associated with URL, assume http
        if url_components.scheme == '':
            link = "http://" + link

        request = urllib2.Request(link)

        err = False
        err_msg = ""

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            err = True
            err_msg += "HTTP Error: " + str(e.code)
        except urllib2.URLError, e:
            err = True
            err_msg += "URL Error: " + str(e.reason)
        except Exception:
            import traceback
            err = True
            err_msg += "Ran into an exception: Traceback - " + traceback.format_exc()

        if err:
            result = {
                'success': False,
                'message': err_msg
            }

        else:
            html = response.read()

            soup = BeautifulSoup(html.decode('utf-8'))

            # Get the description of the web page
            description = []

            description_tag = soup.findAll(attrs={"name": "description"})

            if len(description_tag) > 0:
                for i in range(len(description_tag)):
                    description.append(description_tag[i].get('content'))

            # Get the keywords of the web page
            keywords = []

            keywords_tag = soup.findAll(attrs={"name": "keywords"})

            if len(keywords_tag) > 0:
                for i in range(len(keywords_tag)):
                    keywords.append(keywords_tag[i].get('content'))

            # Get the title of the web page
            title = []

            if soup.title:
                title.append(soup.title.string)

            # Get the thumbnail image URL
            thumbnail_urls = []

            # Search for any open graph image
            og_image_tag = soup.findAll(attrs={"property": "og:image"})

            if len(og_image_tag) > 0:
                for i in range(len(og_image_tag)):
                    thumbnail_urls.append(og_image_tag[i].get("content"))

            og_image_tag = soup.findAll(attrs={"name": "og:image"})

            if len(og_image_tag) > 0:
                for i in range(len(og_image_tag)):
                    thumbnail_urls.append(og_image_tag[i].get("content"))

            # Search for link rel=img_src or image_src
            link_image_tag = soup.findAll(attrs={"rel": "img_src"})

            if len(link_image_tag) > 0:
                for i in range(len(link_image_tag)):
                    thumbnail_urls.append(link_image_tag[i].get("href"))

            link_image_tag = soup.findAll(attrs={"rel": "image_src"})

            if len(link_image_tag) > 0:
                for i in range(len(link_image_tag)):
                    thumbnail_urls.append(link_image_tag[i].get("href"))

            # Search for itemprop=image
            itemprop_image_tag = soup.findAll(attrs={"itemprop": "image"})

            if len(itemprop_image_tag) > 0:
                for i in range(len(itemprop_image_tag)):
                    thumbnail_urls.append(itemprop_image_tag[i].get("content"))

            result = {
                'success': True,
                'title': title,
                'description': description,
                'keywords': keywords,
                'thumbnails': thumbnail_urls
            }

        self.response.write(json.dumps(result))


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/api', APIHandler)
], debug=True)
