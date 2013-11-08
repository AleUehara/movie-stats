#!/usr/bin/python
# -*- encoding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
from random import choice


class GooglePicasa():
    def __init__(self):
        self.link = "https://picasaweb.google.com/112216512556264704254/Moviestatz?authkey=Gv1sRgCJK1ztego-m1CA&noredirect=1"

    def download_html(self):
        response = urllib2.urlopen(self.link)
        self.html = response.read()

    def parse_image_links(self):
        self.download_html()
        soup = BeautifulSoup(self.html)

        result = soup.findAll('noscript', {})
        images_links =  result[1]

        soup2 = BeautifulSoup(str(images_links))
        result = soup2.findAll('img', {})

        images = []
        for image in result:
            images.append(str(image).split("\"")[1].replace("/s128/", "/s0/"))
        return images

    def random_image(self):
        images = self.parse_image_links()
        return choice(images)



def main():
    print GooglePicasa().random_image()

#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    main()