import os
import re
import pandas as pd
import utils
from goods_profile import GoodProfile

def count_jpg_file(path):
    cnt = 0
    l = os.listdir(path)
    for i in l:
        i_path = os.path.join(path,i)
        ext = os.path.splitext(i)[1]
        is_jpg = False
        if ext == ".jpg" or ext == ".JPG" or ext == ".jpeg":
            is_jpg = True

        is_file = True #os.path.isfile(i_path)   此处会有比较严重的性能问题，先不判断
        if is_file and is_jpg:
            cnt = cnt + 1
    return cnt


def is_good_effective(good_path):
    '''判断商品是否有效'''

    isShot = False       # 已拍
    isProcessed = False  # 已修

    l = os.listdir(good_path)

    # 判断文件夹下是否有10个以上jpg文件
    jpg_cnt = count_jpg_file(good_path)
    if jpg_cnt >= 10:
        isShot = True

    images_dir_found = False
    for i in l:
        i_path = os.path.join(good_path,i)
        if os.path.isdir(i_path):
            l2 = os.listdir(i_path)
            for i2 in l2:
                if i2 == 'images':
                    cnt = count_jpg_file(os.path.join(i_path,i2))
                    if cnt >= 10:
                        isProcessed = True
    return (isShot, isProcessed)




def handle_good(good_path):
    '''
    判断款是否有效，有效返回字典，包含一下内容：
    code：商品编码
    orig_str：原始文件夹字符串
    is_effective：是否是有效款
    :param good_str:
    :return:
    '''
    print("正在统计：" + good_path)
    orig_str = os.path.basename(good_path) # 宝贝文件夹的名字

    ret = {}
    ret['orig_str'] = orig_str

    m = re.match(r'^(.+-[^\s]+)', orig_str)
    code = None
    if m != None:
       code = m.group(0)

    ret['code'] = code

    (isShot, isProcessed) = is_good_effective(good_path)
    ret['isShot'] = isShot
    ret['isProcessed'] = isProcessed
    ret['isOnShelf'] = "未知"
    ret['create_time'] = None

    gp = GoodProfile()
    if gp.has_profile():
        (ret['isOnShelf'], ret['create_time']) = gp.get_good_info(code)

    return ret

def handle_one_day(day_path):

    ret_list = []
    goods = os.listdir(day_path)
    for g in goods:
        # 忽略#开头商品
        m = re.match(r'^#.*', g)
        if m != None:
            continue

        good_path = os.path.join(day_path,g)
        ret_list.append(handle_good(good_path))

    return ret_list

def analyze(path, day=None):
    '''
    分析指定文件夹。
    :param path: 月份文件夹
    :return: 结果字典
    '''
    if day != None:
        days = [day]
    else:
        days = os.listdir(path)

    dict = {}

    cnt = 0
    for day in utils.sort_dates(days):
        day_path = os.path.join(path, day)
        if not os.path.isdir(day_path):
            continue

        dict[day] = handle_one_day(day_path)
        cnt = cnt +1
        # if cnt >= 3:
        #     break

    return dict


def dump_dict(dict):
    for date in utils.sort_dates(dict.keys()):
        print("日期：" + date)
        good_list = dict[date]
        for g in good_list:
            print("   款号：%s, 已拍：%s, 已修：%s, 原始字符串：%s" %(g['code'], g['isShot'], g['isProcessed'], g['orig_str']))

def write_to_exel(dict, path):
    writer = pd.ExcelWriter(os.path.join(path, '统计结果.xlsx'))

    df = pd.DataFrame(columns = ['日期', '已拍', '已修'])
    for date in utils.sort_dates(dict.keys()):
        good_list = dict[date]
        nr_shot = 0
        nr_processed = 0
        for g in good_list:
            if g['isShot']:
                nr_shot = nr_shot + 1
            if g['isProcessed']:
                nr_processed = nr_processed + 1


        r = {"日期":date, "已拍": nr_shot, "已修": nr_processed}
        df = df.append(r,ignore_index=True)
    df.to_excel(writer, "汇总", index=False)



    df = pd.DataFrame(columns = ['日期', '款号', '已拍', '已修', '已上架', '创建时间', '原始字符串'])
    for date in utils.sort_dates(dict.keys()):
        good_list = dict[date]
        for g in good_list:
            r = {"日期":date, "已拍": int(g['isShot']), "已修": int(g['isProcessed']), "款号": g['code'], "已上架": int(g['isOnShelf']), "创建时间": g['create_time'], "原始字符串": g['orig_str']}
            df = df.append(r,ignore_index=True)

    df.to_excel(writer, "详情", index=False)
    writer.save()

def start_work():
    month_path = None

    # 调试时使用
    #root_path = os.path.dirname(__file__)
    root_path = "Z:\\"  # 月份文件夹


    print("生产部门工作量统计工具")
    print("该工具必须放到存放所有月份图片的位置才能使用")



    while True:
        month = input("请输入月份(2位数字)：")
        month_path = "%s\%s月" % (root_path, month)
        if os.path.isdir(month_path):
            print("开始统计文件夹：%s" % month_path)
            break
        else:
            print("未找到文件夹：%s，请确认输入是否有误" % month_path)


    GoodProfile(month_path) # 必须以路径为参数初始化GoodProfile
    dict = analyze(month_path)
    dump_dict(dict)
    write_to_exel(dict, month_path)
    input("统计完成")

import cProfile
if __name__ == "__main__":
    #cProfile.run("start_work()",   sort="cumulative")
    start_work()