from random import randint,choice
from datetime import datetime

import sys,time

class utils:
    
    def dateTime(self):
        return datetime.today().timestamp()   
    
    def chunk_list(self, data, num_chunks):
        chunk_size, remainder = divmod(len(data), num_chunks)
        chunks = []
        start = 0

        for i in range(num_chunks):
            if i < remainder:
                end = start + chunk_size + 1
            else:
                end = start + chunk_size

            chunks.append(data[start:end])
            start = end

        return chunks
    
    def validateData(self,element):
        if element :
            return element.text
        return None
    
    def stop_execute(self,mesg=None):
        print(mesg)
        input()
        self.close()
        sys.exit(0)

    def random_user(self):
        browsers = (
            "Mozilla",
            "Opera",
            "Internet Explorer",
            "Chrome",
            "Safari",
        )

        operating_system = (
            "Windows NT 10.0; Win64; x64",
            "Windows NT 6.1; WOW64",
            "Macintosh; Intel Mac OS X 10_15_4",
            "X11; Linux x86_64",
            "Android 10.0; Mobile",
            "iOS 13.4; iPhone",
        )

        version = {
            "Mozilla": f"{randint(3, 15)}.0",
            "Opera": f"{randint(3, 15)}.80",
            "Internet Explorer": f"{randint(3, 15)}.0",
            "Chrome": f"{randint(70, 110)}.0.3987.{randint(100, 999)}",
            "Safari": f"{randint(500, 550)}.36",
        }

        browser = choice(browsers)
        os = choice(operating_system)
        browser_version = version[browser]

        user_agent = f"{browser}/{browser_version} ({os})"

        return user_agent
    
    def randomSleep(self,start,end):        
        time.sleep(randint(start,end))


    