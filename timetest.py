import time

t0 = time.time()
for i in range(1000):
    vartest = {
        "x": 10
    }
    vartest = {
        "x": vartest["x"]*2
    }
#    vartest = 10
#    vartest = vartest*2
t1 = time.time()

print(t1-t0)