#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.http import Request

class GamesSpider(Spider):
    name = 'gamespot'
    allowed_domains = ['www.gamespot.com']
    start_urls = ['https://www.gamespot.com/reviews/']

    def parse(self, response):
        games = response.css('.media.media-game.media-game')
        for g in games:
            title = g.css('.media-title::text').extract_first()
            title = title.replace(',', '')
            rating_num = g.css('.content::text').extract_first()
            rating_word = g.css('.score-word::text').extract_first()
            review = g.css('.media-deck::text').extract_first()
            game_url =  g.xpath(".//@href").extract_first()
            game_url = game_url.replace('/reviews','https://www.gamespot.com/reviews')
            
            yield scrapy.Request(game_url,
                            callback=self.parse_game,
                            meta={'Title': title,
                                 'Rating Number': rating_num,
                                 'Rating Word': rating_word,
                                 'Review': review,
                                 })
           
        nextPageLinkSelector = response.xpath('.//*[@class="paginate__item skip next"]/a/@href').extract_first()
        if nextPageLinkSelector:
            yield scrapy.Request(response.urljoin(nextPageLinkSelector), callback=self.parse)

    def parse_game(self, response): 
        title = response.meta['Title']
        rating_num = response.meta['Rating Number']
        rating_word = response.meta['Rating Word']
        review = response.meta['Review']

        
        author_info = response.xpath('normalize-space(.//*[@class="authorCard-deck"]/text())').extract_first()
        
        yield {'Title': title,
               'Rating Number': rating_num,
               'Rating Word': rating_word,
               'Review': review,
               'Author Information': author_info
               }

    