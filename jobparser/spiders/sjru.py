import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from jobparser import mongo_settings


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    # список стартовых адресов
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']  # +++

    def parse(self, response: HtmlResponse):
        # находим кнопку "далее":
        next_page = response.xpath(
            '//span[contains(text(),"Дальше")]/parent::span/parent::span/parent::a/@href').get()  # +++
        # проверяем если есть "далее":
        if next_page:
            # запускаем parse следующей страницы
            yield response.follow(next_page, callback=self.parse)
        # ссылки вакансий на странице:
        links = response.xpath(
            '//div[contains(@class, "f-test-clickable")]//a[contains(@href, "vakansii")]/@href').getall()  # +++
        # перебираем все ссылки из списка links:
        for link in links:
            # проверяем отсутствие выбранной ссылки в БД:
            if not mongo_settings.vacancies.find_one({'vacancy_url': link}):  # +++
                # запускаем vacancy_parse:
                yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_title = response.xpath('//h1//text()').get()  # +++
        # vacancy_title = response.xpath('//h1//text()').getall()
        vacancy_url = response.url

        vacancy_salary = response.xpath(
            '//div[contains(@class, "f-test-address _2Ql_s")]/following-sibling::span/span[1]/text()').getall()  # +++
        vacancy_company_name = response.xpath(
            '//h1/parent::div/parent::div/following-sibling::div//a/div//text()').getall()  # +++
        vacancy_company_link = response.xpath(
            '//h1/parent::div/parent::div/following-sibling::div//a/div/parent::a/@href').get()  # +++
        vacancy_require_experience = response.xpath('//span[contains(text(),"Опыт работы")]//text()').get()  # +++
        vacancy_employment_mode = response.xpath(
            '//span[contains(text(),"Опыт работы")]/following-sibling::span//text()').getall()  # +++

        # # Ключевые навыки: none----------------------------

        vacancy_description = response.xpath(
            '//h1/parent::div/parent::div/parent::div/following-sibling::div//text()').getall()  # +++

        vacancy_creation_time = response.xpath(
            '//div[contains(@class, "f-test-title")]/div[2]/span/text()').get()  # +++

        yield JobparserItem(vacancy_title=vacancy_title,
                            vacancy_url=vacancy_url,
                            min_salary=vacancy_salary,
                            vacancy_company_name=vacancy_company_name,
                            vacancy_company_link=vacancy_company_link,
                            vacancy_require_experience=vacancy_require_experience,
                            vacancy_employment_mode=vacancy_employment_mode,
                            vacancy_description=vacancy_description,
                            vacancy_creation_time=vacancy_creation_time)
