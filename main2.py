import src.engine.engine.scraper 



if __name__ == "__main__":
    testing_url = "https://5278.cc/forum.php?mod=viewthread&tid=1711755&extra=page%3D1"
    scraper = src.engine.engine.scraper.Scraper()
    scraper.url = testing_url
    scraper.run()