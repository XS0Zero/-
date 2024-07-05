import matlab.engine

eng = matlab.engine.start_matlab()
eng.cd('../matlab2')
eng.mainfunc(nargout=0)
print("Test complete")
eng.quit()