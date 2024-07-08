import matlab.engine


# 第三模块matlab函数调用
def matlab_function():
    eng = matlab.engine.start_matlab()
    eng.cd('../matlab2')
    eng.mainfunc(nargout=0)
    print("Compute complete")
    eng.quit()
    return True


if __name__ == '__main__':
    matlab_function()
