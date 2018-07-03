from selenium import webdriver
from scrapy.selector import Selector

broswer=webdriver.Chrome(executable_path='F:\区块链资料\chromedriver_win32\chromedriver.exe')

# broswer.get('https://k.autohome.com.cn/detail/view_01bz95vp0d64w30e9h70sg0000.html?st=1&piap=0|3197|0|0|1|0|0|0|0|0|1#pvareaid=21121')
broswer.get('https://k.m.autohome.com.cn/3901')
# t_selector=Selector(text=broswer.page_source)
# a=t_selector.css('#maodian > div > div > div.mouth-cont.js-koubeidataitembox > div:nth-child(9) > div > div.mouthcon-cont-right.commentParentBox > div.mouth-main > div.mouth-remak > div.allcont.border-b-solid > a.btn.btn-small.fn-left::attr(href)').extract()

source=broswer.page_source
print(source)
broswer.quit()