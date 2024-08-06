from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

print("""
Bu program (TweetScraper) çok basit scriptler ile ve ilk sürümü olduğu için bazı hatalar mevcuttur.
TweetScraper'ı geliştirmek, öneri ve fikirler için iletişime geçin: muhammetemirhansumer@gmail.com
                                    "https://github.com/memirhan"
""")

username = "" # Kendi Twitter (X) kullanıcı adını gir
password = "" # Kendi Twitter (X) şifreni gir

if username == "" or password == "":
    print("Twitter kullanıcı bilgilerinizi kod içerisinde düzenleyin")
    quit()

user = input("Kullanıcı adını giriniz: ")
userPath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[3]/div/div/button'
ileriButon = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]'
loginButton = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button'
tweetXPath = '//div[@data-testid="tweetText"]'
dateXPath = '//time'
imgOrEmojiPath = './/img'
    
cekilenTumTweetler = []
cekilenTumTweetlerTarih = []
cekilecekTweetSayisi = int(input("Kaç tane tweet çeksin: "))
tweetTextSet = set() # tekrarlanan tweetleri önlemek için

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)

url = "https://twitter.com/login"
driver.get(url)

wait = WebDriverWait(driver, 20)

username_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[autocomplete="username"]')))
username_input.send_keys(username)

nextButton = wait.until(EC.element_to_be_clickable((By.XPATH, ileriButon)))
nextButton.click()

password_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[autocomplete="current-password"]')))
password_input.send_keys(password)

loginButon = wait.until(EC.element_to_be_clickable((By.XPATH, loginButton)))
loginButon.click()

searchInput = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[autocomplete="off"]')))
searchInput.send_keys(user)
searchInput.send_keys(u'\ue007')  # Enter tuşunun Unicode kodu

kullanıcıSec = wait.until(EC.element_to_be_clickable((By.XPATH, userPath)))
kullanıcıSec.click()

print("Giriş yapıldı ve kullanıcı arandı. Tweetleri çekmek için bekleniyor...")
time.sleep(2)

def scrollHareketi(driver, durmaZamani = 2, scrollPiksel = 100):
    sonYukseklik = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, arguments[0]);", scrollPiksel) # dikeyde scrollPiksel kadar ilerle dedik
        time.sleep(durmaZamani)
        yeniYukseklik = driver.execute_script("return document.body.scrollHeight") # yeni yukseklik scroll bar kaydırıldıktan sonraki yükseklik

        if yeniYukseklik == sonYukseklik:
            break

        sonYukseklik = yeniYukseklik

tweetDurumu = 0

while len(cekilenTumTweetler) < cekilecekTweetSayisi:
    tumTweetler = driver.find_elements(By.XPATH, tweetXPath)
    for herBirTweet in tumTweetler:
        tweetText = herBirTweet.text.strip().replace('\n','') # Her bir tweetin text ini alıyoruz

        if tweetText not in tweetTextSet: # eğer o tweet yoksa ekle
            try: 
                tweetDate = herBirTweet.find_element(By.XPATH, dateXPath).get_attribute('datetime')
                tweetDate = datetime.fromisoformat(tweetDate.replace('Z', '+00:00'))
                tweetDate = tweetDate.strftime('%d-%m-%Y')
                cekilenTumTweetlerTarih.append(tweetDate)

            except Exception as e:
                cekilenTumTweetlerTarih.append('Tarih bilgisi alınamadı')

            if herBirTweet.find_elements(By.XPATH, imgOrEmojiPath): # eğer sadece resim veya emoji varsa
                tweetText += "Resim veya Emoji var"

            tweetTextSet.add(tweetText)
            cekilenTumTweetler.append(tweetText)
            tweetDurumu += 1
            print("{} tane tweet çekildi".format(tweetDurumu))


            if len(cekilenTumTweetler) == cekilecekTweetSayisi: # Bu sayede cekilecekTweetSayisindan fazla tweet çekmesini engellemiş oluyourz
                break

    scrollHareketi(driver, durmaZamani = 2, scrollPiksel = 100) # Yine kaydır dedik

with open("CekilenTweetler.txt", "w", encoding="utf-8") as file:
    for idx, (tweet, tarih) in enumerate(zip(cekilenTumTweetler, cekilenTumTweetlerTarih), 1):
        file.write("{}: {} - {}\n".format(idx, tweet, tarih))

print(f"{len(cekilenTumTweetler)} tweet başarıyla kaydedildi.")
input("Tarayıcıyı kapatmak için Enter'a basın...")

driver.quit()