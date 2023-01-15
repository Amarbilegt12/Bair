from bs4 import BeautifulSoup
import requests
import csv
import codecs

rooms = str(input('Enter room qty: '))
main_list = []
value = []
page_number_list = 0
main_value = []
header = ['Шал:', 'Тагт:', 'Гараж:', 'Цонх:', 'Хаалга:', 'Цонхны тоо:', 'Барилгын явц', 'Ашиглалтанд орсон он:', 'Барилгын давхар:', 'Талбай:', 'Хэдэн давхарт:', 'Лизингээр авах боломж:', 'Дүүрэг:', 'Байршил:', 'Үнэ', 'Өрөөний Тоо']
csv_list = []

url = f'https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/{str(rooms)}-r/ulan-bator/'
url_uruu = requests.get(url)
soup = BeautifulSoup(url_uruu.content, 'html.parser')
page_number = soup.find('ul', class_='number-list').text.rstrip('\n').replace('\n', '')
page_number_list += int(page_number[-2:])
if int(rooms) >= 5:
    page_number_list = str(page_number_list)[1]
    page_number_list = int(page_number_list)
print(type(page_number_list))

href_list = [a['href'] for a in soup.find_all('a', href=True)]
href_list_1 = [x.replace('/', '') for x in href_list]

for d in href_list_1:
    if len(d) == 0:
        href_list_1.remove(d)
new_list = [i[3:] for i in href_list_1 if (i[0:3] == 'adv' and '_' in i)]
main_list = main_list + new_list


for x in range(2, page_number_list+1):
    page_url = f'https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/{rooms}-r/ulan-bator/?page={x}'
    url_page = requests.get(page_url)
    soup_pages = BeautifulSoup(url_page.content, 'html.parser')
    href_list = [a['href'] for a in soup_pages.find_all('a', href=True)]
    href_list_1 = [x.replace('/', '') for x in href_list]
    for i in href_list_1:
        if len(i) == 0:
            href_list_1.remove(i)
    new_list = [i[3:] for i in href_list_1 if (i[0:3] == 'adv' and '_' in i)]
    main_list = main_list + new_list
main_list = list(set(main_list))

for i in main_list:
    html_text = requests.get(f'https://www.unegui.mn/adv/{i}/')
    print('d')
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

with codecs.open(f'UNEGUI-{rooms} uruu.csv', 'w', 'utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(csv_list)
