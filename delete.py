import undetected_chromedriver as uc
import time
import os

def temizlik_baslat():
    profil_yolu = os.path.join(os.path.expanduser("~/Desktop"), "twitter_silici")
    
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profil_yolu}")

    print("--- twit ve rt silici ---")
    driver = uc.Chrome(options=options, use_subprocess=True)

    print("--- TWITTER GİRİŞİ ---")
    driver.get("https://twitter.com/login")

    print("\n" + "!"*40)
    print("1. X'E GİRİŞ YAP.")
    print("2. PROFİLİNE GİR VE TWEETLER SEKMESİNİ AÇ.")
    print("3. ENTER'A BAS.")
    print("!"*40 + "\n")
    input()

    print(">>> SİLME VE RT GERİ ALMA BAŞLIYOR. <<<")

    silinen_sayisi = 0
    rt_geri_alim = 0

    while True:
        try:
            islem_turu = driver.execute_script("""
                // 1. Yeşil RT butonu var mı? (Bu RT yaptığın anlamına gelir)
                let rtBtn = document.querySelector('[data-testid="unretweet"]');
                if (rtBtn) {
                    rtBtn.click();
                    return "RT_BULUNDU";
                }

                // 2. Üç nokta (Caret) var mı? (Bu kendi tweetin olabilir)
                let caret = document.querySelector('[data-testid="caret"]');
                if (caret) {
                    caret.click();
                    return "TWEET_BULUNDU";
                }

                return "YOK";
            """)

            if islem_turu == "RT_BULUNDU":
                time.sleep(0.5)
                rt_onay = driver.execute_script("""
                    let confirmItem = document.querySelector('[data-testid="unretweetConfirm"]');
                    if (confirmItem) {
                        confirmItem.click();
                        return true;
                    }
                    return false;
                """)
                
                if rt_onay:
                    rt_geri_alim += 1
                    print(f"[RT İPTAL: {rt_geri_alim}] Retweet çekildi.")
                    time.sleep(1)
                else:
                    driver.execute_script("document.body.click();")
            

            elif islem_turu == "TWEET_BULUNDU":
                time.sleep(0.5)
                
                sil_tiklandi = driver.execute_script("""
                    let items = document.querySelectorAll('div[role="menuitem"]');
                    let found = false;
                    for (let item of items) {
                        if (item.innerText.includes('Sil') || item.innerText.includes('Delete')) {
                            item.click();
                            found = true;
                            break;
                        }
                    }
                    return found;
                """)

                if sil_tiklandi:
                    time.sleep(0.5)
                    sil_onay = driver.execute_script("""
                        let confirmBtn = document.querySelector('[data-testid="confirmationSheetConfirm"]');
                        if (confirmBtn) {
                            confirmBtn.click();
                            return true;
                        }
                        return false;
                    """)
                    
                    if sil_onay:
                        silinen_sayisi += 1
                        print(f"[SİLİNEN: {silinen_sayisi}] Tweet silindi.")
                        time.sleep(1.5)
                    else:
                        driver.execute_script("document.body.click();")
                
                else:
                    print("Menüde 'Sil' yok, geçiliyor...")
                    driver.execute_script("document.body.click();")
                    driver.execute_script("window.scrollBy(0, 250);")
                    time.sleep(0.5)


            else:
                print("Twitler kontrol ediliyor, aşağı kaydırılıyor.")
                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(2)

        except Exception as e:
            print("Hata!")
            time.sleep(1)

if __name__ == "__main__":
    temizlik_baslat()