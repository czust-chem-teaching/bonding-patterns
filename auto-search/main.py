import time
import feapder
import warnings
from feapder.utils.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

warnings.filterwarnings('ignore')


class ChemSpiderRender(feapder.AirSpider):

    __custom_setting__ = dict(
        WEBDRIVER=dict(
            pool_size=1,  
            load_images=True,  
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",  # 字符串 或 无参函数，返回值为user_agent
            proxy=None,  
            headless=True,  
            driver_type="CHROME", 
            timeout=10,  
            window_size=(1024, 800),  
            executable_path=None, 
            render_time=10, 
            custom_argument=["--ignore-certificate-errors"], 
            xhr_url_regexes=[
                "/ad",
            ], 
        )
    )

    def __init__(self, elements: list[str]):
        super(ChemSpiderRender, self).__init__()
        self.elements = elements
        self.search_results = []

    def start_requests(self):
        yield feapder.Request("https://www.chemspider.com/search", render=True)

    def download_midware(self, request):
       
        request.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Cookie": "_hjSessionUser_963523=eyJpZCI6ImIzYzAzYTgwLTkwZmUtNTk0OS1iYzJmLTEzOTVkMTFjZGMwNiIsImNyZWF0ZWQiOjE3NDM3MzgwMDgzOTUsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.981429833.1743738009; OptanonAlertBoxClosed=2025-04-04T03:40:35.237Z; _hjMinimizedPolls=1516018; _hjDonePolls=1516018; _hjSession_963523=eyJpZCI6IjM3MmEwMDRlLWY4ZDEtNGUxYS1iYTE2LTRiYzIzZGFkMzQyYiIsImMiOjE3NDM3NDEzODk5NzksInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Apr+04+2025+13%3A47%3A39+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202408.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=024d8d8c-5a6c-4237-99c5-1b11d18490eb&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CSPD_BG%3A1%2CC0002%3A1%2CC0004%3A1&intType=3&geolocation=US%3BCA&AwaitingReconsent=false; _ga_11D1F0F537=GS1.1.1743745445.2.1.1743746557.0.0.0"
        }
        return request

    def parse(self, request, response):
        browser: WebDriver = response.browser
        
        for element in self.elements:
            print("=" * 20 , element, "=" * 20)
            try:
                browser.find_element(value="input-left-icon").click()
                browser.find_element(value="input-left-icon").clear()
                time.sleep(0.5)
                browser.find_element(value="input-left-icon").send_keys(f"{element} ", Keys.ENTER)
                time.sleep(5)

                df_search_result_table = pd.read_html(browser.page_source)[0]  
                # print(len(df_search_result_table.columns))
                # print(df_search_result_table.values)

                if len(df_search_result_table.columns) == 5:
                    if df_search_result_table.shape[0] > 0:
                        df_search_result_table['Synonym'] = df_search_result_table['Synonym'].map(
                            lambda s: s[:int(len(s.replace('Charge', '')) / 2)]
                        )

                if len(df_search_result_table.columns) == 2:
                    element_detail_extract = {}

                    for value in df_search_result_table.values:
                        if value[0] == 'Molecular formula:':
                            element_detail_extract['Mol formula'] = [value[1]]

                        if value[0] == 'Average mass:':
                            element_detail_extract['Average Mass'] = [value[1]]

                    synonym_element = browser.find_element(by=By.CSS_SELECTOR, value='#accordion-names-and-synonyms > div > div.expansion-panel-text > div > div:nth-child(2) > p')
                    element_detail_extract['Synonym'] = [synonym_element.text]
                    element_detail_extract['# of Data Sources'] = 1
                    df_search_result_table = pd.DataFrame.from_dict(element_detail_extract)

            except Exception:
                df_search_result_table = pd.DataFrame([[None, None, None, None, None]],
                                                      columns=['Synonym', 'Structure', 'Mol formula', 'Average Mass',
                                                               '# of Data Sources'])

            df_search_result_table['Element'] = element
            self.search_results.append(
                df_search_result_table[['Element', 'Synonym', 'Mol formula', 'Average Mass', '# of Data Sources']]
            )
            browser.get("https://www.chemspider.com/search")
            time.sleep(5)

    def save_results(self):
        df = pd.concat(self.search_results, ignore_index=True)
        
        df[['Element', 'Synonym', 'Mol formula', 'Average Mass', '# of Data Sources']].to_csv("chem_spider_results.csv", index=False)


def extract_elements_from_file(filename: str):
    with open(filename, 'r') as f:
        elements = [line.strip() for line in f.readlines()]
    return elements


if __name__ == "__main__":
    
    search_elements = extract_elements_from_file("elements-pair.txt")
    chem_spider = ChemSpiderRender(elements=search_elements)
    chem_spider.start()
    chem_spider.save_results()
