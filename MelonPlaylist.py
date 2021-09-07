#-*-coding: utf-8-*-

from selenium import webdriver
import chromedriver_autoinstaller
import time

chromedriver_autoinstaller.install()

class Melon:
    title_xpath = '//*[@id="frm"]/div/table/tbody/tr/td[3]/div/div/a[2]'
    artist_xpath = '//*[@id="artistName"]'
    nav_script = ['javascript:pageObj.sendPage(', ');']

    def __init__(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        self.driver.get(url)
        dummy = self.driver.find_element_by_xpath('//*[@id="pageObjNavgation"]/div/a[4]')
        endpage = dummy.get_attribute("href")
        self.endpage = (int(endpage[29:-3])-1)//50
        
    def fetch_all(self):
        result = []

        for i in range(1, self.endpage+1):
            artists = []
            titles = []

            for j in self.driver.find_elements_by_xpath(Melon.title_xpath):
                titles.append(j.text)

            for j in self.driver.find_elements_by_xpath(Melon.artist_xpath):
                temp = []
                for k in j.find_elements_by_tag_name('a'):
                    temp.append(k.text)

                artists.append(temp)

            result += list(zip(titles, artists))

            self.driver.execute_script(Melon.nav_script[0]+str(50 * i + 1)+Melon.nav_script[1])
            time.sleep(1)
        return result

    def open_playlist(self, url):
        self.driver.get(url)
        time.sleep(1)
        dummy = self.driver.find_element_by_xpath('//*[@id="pageObjNavgation"]/div/a[4]')
        endpage = dummy.get_attribute("href")
        self.endpage = (int(endpage[29:-3])-1)//50

    def get_playlist_title(self):
        return self.driver.find_element_by_xpath('//*[@id="conts"]/div[1]/div/div[2]/dl/dt/span').text
        


        
    def __del__(self):
        self.driver.quit()


def main():
    lists = []
    temp = ""
    print("추출할 멜론 플레이리스트의 링크를 입력하세요.\n링크를 모두 입력했다면 'done'을 입력하세요.")
    while not temp == "done":
        temp = input('> ')
        lists.append(temp)

    lists.remove('done')

    print("\n[*] 추출을 시작합니다.\n추출 작업에는 시간이 다소 소요될 수 있습니다.")

    melon = Melon(lists[0])
    with open(f'{melon.get_playlist_title()}.txt', 'w', encoding='UTF-8') as f:
        for i in melon.fetch_all():
            title, artist = i
            if artist == []: artist = ["Various Artists"] 
            f.write(title+' - ')
            for j in artist[:-1]:
                f.write(f"{j}, ")
            f.write(artist[-1]+'\n')

    for links in lists[1:]:
        melon.open_playlist(links)
        with open(f'{melon.get_playlist_title()}.txt', 'w', encoding='UTF-8') as f:
            for i in melon.fetch_all():
                title, artist = i
                if artist == []: artist = ["Various Artists"] 
                f.write(title+' - ')
                for j in artist[:-1]:
                    f.write(f"{j}, ")
                f.write(artist[-1]+'\n')

    print("\n[+] 작업을 완료했습니다.")
    input("엔터키를 눌러 프로그램을 종료하십시오.")

    return

if __name__ == "__main__":
    main()