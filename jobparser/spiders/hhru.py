import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from jobparser import mongo_settings


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    # список стартовых адресов
    start_urls = ['https://hh.ru/search/vacancy?area=113'
                  '&industry=44&industry=42&industry=41&industry=13'
                  '&search_field=name&search_field=description&text=python'
                  '&clusters=true&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=1&industry=7'
                  '&search_field=name&search_field=description&text=python'
                  '&clusters=true&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=2&industry=7'
                  '&search_field=name&search_field=description&text=python'
                  '&clusters=true&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=3&industry=7'
                  '&search_field=name&search_field=description&text=python'
                  '&clusters=true&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=4&industry=7'
                  '&search_field=name&search_field=description&text=python'
                  '&clusters=true&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=223'
                  '&search_field=name&search_field=description&text=python'
                  '&clusters=true&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=227'
                  '&search_field=name&search_field=description&text=python'
                  '&clusters=true&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=113'
                  '&clusters=true&enable_snippets=true&items_on_page=20'
                  '&no_magic=true&ored_clusters=true'
                  '&search_field=name&search_field=description&text=python'
                  '&search_period=1&hhtmFrom=vacancy_search_list',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=1'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&search_field=name'
                  '&search_field=description&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=2'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&search_field=name'
                  '&search_field=description&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=88'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&search_field=name'
                  '&search_field=description&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=3'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&search_field=name'
                  '&search_field=description&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=99'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&search_field=name'
                  '&search_field=description&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=113&schedule=remote'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&search_field=name'
                  '&search_field=description&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=113'
                  '&search_field=name&text=python'
                  '&from=suggest_post',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=1'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&search_field=name'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=2'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&search_field=name'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=3'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&search_field=name'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=1'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20'
                  '&search_field=description&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=2'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20'
                  '&search_field=description&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=3'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20'
                  '&search_field=description&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?text=python'
                  '&salary=&clusters=true&area=113'
                  '&no_magic=true&ored_clusters=true'
                  '&items_on_page=20&search_field=name'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=113'
                  '&schedule=fullDay'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=1'
                  '&schedule=fullDay'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=3'
                  '&schedule=fullDay'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=2'
                  '&schedule=fullDay'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=4'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=113'
                  '&experience=between1And3'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=1'
                  '&experience=between1And3'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=2'
                  '&experience=between1And3'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=113'
                  '&experience=between3And6'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=1'
                  '&experience=between3And6'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=2'
                  '&experience=between3And6'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=113'
                  '&experience=moreThan6'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=1'
                  '&experience=moreThan6'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=2'
                  '&experience=moreThan6'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=113'
                  '&experience=noExperience'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=1'
                  '&experience=noExperience'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1',
                  'https://hh.ru/search/vacancy?area=2'
                  '&experience=noExperience'
                  '&search_field=name&search_field=description'
                  '&text=python&clusters=true&no_magic=true'
                  '&ored_clusters=true&items_on_page=20'
                  '&enable_snippets=true&customDomain=1']

    def parse(self, response: HtmlResponse):
        # находим кнопку "далее":
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        # проверяем если есть "далее":
        if next_page:
            # запускаем parse следующей страницы
            yield response.follow(next_page, callback=self.parse)
        # ссылки вакансий на странице:
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href')\
            .getall()
        # перебираем все ссылки из списка links:
        for link in links:
            # проверяем отсутствие выбранной ссылки в БД:
            if not mongo_settings.vacancies.find_one({'_id': 'hh_' + link.split('?')[0].split('vacancy/')[-1]}):
                # запускаем vacancy_parse:
                yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_title = response.xpath('//h1[@data-qa="vacancy-title"]/text()').get()
        vacancy_url = response.url
        vacancy_salary = response\
            .xpath('//div[contains(@data-qa, "vacancy-salary")]/span/text()').getall()
        vacancy_company_name = response\
            .xpath('//a[@data-qa="vacancy-company-name"]//text()').getall()
        vacancy_company_link = response\
            .xpath('//a[@data-qa="vacancy-company-name"]/@href').get()
        vacancy_require_experience = response\
            .xpath('//p[@class="vacancy-description-list-item"]/span//text()').get()
        vacancy_employment_mode = response\
            .xpath('//p[@data-qa="vacancy-view-employment-mode"]//text()').getall()
        # # Ключевые навыки:
        vacancy_tag_skills = response\
            .xpath('//div[@class="bloko-tag-list"]//text()').getall()
        vacancy_description = response\
            .xpath('//div[@data-qa="vacancy-description"]//text()').getall()
        vacancy_creation_time = response\
            .xpath('//p[contains(@class, "vacancy-creation-time")]//text()').getall()
        yield JobparserItem(vacancy_title=vacancy_title,
                            vacancy_url=vacancy_url,
                            min_salary=vacancy_salary,
                            vacancy_company_name=vacancy_company_name,
                            vacancy_company_link=vacancy_company_link,
                            vacancy_require_experience=vacancy_require_experience,
                            vacancy_employment_mode=vacancy_employment_mode,
                            vacancy_tag_skills=vacancy_tag_skills,
                            vacancy_description=vacancy_description,
                            vacancy_creation_time=vacancy_creation_time)

