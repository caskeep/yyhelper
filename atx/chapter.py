# -*- coding: utf-8 -*-

import atx
import time
import getopt
import sys

class YysHelper():
    def __init__(self):
        self.d = atx.connect()
        self.d.image_path = ['.', 'assets']

    def chapter(self, level):
        """
        章节，level 表示第几章
        """
        while True:
            chapterImage = "chapter%s.1920x1080.png" % level

            ret = self.clickImage(chapterImage)

            if ret:
                self.sleep(2)

            ret = self.clickImage("explore.1920x1080.png")

            if ret:
                self.sleep(8)

            ret = self.clickImage("lock.1920x1080.png", time=5)

            fightedWithLeader = False

            while not fightedWithLeader:
                swipeCount = 0
                while swipeCount < 3:
                    ret = self.clickImage("sword.1920x1080.png")
                    if not ret:
                        ret = self.clickImageNoWait("leader_sword.1920x1080.png")
                        fightedWithLeader = ret

                    if ret:
                        self.sleep(15)
                        ret = self.checkImageExists("friend.1920x1080.png")
                        if ret:
                            break
                    else:
                        self.swipe(0.78, 0.25)
                        swipeCount += 1
                        continue

                if swipeCount >= 3:
                    break

                count = 0
                while True:
                    ret = self.clickImage("click_to_continue.1920x1080.png")
                    if not ret:
                        if count >= 3:
                            self.sleep(7)
                            break
                    else:
                        count += 1

            if fightedWithLeader:
                while True:
                    ret = self.clickImage("fresh.1920x1080.png")
                    if ret:
                        self.clickImage("back.1920x1080.png")
                    else:
                        self.sleep(7)
                        break
            else:
                ret = self.clickImage("back.1920x1080.png")

                if ret:
                    self.sleep(2)
                    ret = self.clickImage("chapter_quit_confirm.1920x1080.png")
                    if ret:
                        self.sleep(10)

    def clickImage(self, image, time=10):
        try:
            self.d.click_image(image, timeout=time)
            return True
        except atx.ImageNotFoundError:
            print('%s button not found' % image)
            return False

    def clickImageNoWait(self, image):
        ret = self.d.click_nowait(image)
        if ret is not None:
            return True
        else:
            print('%s button not found' % image)
            return False

    def checkImageExists(self, image):
        ret = self.d.exists("friend.1920x1080.png")
        if ret is not None:
            print('%s exists' % image)
            return True
        else:
            print('%s not exists' % image)
            return False

    def swipe(self, startX, endX):
        '''
        入参为百分比
        '''
        x1 = self.d.display.height * startX
        y1 = self.d.display.width * 0.5
        x2 = self.d.display.height * endX
        y2 = self.d.display.width * 0.5
        self.d.swipe(x1, y1, x2, y2, steps=20)

    def sleep(self, seconds, msg=""):
        if msg is not None and msg != "":
            print("sleep for " + msg)
        print("sleep : " + str(seconds))
        time.sleep(seconds)

def usage():
    print("""
          usage: python chapter.py -c <num>

          Augument `num` is the chapter count you want to fight.

          Available:

          -c num | --chapter=num    Fight for chapter num
          """)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:", ["chapter="])
    except getopt.GetoptError as err:
        opts = []

    if len(opts) == 0:
        usage()
        opts = [('-c', '13')]

    yyshelper = YysHelper()

    for o, a in opts:
        if o in ("-c", "--chapter"):
            print("start fight for chapters %s" % a)
            yyshelper.chapter(a)
        break

if __name__ == '__main__':
    main()