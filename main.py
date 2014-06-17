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


def get_link_details(link, number_of_results=None, version=None):

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

            for tag in description_tag:
                description.append(tag.get('content'))

            # Description from open graph tag
            og_description_tag = soup.find_all(attrs={"name": "og:description"})

            for tag in og_description_tag:
                description.append(tag.get('content'))

            og_description_tag = soup.find_all(attrs={"property": "og:description"})

            for tag in og_description_tag:
                description.append(tag.get('content'))

            # Get the keywords of the web page
            keywords = []

            keywords_tag = soup.find_all(attrs={"name": "keywords"})

            for tag in keywords_tag:
                keywords.append(tag.get('content'))

            # Get the title of the web page

            # Get the normal title tag text
            title = []

            if soup.title:
                title.append(soup.title.string)

            # Get the open graph title
            title_tag = soup.find_all(attrs={"name": "og:title"})

            for tag in title_tag:
                title.append(tag.get('content'))

            title_tag = soup.find_all(attrs={"property": "og:title"})

            for tag in title_tag:
                title.append(tag.get('content'))

            # Get the thumbnail image URL
            thumbnail_urls = []

            # Search for any open graph image
            og_image_tag = soup.find_all(attrs={"property": "og:image"})

            for tag in og_image_tag:
                thumbnail_urls.append(tag.get("content"))

            og_image_tag = soup.find_all(attrs={"name": "og:image"})

            for tag in og_image_tag:
                thumbnail_urls.append(tag.get("content"))

            # Search for link rel=img_src or image_src
            link_image_tag = soup.find_all(attrs={"rel": "img_src"})

            for tag in link_image_tag:
                thumbnail_urls.append(tag.get("href"))

            link_image_tag = soup.find_all(attrs={"rel": "image_src"})

            for tag in link_image_tag:
                thumbnail_urls.append(tag.get("href"))

            # Search for itemprop=image
            itemprop_image_tag = soup.find_all(attrs={"itemprop": "image"})

            for tag in itemprop_image_tag:
                thumbnail_urls.append(tag.get("content"))

            # Get the author of webpage
            author = []

            author_tag = soup.find_all(attrs={"name": "author"})

            for tag in author_tag:
                author.append(tag.get("content"))

            # Get the subject of the web page
            subject = []

            subject_tag = soup.find_all(attrs={"name": "subject"})

            for tag in subject_tag:
                subject.append(tag.get("content"))

            # Get the copyright of the web page
            copyright = []

            copyright_tag = soup.find_all(attrs={"name": "copyright"})

            for tag in copyright_tag:
                copyright.append(tag.get("content"))

            # Get the language of the web page
            language = []

            language_tag = soup.find_all(attrs={"name": "language"})

            for tag in language_tag:
                language.append(tag.get("content"))

            # Get the revised time of the web page
            revised = []

            revised_tag = soup.find_all(attrs={"name": "revised"})

            for tag in revised_tag:
                revised.append(tag.get("content"))

            # Get the abstract of the web page
            abstract = []

            abstract_tag = soup.find_all(attrs={"name": "abstract"})

            for tag in abstract_tag:
                abstract.append(tag.get("content"))

            # Get the topic of the web page
            topic = []

            topic_tag = soup.find_all(attrs={"name": "topic"})

            for tag in topic_tag:
                topic.append(tag.get("content"))

            # Get the summary of the web page
            summary = []

            summary_tag = soup.find_all(attrs={"name": "summary"})

            for tag in summary_tag:
                summary.append(tag.get("content"))

            # Get the classification of the web page
            classification = []

            classification_tag = soup.find_all(attrs={"name": "classification"})

            for tag in classification_tag:
                classification.append(tag.get("content"))

            # Get the designer of the web page
            designer = []

            designer_tag = soup.find_all(attrs={"name": "designer"})

            for tag in designer_tag:
                designer.append(tag.get("content"))

            # Get the mail id of the web page
            mail = []

            mail_tag = soup.find_all(attrs={"name": "reply-to"})

            for tag in mail_tag:
                mail.append(tag.get("content"))

            # Get the owner of the web page
            owner = []

            owner_tag = soup.find_all(attrs={"name": "owner"})

            for tag in owner_tag:
                owner.append(tag.get("content"))

            # Get the url of the web page
            url = []

            url_tag = soup.find_all(attrs={"name": "url"})

            for tag in url_tag:
                url.append(tag.get("content"))

            # Get the identifier url of the web page
            identifier_url = []

            identifier_url_tag = soup.find_all(attrs={"name": "identifier-url"})

            for tag in identifier_url_tag:
                identifier_url.append(tag)

            # Get the directory of the web page
            directory = []

            directory_tag = soup.find_all(attrs={"name": "directory"})

            for tag in directory_tag:
                directory.append(tag.get("content"))

            # Get the page name
            pagename = []

            pagename_tag = soup.find_all(attrs={"name": "pagename"})

            for tag in pagename_tag:
                pagename.append(tag.get("content"))

            # Get the category of the web page
            category = []

            category_tag = soup.find_all(attrs={"name": "category"})

            for tag in category_tag:
                category.append(tag.get("content"))

            # Get the coverage of the web page
            coverage = []

            coverage_tag = soup.find_all(attrs={"name": "coverage"})

            for tag in coverage_tag:
                coverage.append(tag.get("content"))

            # Get the distribution of the web page
            distribution = []

            distribution_tag = soup.find_all(attrs={"name": "distribution"})

            for tag in distribution_tag:
                distribution.append(tag.get("content"))

            # Get the rating of the web page
            rating = []

            rating_tag = soup.find_all(attrs={"name": "rating"})

            for tag in rating_tag:
                rating.append(tag.get("content"))

            # Get the subtitle of the web page
            subtitle = []

            subtitle_tag = soup.find_all(attrs={"name": "subtitle"})

            for tag in subtitle_tag:
                subtitle.append(tag.get("content"))

            # Get the target of the web page
            target = []

            target_tag = soup.find_all(attrs={"name": "target"})

            for tag in target_tag:
                target.append(tag.get("content"))

            # Get the date of the web page
            date = []

            date_tag = soup.find_all(attrs={"name": "date"})

            for tag in date_tag:
                date.append(tag.get("content"))

            # Get the search date of the web page
            search_date = []

            search_date_tag = soup.find_all({"name": "search_date"})

            for tag in search_date_tag:
                search_date.append(tag.get("content"))

            # Get the medium of the web page
            medium = []

            medium_tag = soup.find_all({"name": "medium"})

            for tag in medium_tag:
                medium.append(tag.get("content"))

            # Get the syndication source of the web page
            syndication_source = []

            syndication_source_tag = soup.find_all({"name": "syndication-source"})

            for tag in syndication_source_tag:
                syndication_source.append(tag.get("content"))

            # Get the original source of the web page
            original_source = []

            original_source_tag = soup.find_all({"name": "original-source"})

            for tag in original_source_tag:
                original_source.append(tag.get("content"))

            if number_of_results == 'multiple':
                result = {
                    'success': True,
                    'title': title,
                    'description': description,
                    'thumbnails': thumbnail_urls,
                    'link': link,
                    'author': author
                }

                if version == 'long':
                    result['keywords'] = keywords

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
                    'thumbnail': thumbnails_result,
                    'link': link,
                    'author': author_result
                }

                if version == 'long':
                    result['keywords'] = keywords_result

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
        version = self.request.get("version")

        result = get_link_details(link, number_of_results, version)

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
