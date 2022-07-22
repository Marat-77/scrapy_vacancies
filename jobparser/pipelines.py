# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import re
from datetime import datetime, timedelta

import mongo_settings


class JobparserPipeline:

    def process_item(self, item, spider):
        if spider.name == 'sjru':
            # парсим superjob.ru
            item['vacancy_company_name'] = \
                self.process_sjru_vacancy_company_name(item['vacancy_company_name'])

            item['vacancy_company_link'] = self.process_sjru_vacancy_company_link(item)

            item['_id'] = self.process_sjru_id(item['vacancy_url'])

            item['min_salary'], item['max_salary'], item['cur_salary'] = \
                self.process_sjru_vacancy_salary(item['min_salary'])

            item['vacancy_creation_time'] = \
                self.process_sjru_vacancy_creation_time(item['vacancy_creation_time'])

            item['vacancy_description'] = \
                self.process_sjru_vacancy_description(item['vacancy_description'])

            item['vacancy_employment_mode'] = \
                self.process_sjru_vacancy_employment_mode(item['vacancy_employment_mode'])

            item['vacancy_require_experience'] = \
                self.process_sjru_vacancy_require_experience(item['vacancy_require_experience'])

        elif spider.name == 'hhru':
            # парсим hh.ru
            item['vacancy_url'] = self.process_vacancy_url(item['vacancy_url'])
            item['_id'] = self.process_id(item['vacancy_url'])
            item['min_salary'], item['max_salary'], item['cur_salary'] = \
                self.process_vacancy_salary(item['min_salary'])
            item['vacancy_company_name'] = \
                self.process_vacancy_company_name(item['vacancy_company_name'])
            item['vacancy_company_link'] = self.process_hhru_vacancy_company_link(item)
            item['vacancy_employment_mode'] = \
                self.process_vacancy_employment_mode(item['vacancy_employment_mode'])
            # vacancy_tag_skills
            item['vacancy_tag_skills'] = \
                self.process_vacancy_tag_skills(item['vacancy_tag_skills'])
            # vacancy_description
            item['vacancy_description'] = \
                self.process_vacancy_description(item['vacancy_description'])
            # vacancy_creation_time
            item['vacancy_creation_time'] = \
                self.process_vacancy_creation_time(item['vacancy_creation_time'])

        # # # для сохранения в MongoDB:
        mongo_settings.vacancies.insert_one(item)
        return item

    def process_vacancy_salary(self, vacancy_salary):
        min_salary = None
        max_salary = None
        cur_salary = None
        if vacancy_salary[0] == 'от ' and vacancy_salary[2] == ' до ':
            min_salary = vacancy_salary[1].replace('\xa0', '')
            max_salary = vacancy_salary[3].replace('\xa0', '')
            cur_salary = vacancy_salary[5]
        elif vacancy_salary[0] == 'от ':
            min_salary = vacancy_salary[1].replace('\xa0', '')
            cur_salary = vacancy_salary[3]
        elif vacancy_salary[0] == 'до ':
            max_salary = vacancy_salary[1].replace('\xa0', '')
            cur_salary = vacancy_salary[3]
        try:
            min_salary = int(min_salary)
        except:
            pass
        try:
            max_salary = int(max_salary)
        except:
            pass
        return min_salary, max_salary, cur_salary

    def process_vacancy_url(self, vacancy_url):
        return vacancy_url.split('?')[0]

    def process_id(self, vacancy_url):
        # print('hh_' + vacancy_url.split('vacancy/')[-1])
        return 'hh_' + vacancy_url.split('vacancy/')[-1]

    def process_vacancy_company_name(self, vacancy_company_name):
        return ''.join(vacancy_company_name[0:len(set(vacancy_company_name))])\
            .replace('\xa0', ' ')

    # vacancy_description
    def process_vacancy_description(self, vacancy_description):
        return ''.join(vacancy_description)

    def process_vacancy_employment_mode(self, vacancy_employment_mode):
        return ''.join(vacancy_employment_mode)

    def process_vacancy_tag_skills(self, vacancy_tag_skills):
        return [tag.replace('\xa0', ' ') for tag in vacancy_tag_skills]

    def process_hhru_vacancy_company_link(self, item):
        if item.get('vacancy_company_link'):
            vacancy_company_link = f"{item['vacancy_url'].split('/vacancy/')[0]}" \
                                   f"{item['vacancy_company_link'].split('?')[0]}"
        else:
            vacancy_company_link = None
        return vacancy_company_link

    def process_vacancy_creation_time(self, vacancy_creation_time):
        vacancy_creation_time = ''.join(vacancy_creation_time).replace('\xa0', ' ')
        months = {'января': '01',
                  'февраля': '02',
                  'марта': '03',
                  'апреля': '04',
                  'мая': '05',
                  'июня': '06',
                  'июля': '07',
                  'августа': '08',
                  'сентября': '09',
                  'октября': '10',
                  'ноября': '11',
                  'декабря': '12'}
        pattern = r'Вакансия опубликована (\d{1,2}\s[а-я]{3,8}\s\d{4})'
        date_ru = re.findall(pattern, vacancy_creation_time)[0]
        day = date_ru.split(' ')[0]
        day = f'{int(day):02}'
        month = date_ru.split(' ')[1]
        month = month.replace(month, months.get(month))
        year = date_ru.split(' ')[2]
        date_str = f'{year}-{month}-{day}'
        format_str = '%Y-%m-%d'
        dateformat = datetime.strptime(date_str, format_str).date()
        dateformat = datetime.combine(dateformat, datetime.min.time())
        return dateformat

    def process_sjru_id(self, vacancy_url):
        return f'sj_{vacancy_url.split("/vakansii/")[-1]}'

    def process_sjru_vacancy_company_link(self, item):
        if item.get('vacancy_company_link'):
            vacancy_company_link = f"{item['vacancy_url'].split('/vakansii/')[0]}" \
                                   f"{item['vacancy_company_link']}"
        else:
            vacancy_company_link = None
        return vacancy_company_link

    def process_sjru_vacancy_salary(self, vacancy_salary):
        vacancy_salary = [i.replace('\xa0', '') for i in vacancy_salary]
        min_salary = None
        max_salary = None
        cur_salary = None
        pattern_1 = '^(\d+)(\D+\.)$'
        if vacancy_salary[0] == 'от':
            min_cur = re.findall(pattern_1, vacancy_salary[2])
            min_salary = int(min_cur[0][0])
            cur_salary = min_cur[0][1]
        elif vacancy_salary[0] == 'до':
            max_cur = re.findall(pattern_1, vacancy_salary[2])
            max_salary = int(max_cur[0][0])
            cur_salary = max_cur[0][1]
        elif vacancy_salary[0].isdigit() and vacancy_salary[1].isdigit():
            min_salary = int(vacancy_salary[0])
            max_salary = int(vacancy_salary[1])
            cur_salary = vacancy_salary[-1]
        elif vacancy_salary[0].isdigit():
            min_salary = max_salary = int(vacancy_salary[0])
            cur_salary = vacancy_salary[-1]
        return min_salary, max_salary, cur_salary

    def process_sjru_vacancy_company_name(self, vacancy_company_name):
        if not vacancy_company_name:
            return None
        else:
            return vacancy_company_name[0]

    def process_sjru_vacancy_creation_time(self, vacancy_creation_time):
        months = {'января': '01',
                  'февраля': '02',
                  'марта': '03',
                  'апреля': '04',
                  'мая': '05',
                  'июня': '06',
                  'июля': '07',
                  'августа': '08',
                  'сентября': '09',
                  'октября': '10',
                  'ноября': '11',
                  'декабря': '12'}
        pattern_today = r'^(\d{1,2}:\d{2})$'
        pattern_date = r'^(\d{1,2})\s([а-я]{3,8})$'
        pattern_date_year = r'^(\d{1,2})\s([а-я]{3,8})\s(\d{4})$'
        if vacancy_creation_time == 'вчера':
            vac_date = datetime.today().date() - timedelta(days=1)
            vac_date = datetime.combine(vac_date, datetime.min.time())
        elif re.search(pattern_date, vacancy_creation_time):
            vac_date = re.findall(pattern_date, vacancy_creation_time)
            vac_day = vac_date[0][0]
            vac_month = vac_date[0][1]
            vac_month = months.get(vac_month)
            vac_year = datetime.today().year
            vac_date = f'{vac_year}-{vac_month}-{vac_day}'
            vac_date = datetime.strptime(vac_date, '%Y-%m-%d').date()
            vac_date = datetime.combine(vac_date, datetime.min.time())
        elif re.search(pattern_date_year, vacancy_creation_time):
            vac_date = re.findall(pattern_date_year, vacancy_creation_time)
            vac_day = vac_date[0][0]
            vac_month = vac_date[0][1]
            vac_month = months.get(vac_month)
            vac_year = vac_date[0][2]
            vac_date = f'{vac_year}-{vac_month}-{vac_day}'
            vac_date = datetime.strptime(vac_date, '%Y-%m-%d').date()
            vac_date = datetime.combine(vac_date, datetime.min.time())
        elif re.search(pattern_today, vacancy_creation_time):
            vac_date = re.findall(pattern_today, vacancy_creation_time)
            vac_time = vac_date[0]
            vac_time = datetime.strptime(vac_time, '%H:%M').time()
            vac_date = datetime.today().date()
            vac_date = datetime.combine(vac_date, vac_time)
        else:
            vac_date = None
        return vac_date

    def process_sjru_vacancy_description(self, vacancy_description):
        return ' '.join(vacancy_description)

    def process_sjru_vacancy_employment_mode(self, vacancy_employment_mode):
        vacancy_employment_mode = [i.replace('\xa0', ' ') for i in vacancy_employment_mode]
        vacancy_employment_mode = ' '.join(vacancy_employment_mode).replace('   ', ' ')
        return vacancy_employment_mode

    def process_sjru_vacancy_require_experience(self, vacancy_require_experience):
        pattern = r'^Опыт\sработы\s(.+)$'
        if re.search(pattern, vacancy_require_experience):
            return re.findall(pattern, vacancy_require_experience)[0]
        else:
            return vacancy_require_experience
