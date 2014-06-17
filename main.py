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


def get_link_details(link, number_of_results=None):

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

            # Description from meta tag
            description = []

            description_tag = soup.find_all(attrs={"name": "description"})

            for i in range(len(description_tag)):
                description.append(description_tag[i].get('content'))

            # Description from open graph tag
            og_description_tag = soup.find_all(attrs={"name": "og:description"})

            for i in range(len(og_description_tag)):
                description.append(og_description_tag[i].get('content'))

            og_description_tag = soup.find_all(attrs={"property": "og:description"})

            for i in range(len(og_description_tag)):
                description.append(og_description_tag[i].get('content'))

            # Get the keywords of the web page
            keywords = []

            keywords_tag = soup.find_all(attrs={"name": "keywords"})

            for i in range(len(keywords_tag)):
                keywords.append(keywords_tag[i].get('content'))

            # Get the title of the web page

            # Get the normal title tag text
            title = []

            if soup.title:
                title.append(soup.title.string)

            # Get the open graph title
            title_tag = soup.find_all(attrs={"name": "og:title"})

            for i in range(len(title_tag)):
                title.append(title_tag[i].get('content'))

            title_tag = soup.find_all(attrs={"property": "og:title"})

            for i in range(len(title_tag)):
                title.append(title_tag[i].get('content'))

            # Get the thumbnail image URL
            thumbnail_urls = []

            # Search for any open graph image
            og_image_tag = soup.find_all(attrs={"property": "og:image"})

            for i in range(len(og_image_tag)):
                thumbnail_urls.append(og_image_tag[i].get("content"))

            og_image_tag = soup.find_all(attrs={"name": "og:image"})

            for i in range(len(og_image_tag)):
                thumbnail_urls.append(og_image_tag[i].get("content"))

            # Search for link rel=img_src or image_src
            link_image_tag = soup.find_all(attrs={"rel": "img_src"})

            for i in range(len(link_image_tag)):
                thumbnail_urls.append(link_image_tag[i].get("href"))

            link_image_tag = soup.find_all(attrs={"rel": "image_src"})

            for i in range(len(link_image_tag)):
                thumbnail_urls.append(link_image_tag[i].get("href"))

            # Search for itemprop=image
            itemprop_image_tag = soup.find_all(attrs={"itemprop": "image"})

            for i in range(len(itemprop_image_tag)):
                thumbnail_urls.append(itemprop_image_tag[i].get("content"))

            # Get the author of webpage
            author = []

            author_tag = soup.find_all(attrs={"name": "author"})

            for i in range(len(author_tag)):
                author.append(author_tag[i].get("content"))

            if number_of_results == 'multiple':
                result = {
                    'success': True,
                    'title': title,
                    'description': description,
                    'keywords': keywords,
                    'thumbnails': thumbnail_urls,
                    'link': link,
                    'author': author
                }
            else:
                title_result = ''
                description_result = ''
                keywords_result = ''
                thumbnails_result = ''
                author_result = ''

                if len(title) > 0:
                    title_result = title[0]

                if len(description) > 0:
                    description_result = description[0]

                if len(keywords) > 0:
                    keywords_result = keywords[0]

                if len(thumbnail_urls) > 0:
                    thumbnails_result = thumbnail_urls[0]

                if len(author) > 0:
                    author_result = author[0]

                result = {
                    'success': True,
                    'title': title_result,
                    'description': description_result,
                    'keywords': keywords_result,
                    'thumbnail': thumbnails_result,
                    'link': link,
                    'author': author_result
                }

        return result


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())


class APIHandler(webapp2.RequestHandler):
    def get(self):

        self.response.headers['Content-Type'] = 'text/json'

        link = self.request.get("link")
        number_of_results = self.request.get("results")

        result = get_link_details(link, number_of_results)

        self.response.write(json.dumps(result))


class IframeSrcHandler(webapp2.RequestHandler):
    def get(self):

        link = self.request.get("link")

        result = get_link_details(link)

        if result['success']:
            template = JINJA_ENVIRONMENT.get_template('iframe-src.html')
            self.response.write(template.render(result))
        else:
            template = JINJA_ENVIRONMENT.get_template('iframe-error.html')
            self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/api', APIHandler),
    ('/iframe-src', IframeSrcHandler)
], debug=True)
