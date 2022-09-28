import string


class PlayerTag():

    _order = list(["0","2","8","9","C","G","J","L","P","Q","R","U","V","Y"])

    def __init__(self, tag:string):

        if tag=="":
            self.tag=tag
        else:
            if len(tag)!=8:
                raise ValueError("length of tag is not equal 8")
            for c in tag:
                if not c in PlayerTag._order:
                    raise ValueError("Illegal charakter in tag")
            self.tag = list(tag)

        
    

    def _increment(self):
        if self.tag=="":
            self.tag=list("00000000")
        else:
            if self.tag == list("YYYYYYYY"):
                raise Exception("done")
            for i in range(7,-1,-1):
                if self.tag[i]=="Y":
                    self.tag[i]="0"
                else:
                    nextindex = PlayerTag._order.index(self.tag[i])+1
                    self.tag[i]=PlayerTag._order[nextindex]
                    break

    def _incrementBlock(self):
        if self.tag[0:6] == list("YYYYYY"):
            raise Exception("done")
        for i in range(5,-1,-1):
            if self.tag[i]=="Y":
                self.tag[i]="0"
            else:
                nextindex = PlayerTag._order.index(self.tag[i])+1
                self.tag[i]=PlayerTag._order[nextindex]
                break

    def getNext(self):
        try: 
            self._increment()
        except:
            pass
        return self     

    def __str__(self):
        return "".join(self.tag)




#for i in range(1000):
 #   print(tag)
 #   tag._incrementBlock()

