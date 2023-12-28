import pandas as pd
import os,shutil



class fileManager:

    def readFile(self,file):
        file,ext = file.split('.')
        data_frame = pd.DataFrame()
        try:
            if ext == 'csv':
                data_frame = pd.read_csv(f"{file}.{ext}")
            elif ext == 'xlsx':
                data_frame = pd.read_excel(f"{file}.{ext}")
        except Exception as ex:
            return pd.DataFrame()

        return data_frame 
    
    def save(self,name = None,trig=False,**kwargs):
        if name:
            self.file = name  

        try:
            dataframe = pd.read_excel(f"{self.file}.xlsx")
        except FileNotFoundError:
            dataframe = pd.DataFrame()        
        
        if trig:
            dataframe1 = pd.DataFrame(kwargs)
        else:
            dataframe1 = pd.DataFrame([kwargs])

        dataframe = pd.concat([dataframe,dataframe1],ignore_index=True)
        dataframe.to_excel(f"{self.file}.xlsx",index=False)
    
    def remove_file(self):
        try:
            os.remove(f"{self.file}") if "xlsx" in self.file else os.remove(f"{self.file}.xlsx")    
        except Exception as ex:
            pass

    def cleanTemp(self):
        temp_path = os.environ.get('TMP')
        temp_files  = os.listdir(temp_path)
        if temp_files:
            for file in temp_files:
                try:                  
                    if os.path.isdir(os.path.join(temp_path,file)):
                        shutil.rmtree(os.path.join(temp_path,file))
                    else:
                        os.remove(os.path.join(temp_path,file))
                except Exception as ex:
                    continue   
    
    def colateTempFiles(self):
        list_of_xl_dataframe = list()
        path = os.path.join(os.getcwd())
        list_dir = os.listdir(path)

        for file in list_dir:
            list_of_xl_dataframe.append(pd.read_excel(f"{path}/{file}"))
        
        col_xl = pd.concat(list_of_xl_dataframe,ignore_index=True)
        col_xl.to_excel(f"{self.file}",index=False)

        shutil.rmtree(path=path)