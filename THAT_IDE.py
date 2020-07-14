from tkinter import *
from tkinter.scrolledtext import ScrolledText as ST
from tkinter.filedialog import *
from tkinter.messagebox import *
from time import sleep, strftime
from random import choice
from tkinter import font
from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name as __get__

import os, subprocess

class main:
     def __init__(self, master, lexer):
          self.master=master;self.master.title("PyDE - Untitled")
          self.filename=None;self.lexer=lexer
          self.x, self.y=0 ,10
          self.ftsize=15
          self.end=""

          self.img = PhotoImage(file="C:/Users/shiven/Desktop/anime.png")
          self.__anime__ = self.img.subsample(3,3)

          self.mario1=PhotoImage(file="C:/Users/shiven/Desktop/C++/mariofinal1.png")
          self.mario2=PhotoImage(file="C:/Users/shiven/Desktop/C++/mariofinal2.png")

          self.mario1=self.mario1.subsample(2,2)


          self.types=[("All Files", "*.*"),("Text Files", "*.txt")]

          self.draw()
          self.text.bind("<Control-N>",self.newfile)
          self.text.bind("<Control-n>",self.newfile)
          self.text.bind("<Control-S>",self.savefile)
          self.text.bind("<Control-s>",self.savefile)
          self.text.bind("<Control-o>",self.openfile)
          self.text.bind("<Control-O>",self.openfile)

          self.text.bind("<Control-d>",self.copy_cur_line)
          self.text.bind("<Control-D>",self.copy_cur_line)

          self.text.bind("<Tab>", self.spaces)
          self.text.bind("<KeyRelease>", self.cur_line_col)
          self.text.bind("<Button-1>", self.cur_line_col)
          self.text.bind("<Button-3>", self.cur_line_col)
          self.text.bind("<Button-2>", self.cur_line_col)
          self.text.bind("<Motion>", self.cur_line_col)
          self.text.bind("<Configure>", self.cur_line_col)

          self.master.bind("<Control-[>", self.indent)
          self.master.bind("<Control-]>", self.dedent)
          self.master.bind("<Control-/>", self.comment)
          self.master.bind("<Alt-s>", self.uncomment)

          self.master.bind("<Alt-Up>", self.zoom_in)
          self.master.bind("<F3>", self.zoom_out)

          self.master.bind("<Shift-(>",self.insert_paren)
          self.master.bind("<[>",self.insert_paren)
          self.master.bind("<Shift-{>",self.insert_paren)

          self.master.bind("<Control-b>", self.runscript)

          self.animation()
          self.display_time()
          self.__styles()

          self.master.bind("<KeyRelease>", self.highlight)
          self.master.bind("<Key>", self.highlight)
          
     def highlight(self, e):
          self.recolor()
          
     def highlight_(self):
          self.recolor()
          self.master.after(1000, self.highlight_())
          
     def __styles(self):
          self.bdfont=font.Font(self.text, self.text.cget("font"))
          self.bdfont.config(weight=font.BOLD)
          
          self.itfont=font.Font(self.text, self.text.cget("font"))
          self.itfont.config(slant=font.ITALIC)

          self.style = __get__('default')

          for ttype, ndef in self.style:
               self.tag_font = None
               if ndef['bold']:
                    self.tag_font = self.bdfont
               elif ndef['italic']:
                    self.tag_font = self.itfont

               if ndef['color']:
                    self.fg = "#%s" % ndef['color']

               else:
                    self.fg=None

               self.text.tag_configure(str(ttype), foreground=self.fg, font=self.tag_font)
     def recolor(self):
          self.code = self.text.get("1.0", "end-1c")
          self.tokensource = self.lexer.get_tokens(self.code)
          self.start_line = 1
          self.start_index = 0

          self.end_line = 1
          self.end_index = 0

          for ttype, value in self.tokensource:
               if "\n" in value:
                    self.end_line += value.count("\n")
                    self.end_index = len(value.rsplit("\n", 1)[1])
                    
               else:
                    self.end_index += len(value)

               if value not in (" ", "\n"):
                    idx1 = "%s.%s" % (self.start_line, self.start_index)
                    idx2 = "%s.%s" % (self.end_line, self.end_index)

                    for tagname in self.text.tag_names(idx1):
                         self.text.tag_remove(tagname, idx1, idx2)

                    self.text.tag_add(str(ttype), idx1, idx2)
               self.start_line = self.end_line
               self.start_index = self.end_index

     def draw(self):
          self.filename=None;self.path=None
          self.master.title("PyDE - {}".format("Untitled"))
          self.master.config(bg = "Gray")
          
          self.anime__ = Canvas(self.master,width=1200, height=25, bg="Gray", relief=RAISED, highlightbackground='Gray')
          self.anime__.pack(anchor=NE)
          
          self.__display=Label(self.master, text="", bg="Gray",fg="White" ,padx=55, pady=10,
          justify=RIGHT, font=("8514oem",1 ,'normal'))
          self.__display.place(x=0, y=0)
          
          self.lcol=Label(self.master, bg="Gray")
          self.lcol.pack(side=BOTTOM, fill=X)

          self.scrollx=Scrollbar(self.master, orient=HORIZONTAL)
          self.scrollx.pack(side=BOTTOM, fill=X)
          
          self.text=ST(self.master,xscrollcommand=self.scrollx.set,selectbackground="Gray",fg="Gray",height=400, bg="Black", width=500, wrap=NONE, blockcursor=True)
          self.text.pack(side=TOP)

          self.scrollx.config(command=self.text.xview)

          self.text.config(fg="White", font=("8514oem", self.ftsize, 'bold'), insertbackground="Red")

          self.l_c=Label(self.lcol, bg="Gray")
          self.l_c.pack(side=RIGHT)
          
          self.timelabel=Label(self.lcol, text="",bg=self.anime__['bg'], font=("8514oem", self.ftsize, "bold"))
          self.timelabel.place(x=0, y=self.master.winfo_height()-3)

     def newfile(self, e):
          self.filename=None;self.path=None
          self.curname="Untitled"
          if len(self.text.get(0.0, END)) > 1:
               self.asknew=askyesno("File changed", "Save file?")
               if self.asknew == True:
                    self.savefile_()
               else:
                    self.text.delete(1.0, END)
                    self.master.title("PyDE - {}".format(self.curname))
                    self.__display.config(text="Untitled.py")
          else:
               self.__display.config(text="Untitled.py")
     def savefile_(self):
          if self.filename == None:
               self.s=asksaveasfile(defaultextension=self.types, filetypes=self.types)
               self.path=self.s.name
               self.curname=self.s.name.split("/")[-1]
               self.master.title("PyDE - {}".format(self.curname))
               self.__display.config(text=self.curname)
          else:
               self.s.write(self.text.get(1.0, END))
     def savefile(self, e):
          if self.filename == None:
               self.s=asksaveasfile(defaultextension=self.types, filetypes=self.types)
               self.path=self.s.name
               self.curname=self.s.name.split("/")[-1]
               self.master.title("PyDE - {}".format(self.curname))
               self.__display.config(text=self.curname)
          else:
               self.s.write(self.text.get(1.0, END))
     def openfile(self, e):
          try:
               self.o=askopenfile(filetypes=self.types, defaultextension=self.types)
               self.curname=self.o.name.split("/")[-1]
               self.path=self.o.name
               self.master.title("PyDE - {}".format(self.curname))
               self.__display.config(text=self.curname)
               if self.text.edit_modified():
                    self.a_open=askyesno("save this thing?", "Save file?")
                    if self.a_open == True:
                         self.savefile_()
                    else:
                         pass
               else:
                    self.text.delete(0.0, END)
                    self.op=self.o.read()
                    self.text.insert(END, self.op)
          except UnicodeDecodeError:
               self.unable=showerror("Invalid file", "Invalid file")
     def openfile_(self):
          try:
               if self.text.edit_modified():
                    self.savefile_()
               else:
                    self.o=askopenfile(filetypes=self.types, defaultextension=self.types)
                    self.op=self.o.read()
                    self.path=self.o.name
                    self.text.insert(END, self.op)
          except UnicodeDecodeError:
               self.unable=showerror("Invalid file", "Invalid file")
     def animation(self):
          self.x += 5
          self.anime__.delete(ALL)
          self.anime__.create_image(self.x*2,self.y+5, image=self.mario1)
          if (self.x-10) >= self.anime__.winfo_width():
               self.x = 0
          self.master.after(100, self.animation)
