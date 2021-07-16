from time import sleep
import kinopoisk

def run():
    kinopoisk.request()

while True:
    sleep(86400)
    run()
