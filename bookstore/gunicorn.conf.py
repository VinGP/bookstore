import multiprocessing
import os

workers = multiprocessing.cpu_count() * 2 + 1

threads = 25
loglevel = "debug"

try:
    os.makedirs("./log/gunicorn/")
except FileExistsError:
    pass

accesslog = "./log/gunicorn/access.log"
acceslogformat = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlogfile = "./log/gunicorn/error.log"