#          self.y-=5
          
     def cur_line_col(self, e):
          self.l_raw=self.text.index(INSERT)
          self.lines=self.l_raw.split(".")[0]
          self.cols=self.l_raw.split(".")[1]
          self.binder_=int(self.cols)
          self.l_c.config(text="lines:{0}  columns:{1}".format(self.lines, self.cols), font=("8514oem", 9, 'bold'))
     def spaces(self, e):
          self.text.insert(INSERT, " " * 4)
          return 'break'

     def indent(self, e):
          self.tab="    "
          self.untabbed=self.text.get("sel.first", "sel.last")
          self.splitted=self.untabbed.split("\n")
          self.text.delete("sel.first","sel.last" )
          self.conts=[]
          for self.conts in list(self.splitted):
               self.conts=self.tab+self.conts+"\n"
               self.text.insert(INSERT, self.conts)
     def dedent(self, e):
          self.tab="    "
          self.tabbed=self.text.get("sel.first", "sel.last")
          self.splitted=self.tabbed.split("\n")
          self.text.delete("sel.first","sel.last")
          self.conts=[]
          for self.conts in list(self.splitted):
               self.conts=self.conts.replace(self.tab, "")+"\n"
               self.text.insert(INSERT, self.conts)
     def comment(self,e):
          self.comment="#"
          self.uncommented=self.text.get("sel.first", "sel.last")
          self.split_comment=self.uncommented.split("\n")
          self.split_comment=list(self.split_comment)
          self.text.delete("sel.first", "sel.last")
          self.commconts=[]
          for self.commconts in self.split_comment:
               self.commconts = self.comment+self.commconts+"\n"
               self.text.insert(INSERT, self.commconts)
     def uncomment(self,e):
          self.comment="#"
          self.commented=self.text.get("sel.first", "sel.last")
          self.split_uncomm=self.commented.split("\n")
          self.split_uncomm=list(self.split_uncomm)
          self.text.delete("sel.first", "sel.last")
          self.unconts=[]
          for self.unconts in self.split_uncomm:
               self.unconts = self.unconts.replace(self.comment, "") + "\n"
               self.text.insert(INSERT, self.unconts)

     def runscript(self, e):
          if self.path==None:
               self.asksave=askyesno("Save this file?","Save?")
               if self.asksave == True:
                    self.savefile()
                    os.system("python {}".format(self.path))
                    self.result=str(subprocess.check_output(['python',self.path]))
                    self.output=showinfo("Output", "%s" % (self.result))          

               else:
                    showinfo("Cant run before saving..","Cant run before saving..")
          else:
               os.system("python {}".format(self.path))
               self.result=str(subprocess.check_output(['python',self.path]))
               self.output=showinfo("Output", "%s" % (self.result))          

                    
     def zoom_in(self, event):
          self.ftsize += 2
          self.bdfont.config(size=self.ftsize)
          self.itfont.config(size=self.ftsize)
          self.text.config(font=("8514oem", self.ftsize, 'bold'))
          
     def zoom_out(self, e):
          self.ftsize -= 2
          self.bdfont.config(size=self.ftsize)
          self.itfont.config(size=self.ftsize)
          self.text.config(font=("8514oem", self.ftsize, "bold"))
          
     def display_time(self):
          self.curtime=strftime("%H : %M : %S")
          self.timelabel.config(text=self.curtime)
          self.master.after(1000, self.display_time)
          
     def insert_paren(self, e):
          self.startparams="([{"
          self.endparams=")]}"
          self.cursor=self.text.index(INSERT)
          self.linecur=str(self.cursor.split(".")[0])
          self.colcur=int(self.cursor.split(".")[1])
          if e.char == self.startparams[0] : self.text.insert(INSERT, self.endparams[0]);self.text.mark_set(INSERT, self.linecur+"."+str(self.colcur))
          elif e.char == self.startparams[1] : self.text.insert(INSERT, self.endparams[1]);self.text.mark_set(INSERT, self.linecur+"."+str(self.colcur))
          elif e.char == self.startparams[2] : self.text.insert(INSERT, self.endparams[2]);self.text.mark_set(INSERT, self.linecur+"."+str(self.colcur))
          else : pass
          
     def copy_cur_line(self, e):
          self.linetext=self.text.get("insert linestart", "insert lineend")
          self.newidx=float(self.text.index(INSERT)) + 1.1
          self.text.insert(INSERT,"\n")
          self.text.insert(self.newidx, self.linetext+"\n")
          self.text.mark_set("insert", self.newidx)
          
          return 'break'
if __name__ == "__main__":
     root=Tk()
     main(root, PythonLexer())
     root.mainloop()
