import matlab.engine


# ����ģ��matlab��������
def matlab_function():
    eng = matlab.engine.start_matlab()
    eng.cd('../matlab2')
    eng.mainfunc(nargout=0)
    print("Test complete")
    eng.quit()
    return True



def