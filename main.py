# python imports
import os
import json
import urllib2
import urlparse

# Setup third party libraries
import sys
sys.path.insert(0, 'third-party')

# import third party libraries
from bs4 import BeautifulSoup, SoupStrainer

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
            response = None
            err_msg += "HTTP Error: " + str(e.code)
        except urllib2.URLError, e:
            err = True
            response = None
            err_msg += "URL Error: " + str(e.reason)
        except Exception:
            import traceback
            err = True
            response = None
            err_msg += "Ran into an exception: Traceback - " + traceback.format_exc()

        if err:
            result = {
                'success': False,
                'message': err_msg
            }

        else:
            html = response.read()

            # The meta tags soup
            meta_strainer = SoupStrainer('meta')
            meta_soup = BeautifulSoup(html.decode('utf-8'), parse_only=meta_strainer)

            # The link tags soup
            link_strainer = SoupStrainer('link')
            link_soup = BeautifulSoup(html.decode('utf-8'), parse_only=link_strainer)

            # The title soup
            title_strainer = SoupStrainer('title')
            title_soup = BeautifulSoup(html.decode('utf-8'), parse_only=title_strainer)

            # Get the description of the web page

            # Description from meta tag
            description = []

            description_tag = meta_soup.find_all(attrs={"name": "description"})

            for tag in description_tag:
                description.append(tag.get('content'))

            # Description from open graph tag
            og_description_tag = meta_soup.find_all(attrs={"name": "og:description"})

            for tag in og_description_tag:
                description.append(tag.get('content'))

            og_description_tag = meta_soup.find_all(attrs={"property": "og:description"})

            for tag in og_description_tag:
                description.append(tag.get('content'))

            # Get the title of the web page

            # Get the normal title tag text
            title = []

            if title_soup.title:
                title.append(title_soup.title.string)

            # Get the open graph title
            title_tag = meta_soup.find_all(attrs={"name": "og:title"})

            for tag in title_tag:
                title.append(tag.get('content'))

            title_tag = meta_soup.find_all(attrs={"property": "og:title"})

            for tag in title_tag:
                title.append(tag.get('content'))

            # Get the thumbnail image URL
            thumbnail_urls = []

            # Search for any open graph image
            og_image_tag = meta_soup.find_all(attrs={"property": "og:image"})

            for tag in og_image_tag:
                thumbnail_urls.append(tag.get("content"))

            og_image_tag = meta_soup.find_all(attrs={"name": "og:image"})

            for tag in og_image_tag:
                thumbnail_urls.append(tag.get("content"))

            # Search for link rel=img_src or image_src
            link_image_tag = link_soup.find_all(attrs={"rel": "img_src"})

            for tag in link_image_tag:
                thumbnail_urls.append(tag.get("href"))

            link_image_tag = link_soup.find_all(attrs={"rel": "image_src"})

            for tag in link_image_tag:
                thumbnail_urls.append(tag.get("href"))

            # Search for itemprop=image
            itemprop_image_tag = meta_soup.find_all(attrs={"itemprop": "image"})

            for tag in itemprop_image_tag:
                thumbnail_urls.append(tag.get("content"))

            # Get the author of webpage
            author = []

            author_tag = meta_soup.find_all(attrs={"name": "author"})

            for tag in author_tag:
                author.append(tag.get("content"))

            keywords = []
            subject = []
            copyright = []
            language = []
            revised = []
            abstract = []
            topic = []
            summary = []
            classification = []
            designer = []
            mail = []
            owner = []
            url = []
            identifier_url = []
            directory = []
            pagename = []
            category = []
            coverage = []
            distribution = []
            rating = []
            subtitle = []
            target = []
            date = []
            search_date = []
            medium = []
            syndication_source = []
            original_source = []

            if version == 'long':

                # Get the keywords of the web page
                keywords_tag = meta_soup.find_all(attrs={"name": "keywords"})

                for tag in keywords_tag:
                    keywords.append(tag.get('content'))

                # Get the subject of the web page
                subject_tag = meta_soup.find_all(attrs={"name": "subject"})

                for tag in subject_tag:
                    subject.append(tag.get("content"))

                # Get the copyright of the web page
                copyright_tag = meta_soup.find_all(attrs={"name": "copyright"})

                for tag in copyright_tag:
                    copyright.append(tag.get("content"))

                # Get the language of the web page
                language_tag = meta_soup.find_all(attrs={"name": "language"})

                for tag in language_tag:
                    language.append(tag.get("content"))

                # Get the revised time of the web page
                revised_tag = meta_soup.find_all(attrs={"name": "revised"})

                for tag in revised_tag:
                    revised.append(tag.get("content"))

                # Get the abstract of the web page
                abstract_tag = meta_soup.find_all(attrs={"name": "abstract"})

                for tag in abstract_tag:
                    abstract.append(tag.get("content"))

                # Get the topic of the web page
                topic_tag = meta_soup.find_all(attrs={"name": "topic"})

                for tag in topic_tag:
                    topic.append(tag.get("content"))

                # Get the summary of the web page
                summary_tag = meta_soup.find_all(attrs={"name": "summary"})

                for tag in summary_tag:
                    summary.append(tag.get("content"))

                # Get the classification of the web page
                classification_tag = meta_soup.find_all(attrs={"name": "classification"})

                for tag in classification_tag:
                    classification.append(tag.get("content"))

                # Get the designer of the web page
                designer_tag = meta_soup.find_all(attrs={"name": "designer"})

                for tag in designer_tag:
                    designer.append(tag.get("content"))

                # Get the mail id of the web page
                mail_tag = meta_soup.find_all(attrs={"name": "reply-to"})

                for tag in mail_tag:
                    mail.append(tag.get("content"))

                # Get the owner of the web page
                owner_tag = meta_soup.find_all(attrs={"name": "owner"})

                for tag in owner_tag:
                    owner.append(tag.get("content"))

                # Get the url of the web page
                url_tag = meta_soup.find_all(attrs={"name": "url"})

                for tag in url_tag:
                    url.append(tag.get("content"))

                # Get the identifier url of the web page
                identifier_url_tag = meta_soup.find_all(attrs={"name": "identifier-url"})

                for tag in identifier_url_tag:
                    identifier_url.append(tag)

                # Get the directory of the web page
                directory_tag = meta_soup.find_all(attrs={"name": "directory"})

                for tag in directory_tag:
                    directory.append(tag.get("content"))

                # Get the page name
                pagename_tag = meta_soup.find_all(attrs={"name": "pagename"})

                for tag in pagename_tag:
                    pagename.append(tag.get("content"))

                # Get the category of the web page
                category_tag = meta_soup.find_all(attrs={"name": "category"})

                for tag in category_tag:
                    category.append(tag.get("content"))

                # Get the coverage of the web page
                coverage_tag = meta_soup.find_all(attrs={"name": "coverage"})

                for tag in coverage_tag:
                    coverage.append(tag.get("content"))

                # Get the distribution of the web page
                distribution_tag = meta_soup.find_all(attrs={"name": "distribution"})

                for tag in distribution_tag:
                    distribution.append(tag.get("content"))

                # Get the rating of the web page
                rating_tag = meta_soup.find_all(attrs={"name": "rating"})

                for tag in rating_tag:
                    rating.append(tag.get("content"))

                # Get the subtitle of the web page
                subtitle_tag = meta_soup.find_all(attrs={"name": "subtitle"})

                for tag in subtitle_tag:
                    subtitle.append(tag.get("content"))

                # Get the target of the web page
                target_tag = meta_soup.find_all(attrs={"name": "target"})

                for tag in target_tag:
                    target.append(tag.get("content"))

                # Get the date of the web page
                date_tag = meta_soup.find_all(attrs={"name": "date"})

                for tag in date_tag:
                    date.append(tag.get("content"))

                # Get the search date of the web page
                search_date_tag = meta_soup.find_all({"name": "search_date"})

                for tag in search_date_tag:
                    search_date.append(tag.get("content"))

                # Get the medium of the web page
                medium_tag = meta_soup.find_all({"name": "medium"})

                for tag in medium_tag:
                    medium.append(tag.get("content"))

                # Get the syndication source of the web page
                syndication_source_tag = meta_soup.find_all({"name": "syndication-source"})

                for tag in syndication_source_tag:
                    syndication_source.append(tag.get("content"))

                # Get the original source of the web page
                original_source_tag = meta_soup.find_all({"name": "original-source"})

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
                    result['subject'] = subject
                    result['copyright'] = copyright
                    result['language'] = language
                    result['revised'] = revised
                    result['abstract'] = abstract
                    result['topic'] = topic
                    result['summary'] = summary
                    result['classification'] = classification
                    result['designer'] = designer
                    result['mail'] = mail
                    result['owner'] = owner
                    result['url'] = url
                    result['identifier_url'] = identifier_url
                    result['directory'] = directory
                    result['pagename'] = pagename
                    result['category'] = category
                    result['coverage'] = coverage
                    result['distribution'] = distribution
                    result['rating'] = rating
                    result['subtitle'] = subtitle
                    result['target'] = target
                    result['date'] = date
                    result['search_date'] = search_date
                    result['medium'] = medium
                    result['syndication_source'] = syndication_source
                    result['original_source'] = original_source

            else:
                title_result = ''
                description_result = ''
                thumbnails_result = ''
                author_result = ''

                if len(title) > 0:
                    title_result = title[0]

                if len(description) > 0:
                    description_result = description[0]

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

                    subject_result = ''
                    copyright_result = ''
                    language_result = ''
                    revised_result = ''
                    abstract_result = ''
                    topic_result = ''
                    summary_result = ''
                    classification_result = ''
                    designer_result = ''
                    mail_result = ''
                    owner_result = ''
                    url_result = ''
                    identifier_url_result = ''
                    directory_result = ''
                    pagename_result = ''
                    category_result = ''
                    coverage_result = ''
                    distribution_result = ''
                    rating_result = ''
                    subtitle_result = ''
                    target_result = ''
                    date_result = ''
                    search_date_result = ''
                    medium_result = ''
                    syndication_source_result = ''
                    original_source_result = ''
                    keywords_result = ''

                    if len(keywords) > 0:
                        keywords_result = keywords[0]

                    if len(subject) > 0:
                        subject_result = subject[0]

                    if len(copyright) > 0:
                        copyright_result = copyright[0]

                    if len(language) > 0:
                        language_result = language[0]

                    if len(revised) > 0:
                        revised_result = revised[0]

                    if len(abstract) > 0:
                        abstract_result = abstract[0]

                    if len(topic) > 0:
                        topic_result = topic[0]

                    if len(summary) > 0:
                        summary_result = summary[0]

                    if len(classification) > 0:
                        classification_result = classification[0]

                    if len(designer) > 0:
                        designer_result = designer[0]

                    if len(mail) > 0:
                        mail_result = mail[0]

                    if len(owner) > 0:
                        owner_result = owner[0]

                    if len(url) > 0:
                        url_result = url[0]

                    if len(identifier_url) > 0:
                        identifier_url_result = identifier_url[0]

                    if len(directory) > 0:
                        directory_result = directory[0]

                    if len(pagename) > 0:
                        pagename_result = pagename[0]

                    if len(category) > 0:
                        category_result = category[0]

                    if len(coverage) > 0:
                        coverage_result = coverage[0]

                    if len(distribution) > 0:
                        distribution_result = distribution[0]

                    if len(rating) > 0:
                        rating_result = rating[0]

                    if len(subtitle) > 0:
                        subtitle_result = subtitle[0]

                    if len(target) > 0:
                        target_result = target[0]

                    if len(date) > 0:
                        date_result = date[0]

                    if len(search_date) > 0:
                        search_date_result = search_date[0]

                    if len(medium) > 0:
                        medium_result = medium[0]

                    if len(syndication_source) > 0:
                        syndication_source_result = syndication_source[0]

                    if len(original_source) > 0:
                        original_source_result = original_source[0]

                    result['keywords'] = keywords_result
                    result['subject'] = subject_result
                    result['copyright'] = copyright_result
                    result['language'] = language_result
                    result['revised'] = revised_result
                    result['abstract'] = abstract_result
                    result['topic'] = topic_result
                    result['summary'] = summary_result
                    result['classification'] = classification_result
                    result['designer'] = designer_result
                    result['mail'] = mail_result
                    result['owner'] = owner_result
                    result['url'] = url_result
                    result['identifier_url'] = identifier_url_result
                    result['directory'] = directory_result
                    result['pagename'] = pagename_result
                    result['category'] = category_result
                    result['coverage'] = coverage_result
                    result['distribution'] = distribution_result
                    result['rating'] = rating_result
                    result['subtitle'] = subtitle_result
                    result['target'] = target_result
                    result['date'] = date_result
                    result['search_date'] = search_date_result
                    result['medium'] = medium_result
                    result['syndication_source'] = syndication_source_result
                    result['original_source'] = original_source_result

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
