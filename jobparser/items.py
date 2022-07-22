# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    vacancy_title = scrapy.Field()
    vacancy_url = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    cur_salary = scrapy.Field()
    vacancy_company_name = scrapy.Field()
    vacancy_company_link = scrapy.Field()
    vacancy_require_experience = scrapy.Field()
    vacancy_employment_mode = scrapy.Field()
    vacancy_tag_skills = scrapy.Field()
    vacancy_description = scrapy.Field()
    vacancy_creation_time = scrapy.Field()
