from sys import argv
from subprocess import call


# TODO: this file!


class Commander(object):

    def start(self):
        if not self.check():
            pass  # CMD: python src > out.log
        # print call(["python", "src"])

    def stop(self):
        # TODO: remove this process from the command
        if self.check():
            pass  # ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9

    def update(self):
        reload = self.check()
        if reload:
            self.stop()
        # CMD: git pull
        if reload:
            self.start()

    @ staticmethod
    def check():
        # TODO: determine if process is running!!!
        # CMD: ???
        return False

    def restart(self):
        if self.check():
            self.stop()
        self.start()


if __name__ == '__main__':
    cmd = Commander()
    task = argv[1] if argv and len(argv) == 2 else None
    task = task if task and hasattr(cmd, task) else None
    if not task:
        print 'Usage (start|stop|update|check|restart)'
        exit(1)
    getattr(cmd, task)()
