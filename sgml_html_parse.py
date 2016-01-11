from sgmllib import SGMLParser  
  
class ListName(SGMLParser):  
  
    def reset(self):  
        #变量标示是否是标签a,或使用self.is_a=True  
        self.is_a=""  
        self.name=[]  
        #继承父类reset方法  
        SGMLParser.reset(self)  
  
    def start_a(self,attrs):  
        #如果是标签a，则设置is_a=1  
        self.is_a=1  
  
    def end_a(self):  
        self.is_a=""  
  
    def handle_data(self,data):  
        #如果是标签a的数据，则追加  
        if self.is_a:  
            self.name.append(data)  
  
if __name__ == '__main__':  
    urls=''''' 
    <tr> 
<td height="207" colspan="2" align="left" valign="top" class="normal"> 
<p>Damien Rice - 《0》 </p> 
<a href="http://galeki.xy568.net/music/Delicate.mp3">1. Delicate</a><br /> 
<a href="http://galeki.xy568.net/music/Volcano.mp3">2. Volcano</a><br /> 
<a href="http://galeki.xy568.net/music/The Blower's Daughter.mp3">3. The Blower's Daughter</a><br /> 
<a href="http://galeki.xy568.net/music/Cannonball.mp3">4. Cannonball </a><br /> 
<a href="http://galeki.xy568.net/music/Older Chests.mp3">5. Order Chests</a><br /> 
<a href="http://galeki.xy568.net/music/Amie.mp3">6. Amie</a><br /> 
<a href="http://galeki.xy568.net/music/Cheers Darlin'.mp3">7. Cheers Darling</a><br /> 
<a href="http://galeki.xy568.net/music/Cold Water.mp3">8. Cold water</a><br /> 
<a href="http://galeki.xy568.net/music/I Remember.mp3">9. I remember</a><br /> 
<a href="http://galeki.xy568.net/music/Eskimo.mp3">10. Eskimo</a></p> 
</td> 
</tr> 
    '''  
    listname=ListName()  
    listname.feed(urls)  
    #输出文本的列表结果  
    print listname.name  
    listname.close()
