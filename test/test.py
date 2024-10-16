# import pandas as pd
#
# moudle3_result = pd.DataFrame().to_string(index=False, header=False)
# print(moudle3_result)
# import os
# import subprocess
#
# current_path = os.getcwd()
# print(current_path)
# myPopenObj = subprocess.Popen("../matlab2/test.exe")
# try:
#     myPopenObj.wait(timeout=6000)
# except Exception as e:
#     print("===== process timeout ======")
#     myPopenObj.kill()
# print("模块三计算完成")
import os

import pandas as pd

filename = '振动位移随管长变化.csv'

if os.path.exists(filename):
    df = pd.DataFrame()
    df.to_csv(filename, index=False)