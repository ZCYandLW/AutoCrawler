from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 将项目路径加入系统path去

execute(['scrapy','crawl','carComment'])  # 启动spider
