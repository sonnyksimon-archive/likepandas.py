from selenium import webdriver
import time, random

def wait(): time.sleep(2)
def randwait(): time.sleep(random.randint(2,4))
def xwait(): time.sleep((random.randint(1, 7) / 30))

class Bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('./chromedriver')
        self.comments = ['Nice', 'Great capture.', 'Love it.']
    
    def scroll(self): 
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def close(self): 
        self.driver.close()
    
    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        wait()
        elem = driver.find_element_by_name('username')
        elem.send_keys(self.username)
        elem = driver.find_element_by_name('password')
        elem.send_keys(self.password)
        wait()
        elem.submit()
        wait()
        driver.get("https://www.instagram.com")
    
    def findlinks(self,links):
        for x in range(1,3):
            for y in range(1,3):
                curlink = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[' + str(x) + ']/div[' + str(y) + ']/a')
                links.add(curlink.get_attribute('href'))
    
    def getlinks(self, hashtag, scrolls):
        self.driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        wait()
        links = set()
        for i in range(scrolls):
            try:
                self.scroll()
                wait()
                self.findlinks(links)
            except: 
                continue
        return links
    
    def like(self, link):
        wait()
        self.driver.get(link)
        self.scroll()
        try:
            randwait()
            like = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button')
            like.click()
            randwait()
        except Exception as e:
            print(e)
            wait()
    
    def comment(self,text):
        try:
            btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[2]/button/span')
            btn.click()
        except: pass
        
        try:
            commentbox = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/textarea')
            commentbox.send_keys('')
            commentbox.clear()
            for letter in text:
                commentbox.send_keys(letter)
                xwait()
            return commentbox
        except Exception as e:
            print(e)
            return False
    
    def commentpost(self,text):
        randwait()
        commentbox=  self.comment(text)
        commentbox.submit()
        commentbox.send_keys(Keys.ENTER)
        randwait()
    
    def likecomment(self, links):
        for link in links:
            try:
                self.like(link)
                self.commentpost(random.choices(self.comments))
            except: continue

def likepandas(igname, igpass):
    ig = Bot(igname, igpass)
    ig.login()
    links = ig.getlinks('pandas',1)
    ig.likecomment(links)
    wait()
    ig.close()
    
if __name__ == '__main__':
    likepandas('your username','your password')
