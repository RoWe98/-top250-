# 获取豆瓣top250的 标题 副标题 经典名句 评分 网址
# 存入.txt文件中


# 导入第三方库
import lxml.html
# from lxml import html
import requests


# 获取目标网站

# 获取目标网页url 规律 ： 页数-1 * 25 用5的倍数替换

doubanUrl = 'https://movie.douban.com/top250?start={}&filter='

# 解析目标网页
# 定义一个函数 目的：获取网页中我们所需要的数据
def getSource(url):
    # 获取目标网页
    response = requests.get(url)
    # 修改编码
    response.encoding = 'utf-8'
    return response.content
    
# 定义一个函数 目的：获取每一个电影的相关信息
def getEveryItem(source):
    
    selector = lxml.html.document_fromstring(source)

    # 获取所有info
    movieItemList = selector.xpath('//div[@class="info"]')

    # 定义一个列表 目的：展示信息

    movieList = []
    for eachMovie in movieItemList:
        
        movieDict = {}
        # 展示的结果--> [movieDict1,movieDict2]

        title = eachMovie.xpath('div[@class="hd"]/a/span[@class="title"]/text()')
        #print(title)
        #otherTitle = eachMovie.xpath('div[@class="hd"]/a/span[@class="other"]/text()')
        link = eachMovie.xpath('div[@class="hd"]/a/@href')[0]
        star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]
        quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')
        # player = eachMovie.xpath('div[@class="bd"]/p[@class=""]/text()"]')
        player = eachMovie.xpath('div[@class="bd"]/p[@class=""]/text()')
        
        # 保存到字典
        #movieDict['title'] = ''.join(title + otherTitle)
        movieDict['title'] = ''.join(title)
        movieDict['url'] = link
        movieDict['star'] = star
        movieDict['quote'] = quote
        movieDict['player'] = player
        # print(movieDict)
        movieList.append(movieDict)
    
    return movieList
'''
# 下载目标网页数据
def writeData(movieList):
    with open('./DoubanMovie.csv','w',encoding='utf-8',newline='') as f:
        
        writer = csv.DictWriter(f,fieldnames=['title','star','quote','url'])
        writer.writeheader()
        for each in movieList:
            writer.writerow(each)
'''
def writeData(movieList):
    with open('./DoubanMovie.txt','w',encoding='utf-8',newline='') as f:
        #print(source)
        i = 0
        for data in movieList:
            for values in movieList[i].values():

                values_title = movieList[i]['title']
                values_url = movieList[i]['url']
                values_star = movieList[i]['star']
                values_quote = movieList[i]['quote']
                values_player = movieList[i]['player']
    

                # value = '片名: ' + values_title + '\n' + '评分: ' + values_star + '\n' + '名句：' + values_quote + '\n' + '网址: ' + values_url
                value = str(i+1) + '.片名: ' + values_title + '\n' + '  评分: ' + values_star + '\n' + '  名句: ' + str(values_quote[0]) + '\n' + '  网址: ' + values_url + str(values_player[0])
            f.write(value+'\n'+'\n')
            i+=1
            
        


if __name__ == '__main__':

    movieList = []

    for i in range(10):
        
        pageLink = doubanUrl.format(i*25)

        print(pageLink)

        # 获取资源
        source = getSource(pageLink)

        # 信息
        movieList += getEveryItem(source)

        #print(movieList[:10])

        writeData(movieList)
