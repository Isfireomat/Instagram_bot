import transmutation
import sys
import multiprocessing
from multiprocessing import Queue
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
from main_form import Ui_MainWindow
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import random
from selenium.webdriver.common.by import By
import instaloader

def authorize(driver,login,password):
    driver.get('https://www.instagram.com')
    time.sleep(5)
    driver.find_element(By.NAME, "username").send_keys(login)
    driver.find_element(By.NAME,"password").send_keys(password)
    time.sleep(2)
    driver.execute_script("document.getElementsByClassName(' _acan _acap _acas _aj1- _ap30')[0].click()")
    time.sleep(10)
    driver.execute_script("document.getElementsByClassName(' _acan _acap _acas _aj1- _ap30')[0].click()")
    time.sleep(10)
    driver.execute_script("document.getElementsByClassName('_a9-- _ap36 _a9_1')[0].click()")

def get_followers_with_stories(login,password,user_name,queue,queue_2):
        try:
            loader = instaloader.Instaloader()
            loader.login(login, password)
        except Exception as E:
            queue_2.put("Первая авторизация провалена")
            queue_2.put(str(E))
            return
        queue_2.put("Первая авторизация успешна")
        profile = instaloader.Profile.from_username(loader.context, user_name)
        number=0
        try:
            for follower in profile.get_followers():
                queue_2.put(follower.username)
                try:
                    number+=1
                    if number%15==0: time.sleep(random.randint(10,50))
                    if follower.has_viewable_story:
                        queue.put(follower.username)
                except Exception as E :queue_2.put(str(E))
        except Exception as E :queue_2.put(str(E))
        queue_2.put(" ")
        queue_2.put("Получение завершено")
        queue_2.put(" ")
        
def view_all_stories(followers,login,password,queue,queue_2):
        
    if len(followers)==0: 
        queue_2.put("Пользователей нет")
        return
    
    try:
        service = webdriver.ChromeService(executable_path = "chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        queue_2.put("Драйвер успешно загружен")
    except: queue_2.put("Проблема с драйвером")
    
    try:
        authorize(driver,login,password)
        queue_2.put("Вторая авторизация прошла успешно")
    except: 
        queue_2.put("Вторая авторизация провалилась")
        return
    
    people_stories=0
    all_stories_count=0
    script = """
            const svgElements = document.querySelectorAll('svg');
            let clicked = false;
            svgElements.forEach(svg => {
            const titleElement = svg.querySelector('title');
            if (titleElement && titleElement.textContent.trim() === 'Next') {
                const clickableParent = svg.closest('div[role="button"]');
                if (clickableParent) {
                clickableParent.click();
                clicked = true;
                return;
                }
            }
            });
            return clicked;
            """
    for follower in followers:
        try:
            if people_stories%15==0: time.sleep(random.randint(10,50))
            driver.get(f'https://www.instagram.com/stories/{follower}/')
            time.sleep(random.randint(1,3))
            driver.execute_script("document.getElementsByClassName('x1i10hfl xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1k74hu9 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x9f619 x1ypdohk x78zum5 x1f6kntn xwhw2v2 xl56j7k x17ydfre x1n2onr6 x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xn3w4p2 x5ib6vp xc73u3c xc58f59 xm71usk x19hv4p6 xfn85t x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x178xt8z xm81vs4 xso031l xy80clv x9bdzbf')[0].click()")
            while True:
                time.sleep(random.randint(1,2))    
                all_stories_count+=1    
                if not driver.execute_script(script): break
            people_stories+=1
            queue_2.put(f"Просмотрен {follower}")
        except: pass

    queue_2.put(" ")
    queue_2.put(f"Всего людей просмотрено: {people_stories}")
    queue_2.put(f"Всего историй просмотрено: {all_stories_count}")    

class main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        self.setupUi(self)
        self.queue = Queue()
        self.queue_2 = Queue()
        self.pushButton.clicked.connect(self.get_followers_with_stories_main)
        self.pushButton_2.clicked.connect(self.view_all_stories_main)
        self.pushButton_3.clicked.connect(self.add_user_name)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_callback)
        self.timer.start(500)
    
    def add_user_name(self):
        if len(self.lineEdit_4.text())!=0:
            self.queue.put(self.lineEdit_4.text())
        self.lineEdit_4.clear()
        
    def timer_callback(self):
        if not self.queue.empty():
            self.listWidget.addItem(self.queue.get())
            self.listWidget.scrollToBottom()

        if not self.queue_2.empty():
            self.listWidget_2.addItem(self.queue_2.get())
            self.listWidget_2.scrollToBottom()
        
    def get_followers_with_stories_main(self):
        self.listWidget.clear()
        login=self.lineEdit.text()
        password=self.lineEdit_2.text()
        user_name=self.lineEdit_3.text()
        process = multiprocessing.Process(target=get_followers_with_stories, args=(login, password, user_name,self.queue,self.queue_2))
        process.start()
        
    def view_all_stories_main(self):
        
        followers=[]
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            followers.append(item.text())
            
        login=self.lineEdit.text()
        password=self.lineEdit_2.text()
            
        process = multiprocessing.Process(target=view_all_stories, args=(followers,login, password,self.queue,self.queue_2))
        process.start()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    player = main()
    player.show()
    sys.exit(app.exec())
