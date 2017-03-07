
def run():
    for i in range(1, 100):
        yield i
        yield i+100

for j in run():
    print j
