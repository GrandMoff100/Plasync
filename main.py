from plasync import EventLoop, sleep


def main():
    print("1")
    print("waiting 10")
    yield from sleep(10)
    print("4")


def two():
    print("2")
    print("waiting 11")
    yield from sleep(11)
    print("5")


def three():
    print("3")
    print("waiting 12")
    yield from sleep(12)
    print("6")


loop = EventLoop()
loop.promise(main())
loop.promise(two())
loop.promise(three())
loop.run()