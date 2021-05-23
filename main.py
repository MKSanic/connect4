import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui as pyag
import threading
import keyboard as kb
import time

print("imports complete")
ys = []

site = 'https://connect4.gamesolver.org/'
blank = (37, 34, 51)
red = (244, 55, 46)
yellow = (207, 169, 23)
blue = (22, 135, 239)
blue_pos = (980, 120)
pos = [
    [(700, 700), (700, 620), (700, 550), (700, 470), (700, 390), (700, 320)],
    [(780, 700), (780, 620), (780, 550), (780, 470), (780, 390), (780, 320)],
    [(850, 700), (850, 620), (850, 550), (850, 470), (850, 390), (850, 320)],
    [(930, 700), (930, 620), (930, 550), (930, 470), (930, 390), (930, 320)],
    [(1000, 700), (1000, 620), (1000, 550), (1000, 470), (1000, 390), (1000, 320)],
    [(1080, 700), (1080, 620), (1080, 550), (1080, 470), (1080, 390), (1080, 320)],
    [(1160, 700), (1160, 620), (1160, 550), (1160, 470), (1160, 390), (1160, 320)]
]

coptions = Options()
coptions.headless = True
browser = webdriver.Chrome(options=coptions)


def scan():
    yellows = []
    for collumn in pos:
        for v in collumn:
            p = pyag.pixel(v[0], v[1])
            if p == yellow:
                yellows.append(v)
    return yellows


def turn():
    if pyag.pixel(blue_pos[0], blue_pos[1]) == blue:
        return 0
    else:
        return 1


def bm(s):
    pyag.click(690, 1000)
    time.sleep(0.2)
    pyag.typewrite(s + "\n", 0.01)
    pyag.click(740, 910)


def update(where):
    i = -1
    c = 0
    final = 0
    for v, collumn in enumerate(pos):
        try:
            i = collumn.index(where)
            c = v
            break
        except:
            pass
    if i != -1:
        final = c * 6 + i
    browser.find_elements_by_xpath('//*[@id="board"]/*[@class="board"]')[final].click()
    while browser.find_element_by_xpath('//*[@id="solution_header"]').text == 'computing solution...':
        pass
    time.sleep(0.5)
    sols = browser.find_elements_by_xpath('//*[@id="solution"]/*')
    vals = []
    for v in sols:
        try:
            vals.append(int(v.text))
        except:
            vals.append(-30)
    best = max(vals)
    for i, v in enumerate(sols):
        try:
            if int(v.text) == best:
                return i
        except:
            pass


class main:
    kill = False

    def __init__(self):
        while not self.kill:
            self.real()

    def real(self):
        browser.get(site)
        browser.find_element_by_xpath('//*[@id="hide_solution_link"]').click()  # Clicks on show solutions
        ys = []
        browser.find_element_by_xpath('//*[@id="new"]').click()
        time.sleep(2)
        pyag.click(pos[3][0])
        update(pos[3][0])
        while True:
            while turn() == 1:  # their turn, wait
                if self.kill or pyag.pixel(700, 370) == (255, 255, 255):
                    pyag.click(800, 700)
                    time.sleep(10)
                    pyag.click(680, 80)
                    time.sleep(5)
                    pyag.click(800, 1000)
                    time.sleep(1)
                    pyag.click(925, 785)
                    time.sleep(2)
                    return
            time.sleep(1)
            yellows = scan()  # my turn, scan
            their_move = 0
            for v in yellows:
                if v not in ys:
                    ys.append(v)
                    their_move = v
                    break
            choice = update(their_move)
            bm("I will win in at most " + browser.find_element_by_xpath('//*[@id="solution_header"]').text.split(" in ")[1])
            pyag.click(pos[choice][0])
            update(pos[choice][0])
            while turn() == 0:
                pass

    def killer(self):
        def main():
            while True:
                if keyboard.is_pressed('-'):
                    self.kill = True
                    return

        threading.Thread(target=main).start()


time.sleep(5)
main()
