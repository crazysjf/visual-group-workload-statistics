import pandas as pd
import os
import re

class GoodProfile():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, path = None):
        if path != None:
            l = os.listdir(path)
            self.good_profile_file = None
            self.df = None

            for i in l:
                m = re.match(r'^商品资料.*\.xlsx$', i)
                if m != None:
                    self.good_profile_file = i
                    print("开始解析商品资料文件：%s ......" % self.good_profile_file, end='')
                    self.df =  pd.read_excel(os.path.join(path, self.good_profile_file))
                    print("完成")
                    return
            print("商品资料文件未找到")


    def has_profile(self):
        '''判断是否存在商品资料文件'''
        return not self.df is None

    def get_good_info(self,code):
        '''仅能在has_profile()返回True的情况下调用'''
        existing = False
        create_time = None

        df2 = self.df.loc[self.df['款式编码'] == code]
        if len(df2) > 0:
            existing = True
            create_time = df2.iloc[0]['创建时间']

        return (existing, create_time)
