import lxml.html
import requests

class Douban(object):
    def __init__(self, doubanUrl):
        
        self.doubanUrl = doubanUrl

class getInfo(Douban):
    def __init__(self, doubanUrl):
        super(getInfo,self).__init__(doubanUrl)
    
    def getSource(self,doubanUrl):
        
        response = requests.get(self.doubanUrl)

        response.encoding = 'utf-8'

        return response.content

    def getEveryItem(self,source):
        
        selector = lxml.html.document_fromstring(source)

        movieItemList = selector.xpath('//div[@class="info"]')

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
            #player = eachMovie.xpath('div[@class="bd"]/p[@class=""]/text()')
            
            # 保存到字典
            #movieDict['title'] = ''.join(title + otherTitle)
            movieDict['title'] = ''.join(title)
            movieDict['url'] = link
            movieDict['star'] = star
            movieDict['quote'] = quote
            # movieDict['player'] = player
            # print(movieDict)
            movieList.append(movieDict)
        
        return movieList

    def writeData(self,movieList):
        with open('./DoubanMovie.txt','w',encoding='utf-8',newline='') as f:
            #print(source)
            i = 0
            for data in movieList:
                for values in movieList[i].values():

                    values_title = movieList[i]['title']
                    values_url = movieList[i]['url']
                    values_star = movieList[i]['star']
                    values_quote = movieList[i]['quote']
                    #values_player = movieList[i]['player']
        

                    # value = '片名: ' + values_title + '\n' + '评分: ' + values_star + '\n' + '名句：' + values_quote + '\n' + '网址: ' + values_url
                    value = str(i+1) + '.片名: ' + values_title + '\n' + '  评分: ' + values_star + '\n' + '  名句: ' + str(values_quote[0]) + '\n' + '  网址: ' + values_url # + str(values_player[0])
                f.write(value+'\n'+'\n')
                i+=1

    
if __name__ == '__main__':
        
    movieList = []
    NewDoubanUrl = 'https://movie.douban.com/top250?start={}&filter='
    data = getInfo(NewDoubanUrl)
    for i in range(10):
        pageLink = NewDoubanUrl.format(i*25)

        print(pageLink)

        source = data.getSource(pageLink)

        movieList += data.getEveryItem(source)

        data.writeData(movieList)



