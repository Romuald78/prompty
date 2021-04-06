import arcade


class TextReader():

    # speed is number of pixels/sec
    def __init__(self, filePath, fontSize):
        self._speed  = 0
        self._rows   = []
        self._yRef   = 980
        self._size   = fontSize
        square = arcade.make_soft_square_texture(50,(255,255,0))
        self._cursor = arcade.Sprite()
        self._cursor.textures.append(square)
        self._cursor.set_texture(0)
        self._cursor.center_x = 1920-25
        # Create sprites
        self._addText(filePath)


    def _splitText(self,txt,isTitle=False):
        words = txt.split(' ')
        out = []
        tmpStr = ""
        while len(words)>0:
            word  = words[0]
            words = words[1:]
            if len(tmpStr)+len(word) <= 30:
                tmpStr += ' '+ word
            else:
                if isTitle:
                    tmpStr = "<title>"+tmpStr
                out.append(tmpStr)
                tmpStr = ' ' + word
        if tmpStr != "":
            if isTitle:
                tmpStr = "<title>" + tmpStr
            out.append(tmpStr)
        return out

    def _cutText(self,txt):
        out = []
        # Cut the text according to \n
        textLines = txt.split('\n')
        for textLine in textLines:
            textLine = textLine.replace("\n", "")
            textLine = textLine.replace("\r", "")
            textLine = textLine.replace("\t", " ")
            while "  " in textLine:
                textLine = textLine.replace("  ", " ")

            isTitle = False
            if "<title>" in textLine.lower():
                isTitle = True
                textLine = textLine.replace("<title>", "")
                textLine = textLine.replace("<TITLE>", "")
            # Get rows from text
            splittedLines = self._splitText(textLine, isTitle)
            # add them into the output
            for s in splittedLines:
                out.append(s)
        return out

    def _addText(self, filePath):
        fp = open(filePath)
        rl = fp.readlines()
        fp.close()
        txt = "".join(rl)
        # First cut text into several rows
        rows2Add = self._cutText(txt)
        for row in rows2Add:
            color = (255,255,255)
            if "<title>" in row.lower():
                color = (255,255,0)
                row = row.replace("<title>","")
            text = arcade.draw_text(row,0,0,color,self._size,align="left")
            spr = arcade.AnimatedTimeSprite()
            spr.append_texture(text.texture)
            spr.set_texture(0)
            self._rows.append(spr)

    def update(self,deltaTime):
        # make the ref goes upward
        self._yRef += deltaTime*self._speed
        # Set sprite positions
        for i in range(len(self._rows)):
            self._rows[i].center_x = self._rows[i].width//2
            self._rows[i].center_y = self._yRef - i*self._size
        # cursor
        self._cursor.center_y = (1.0-self.getProgress())*(1080-50)+25

    def draw(self):
        self._cursor.draw()
        for texture in self._rows:
            texture.draw()
        arcade.draw_line(0,540,1920,540,(255,0,0),2)


    def reset(self):
        self._yRef = 1080

    def getSpeed(self):
        return self._speed

    def setSpeed(self,speed):
        self._speed = speed

    def getSize(self):
        return self._size

    def getProgress(self):
        total   = (self._size*len(self._rows)) - 980
        total   = max(0,total)
        if total == 0:
            return 1.0
        else:
            current = self._yRef-980
            return current/total

