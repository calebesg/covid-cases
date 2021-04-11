import json
import pandas
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

url = "https://www.google.com/search?q=numero+de+casos+de+coronavirus+no+mundo&source=hp&ei=vLJvYJpgs9fk5Q_pjb3ICQ&iflsig=AINFCbYAAAAAYG_AzLX_OlfJdLHTIggDcI1kmYejKj7d&oq=numero+de+casos+de+coronavirus+no+&gs_lcp=Cgdnd3Mtd2l6EAMYATIICAAQsQMQgwEyCAgAELEDEIMBMgIIADICCAA6BQgAELEDOggIABDHARCjAjoLCAAQsQMQgwEQyQM6BQgAEJIDUL0SWMRDYLVUaAFwAHgAgAF5iAHKEJIBBDAuMTmYAQCgAQGqAQdnd3Mtd2l6sAEA&sclient=gws-wiz"

browser = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())
browser.get(url)
browser.implicitly_wait(10)

browser.find_element_by_xpath(f"//div[@class='oCEWs']").click()

element = browser.find_element_by_xpath(f"//div[@class='ZDcxi']//table")
html_content = element.get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find('table')

data_frame = pandas.read_html(str(table))[0].head(10)
data_frame = data_frame[['Local', 'Casos', 'Recuperados', 'Mortes']]

list_cases = data_frame.to_dict('records')

browser.quit()


def format_interator(interator):
    cases = str(interator['Casos'])
    recovered = str(interator['Recuperados'])
    deaths = str(interator['Mortes'])

    cases = cases.split("\xa0")[0] + " mi"

    if recovered != '-':
        recovered = recovered.split("\xa0")[0] + " mi"

    deaths = deaths.split("\xa0")[0] + " mil"

    return {
        'Local': interator['Local'],
        'Casos': cases,
        'Recuperados': recovered,
        'Mortes': deaths
    }


format_cases = map(format_interator, list_cases)

with open('covid-cases.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(list(format_cases), ensure_ascii=False, indent=4)
    print(js)
    jp.write(js)

