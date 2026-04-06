import scraper
'''
論壇:https://5278.cc/
功能:爬影片

'''


if __name__ == "__main__":
    while True:
        url = input("\n請輸入網址 (或輸入 'q' 離開): ")
        
        if url.lower() == 'q':
            print("程式結束。")
            break
            
        if not url.strip():
            print("網址不能為空，請重新輸入。")
            continue     
        try:
            # 執行你的爬蟲邏輯
            scraper.GetData(url)
            print("-" * 30)
            print("該網址處理完成！")
            
        except Exception as e:
            # 這樣萬一其中一個網址報錯，迴圈才不會直接崩潰退出
            print(f"發生錯誤: {e}")
            print("請檢查網址是否正確，或網站是否阻擋了連線。")

    input("按 Enter 鍵完全退出視窗...")