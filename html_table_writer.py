# THIS IS A SIMPLE PROGRAM TO WRITE A HTML TABLE.

import os
from io import TextIOWrapper


def open_file(file,mode,encoding=None) -> TextIOWrapper: #A function to open a file.
    if encoding:
        fh = open(file,mode,encoding = encoding)
    else:
        fh = open(file,mode) #this ensures that file is optimised according to encoding of system if no encoding is provided
    return fh
   

class table: #A table object to store all the data
    def __init__(self,file,encoding=None,bg_color='white',align = 'left', text_color='black',border=0, border_color='black',headers=[]) -> None:
        self.file = file
        self.encoding = encoding
        self.bg_colour = bg_color
        self.align = align
        self.text_color = text_color
        self.border = border
        self.border_color = border_color
        self.headers = headers

    #A function to write a table.
    def write_table(self,data):
        fh = open_file(self.file,'w',encoding = self.encoding)

        #Create a html table.
        fh.write(f'''<table style="color: {self.text_color}; background: {self.bg_colour}; border: {self.border}px solid; border-color: {self.border_color};">\n''')

        #add headers to the table    
        if self.headers:
            fh.write('<thead>\n<tr>')
            for head in self.headers:
                fh.write(f'''<th style= "text-align: {self.align}; border: {self.border}px solid; border-color: {self.border_color}">{head}</th>''')
            fh.write('</tr>\n</thead>\n<tbody>\n')

        #iterate through each row and create table of it.
        for row in data:
            fh.write('<tr>')
            for value in row:
                fh.write(f'''<td style= "text-align: {self.align}; border: {self.border}px solid; border-color: {self.border_color}">{value}</td>''')
            fh.write('</tr>\n')

        fh.write('</tbody>\n</table>')
        fh.close()

    #A function to extend a previously created table.
    def extend_table(self,data):
        fh = open_file(self.file,'r+',self.encoding)

        ft = open_file('temp.txt','w',self.encoding) #Creating a temp file to store all the lines except ending tags.
        #Temp file is created just to remove ending tags from the previously stored data. 


        for line in fh: #copy previously created table into new file without ending tags.
            if line.strip() == '</tbody>' or line.strip() == '</table>': #skip the lines that contain these tags.
                continue
            ft.write(line)

        fh.truncate(0) #Emptying the previous file.
        ft.close()
        fh.close()

        #copy the table from temp file and remove temp file.
        fh = open_file(self.file,'w',self.encoding)
        ft = open_file('temp.txt','r',self.encoding)
        for line in ft:
            fh.write(line)
        ft.close()
        os.remove('temp.txt')

        #iterating through new data to extend the previous table.
        for row in data:
            fh.write('<tr>')
            for value in row:
                fh.write(f'''<td style= "text-align: {self.align}; border: {self.border}px solid; border-color: {self.border_color}">{value}</td>''')
            fh.write('</tr>\n')
        fh.write('</tbody>\n</table>')
        fh.close()