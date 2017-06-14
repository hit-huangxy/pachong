# -*- coding: utf-8 -*-
import requests  # requests作为我们的html客户端
from pyquery import PyQuery as Pq  # pyquery来操作dom

class SegmentfaultQuestionSpider(object):
    
    def __init__(self,segmentfault_id):  # 参数为在segmentfault上的id
	self.url = 'http://segmentfault.com/q/{0}'.format(segmentfault_id)
	self._dom = None  # 弄个这个来缓存获取到的html内容，一个蜘蛛应该之访问一次
    
    @property
    def dom(self):
	if not self._dom:  # 获取html内容
	    document = requests.get(self.url)
	    document.encoding = 'utf-8'
	    self._dom = Pq(document.text)
	return self._dom
    
    @property
    def title(self): # 让方法可以通过s.title的方式访问 可以少打对括号
	return self.dom('h1#questionTitle').text()  # 关于选择器可以参考css selector或者jquery selector, 它们在pyquery下几乎都可以使用
    
    @property
    def content(self):  # 直接获取html 胆子就是大 以后再来过滤
	return self.dom('.divquestion.fmt').html()

    @property
    def answers(self):
	return list(answer.html() for answer in self.dom('.answer.fmt').items())  # 记住，Pq实例的items方法是很有用的

    @property
    def  tags(self):
	return self.dom('ul.taglist--inline > li').text().split()  # 获取tags，这里直接用text方法，再切分就行了。一般只要是文字内容，而且文字内容自己没有空格,逗号等，都可以这样弄，省事。
