from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from customFileManager import fileManager
from Utilis import utils
from bs4 import BeautifulSoup

import sys, os, multiprocessing
import undetected_chromedriver as uc




class customSelenium(fileManager,utils):
    __ver__ = '3.0' #Version of Custom Selenium 
    __dev__ = 'Vicky P' # Developed By 


    def __init__(self) -> None:      
        self.wait = None
        self.driver = None
        self.chrome_ext = None
        self.file = self.__class__.__name__
        self.random_user_agent = self.random_user()         
        self.lock =  multiprocessing.Manager().Lock()
        
    def intializeDriver(self):
        if self.driver is None:
            self.driver = self.browser()
            self.wait = WebDriverWait(self.driver,30)

    def closeDriver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
    
    def browser(self,head=False):                  
        options = uc.ChromeOptions()
        

        options.add_argument("--disable-popup-blocking")
        # options.add_argument("--force-device-scale-factor=0.8")

        # options.add_experimental_option('prefs' ,{
        #     "download.default_directory": os.path.join(os.getcwd() , "CaptchaImage")
        # })

        # if not os.path.exists(os.path.join(os.getcwd() , "CaptchaImage")):
        #     os.mkdir(os.path.join(os.getcwd() , "CaptchaImage"))

        if self.chrome_ext is not None:
            options.add_argument(f'--load-extension={self.chrome_ext}')  

        # browser_executable_path = ".\Google\Chrome\Application\chrome.exe"

        # if not os.path.exists(browser_executable_path):
        #     print('Chrome Folder Missing, make sure chrome folder exist in current working directory.')
        #     input()
        #     sys.exit(0)
            

        try:
            driver = uc.Chrome(
                options=options,
                use_subprocess=True,
                headless=head,
                # browser_executable_path=browser_executable_path
            )            
        except Exception as ex:            
            print('Chrome Intializing Error...probably Version error \n') 
            input()          
            sys.exit(0)   

        driver.maximize_window()
        print('Chrome Intialized...')
        return driver
                
    def getXpathValue(self,xpath_Id,all_elements=False,wait_time = 15):        
        self.wait = WebDriverWait(self.driver,wait_time)
        
        if all_elements:
            locate_element = EC.presence_of_all_elements_located
        else:
            locate_element = EC.presence_of_element_located        
        
        try:
            value = self.wait.until(locate_element((By.XPATH, xpath_Id)))
        except Exception as ex:
            value = None   
        return value    
    
    def openNewWindow(self):
        try:
            self.driver.execute_script("window.open(arguments[0], '_blank')")
            self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as ex:
            print(ex)
            print("Driver is not available. Make sure the driver is started.")
        return self.driver
    
    def click(self,xpath,wait_time=15):
        self.wait = WebDriverWait(self.driver,wait_time)
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
            self.scrollToElement(element=element)
            self.randomSleep(2,3)
            element.click()
            return True
        except Exception as ex:
            return False
            
    def getPageSource(self,element=None):
        try:
            if element:
                source = element.get_attribute("innerHTML")
            else:
                source = self.driver.page_source              
            soup = BeautifulSoup(source,'lxml')            
        except Exception as ex : 
            soup = None
        
        return soup

    def scrollToElement(self,element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});",element)
        except:
            return False
        
    def loadExtension(self,name,version):
        self.chrome_ext = os.path.join(os.getcwd(),name,version)
    
    def closeExtensionTab(self):
        try:
            self.get_Xpath_value(xpath_Id='//p[@class="installed-loading__lead-paragraph"]')
            self.driver.switch_to.window(self.driver.window_handles[-1])  
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
        except:
            print('Disk Full ....Free Up Some Space')
            sys.exit(0)
           
    def execute(self):
        #checking 
        # if already file exist , it will continue.        
        dataframe = self.readFile(f"{self.file}_link.xlsx")
        if dataframe.size != 0:
            dataframe = dataframe['Links']
            self.file = f"{self.file}_link.xlsx"
            print("\nExtraction Resumes...")
        else:
            self.scrapeLinks()
        
        self.driver.close() 
        
        #reading new excel file which was created by scrapeLinks method
        if dataframe.size == 0:
            dataframe = self.readFile(f"{self.file}.xlsx")
            
            if dataframe.size == 0:
                print("There is no links left to extract.")
                return  
        
        # Number of Processer will be auto choosed, depends on the size of file
        if dataframe.size > 10 and dataframe.size < 20:
            processes = 2
        elif dataframe.size <= 5:
            processes = 1
        else:
            processes = int(multiprocessing.cpu_count()) // 2
            
        
        linksChunks = self.chunk_list(dataframe,processes)        
        instance = self.__class__()
        
        print("Relax Now ...Extracting Data From the Links.\n")
        
        with multiprocessing.Pool(processes=processes) as pool:            
            pool.starmap(instance.scrape_data, [(instance, url_chunk) for url_chunk in linksChunks])

        print("Extraction Completed\n")
        
                
            
                
            

    
    
    