import urllib2, sys, re
from HTMLParser import HTMLParser

class AmazonAppHTMLParser(HTMLParser):
    _appinfo = {}

    def __init__(self):
        """
        Initializing member variables, mostly flags
        """
        HTMLParser.__init__(self)
        self.inTitle = False
        self.inStrong = False
        self.checkChangelog = False
        self.inChangelog = False
        self.checkReleasedate = False
        self.inProductdetails = False
        self.inReleasetag = False

    def handle_starttag(self, tag, attrs):
        """
        Evaluate start tags while parsing HTML and set flags accordingly
        """
        self.inTitle = False
        self.inStrong = False
        self.inChangelog = False
        self.inReleasetag = False

        if tag == 'title':
            self.inTitle = True
        if tag == 'strong':
            self.inStrong = True
        if tag == 'li':
            if self.checkChangelog:
                self.inChangelog = True
            elif self.inProductdetails:
                self.checkReleasedate = True
        if tag == 'table':
            for name, value in attrs:
                if name == 'id' and value == 'productDetailsTable':
                    self.inProductdetails = True
                    break 

    def handle_endtag(self, tag):
        """
        Parse end tags and evaluate based on appropriately flagged start tags
        """
        if tag == 'title':
            self.inTitle = False
        if tag == 'ul':
            self.checkChangelog = False
            self.inChangelog = False
        if tag == 'table':
            self.checkReleasedate = False
        if tag == 'li' and self.inReleasetag:
            self.inReleasetag = False

    def handle_data(self, data):
        """
        Encounter parsed data and assign to global member variable accordingly
        """
        if self.inTitle:
            title = re.match('Amazon.com: (.*): Appstore for Android', data)
            self._appinfo['appName'] = title.group(1)
            self._appinfo['changelog'] = []
        if self.inStrong:
            if re.match('What\'s new in version', data):
                version = re.match('What\'s new in version (.*)$', data)
                self._appinfo['appVersion'] = version.group(1)
                self.checkChangelog = True
            else:
                self.inStrong = False
        if self.inChangelog:
            if not data.strip():
                return
            self._appinfo['changelog'].append(data)
        if self.checkReleasedate:
            if re.match('Original Release Date', data):
                self.inReleasetag = True
            elif self.inReleasetag:
                self._appinfo['release'] = data

    def extract(self):
        return self._appinfo

def getAppInfo(url):
    """
    Global function for extracting collated data
    """
    try:
        curl = urllib2.urlopen(url)
        html = curl.read()
        curl.close()
    except urllib2.HTTPError as e:
        return {'appName': 'ERROR'}

    parser = AmazonAppHTMLParser()
    parser.feed(html)

    return parser.extract()

