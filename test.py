
from bs4 import BeautifulSoup
import requests
import csv
import codecs

main_list = ['6847668_1-oroo-bair-yaraltai-zarna', '6844653_khotyn-tov-bokhiin-orgoond-gal-togoo-tusdaa-1oroo-bair-zarna']
header = ['Шал:', 'Тагт:', 'Гараж:', 'Цонх:', 'Хаалга:', 'Цонхны тоо:', 'Барилгын явц', 'Ашиглалтанд орсон он:', 'Барилгын давхар:', 'Талбай:', 'Хэдэн давхарт:', 'Лизингээр авах боломж:', 'Дүүрэг:', 'Байршил:', 'Үнэ', 'Өрөөний Тоо']
csv_list = []
main_value = []
for i in main_list:
        html_text = requests.get(f'https://www.unegui.mn/adv/{i}/')
        soup = BeautifulSoup(html_text.content, 'html.parser')
        soup_all = soup.find_all('div', class_='announcement-characteristics clearfix')
        result_1 = soup.find_all('span', class_='value-chars')
        result_2 = soup.find_all('a', class_='value-chars')
        value_1 = [x.text.rstrip() for x in result_1]
        value_2 = [x.text.rstrip() for x in result_2]
        value_3 = soup.find('div', class_='announcement-price__cost').text.rstrip('\n').strip(' ').replace(' ', '')[3:]
        value_4 = soup.find('div', class_='wrap js-single-item__location').find_all('span')[-1].text
        main_value = (value_1 + value_2)
        main_value.append(value_3)
        main_value.append(value_4)
        sub_dic = dict(zip(header, main_value))
        csv_list.append(sub_dic)
print(csv_list)

with codecs.open('test_1.csv', 'w', 'utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(csv_list)









