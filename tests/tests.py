from pub.url_benchmark import Command


def test_base():
    arguments = ["localhost", 20]
    cmd = Command(arguments=arguments)
    cmd.run()
