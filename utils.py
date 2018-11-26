
def sort_dates(date_array):
    '''
    对日期进行排序。
    假设参数为： = ['11.1','11.11','11.12','11.2','11.3','11.4','11.5','xxx']
    返回：
    :param date_array:
    :return: ['xxx', '11.1', '11.2', '11.3', '11.4', '11.5', '11.11', '11.12']
    '''

    def get_date_in_month(date):
        s = date.split('.')
        if len(s) < 2:
            return 0
        else:
            try:
                return int(s[1])
            except:
                return 0


    return sorted(date_array, key=get_date_in_month)

if __name__ == "__main__":
    a = ['11.1','11.11','11.12','11.2','11.3','11.4','11.5','xxx', 'xxx.xxx']
    print(sort_dates(a))