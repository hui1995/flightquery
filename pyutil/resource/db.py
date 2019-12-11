# coding: utf-8
import pymysql


class DAL(object):
    def __init__(self, host, port, user, passwd, db, retry=1):
        self.conn = None
        self.cur = None
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.retry = retry

    def open(self):
        if not self.conn or not self.cur:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                charset='utf8',
                autocommit=True
            )
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def execute(self, cmd, *args):
        while True:
            try:
                self.open()
                self.cur.execute(cmd, args)
                return self.cur
            except Exception as e:
                print(e)
                if self.retry <= 0:
                    raise
                self.retry -= 1
            finally:
                self.close()

    def close(self):
        if self.cur:
            self.cur.close()
            self.cur = None
        if self.conn:
            self.conn.close()
            self.conn = None


if __name__ == '__main__':
    pass
