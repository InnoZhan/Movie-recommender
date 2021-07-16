from time import sleep
import kinopoisk

def run():
    kinopoisk.request()

while True:
    sleep(2)
    run()
