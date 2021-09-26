import tkinter as tk
import tkinter.filedialog as fd
from os import listdir
import PicEditPIL as PEPIL


class MainWindow(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.windowtitle = "Picture Tiler"
        self.master.title(self.windowtitle)
        self.widgets = {}
#       self.pack()
        self.create_ui()

    def create_ui(self):
        self.widgets["label"] = [self.create_label(self.master, "Choose starting image", 0, 0, "n", 10, 5)]
        self.widgets["textbox"] = [self.create_textbox(self.master, 50, 1, 0, "n", 10, 5)]
        self.widgets["button"] = [self.create_button(self.master, u"\u2BA1", 5, 1, 1, 1, "n", 2, 0, self.createospath)]
        self.widgets["label"].append(self.create_label(self.master, "Number of columns", 2, 0, "n", 10, 5))
        self.widgets["textbox"].append(self.create_textbox(self.master, 10, 3, 0, "n", 10, 5))
        self.widgets["label"].append(self.create_label(self.master, "Filename to save as", 4, 0, "n", 10, 5))
        self.widgets["textbox"].append(self.create_textbox(self.master, 10, 5, 0, "n", 10, 5))
        self.widgets["button"].append(self.create_button(self.master, "Start Tiling", 8, 1, 6, 0, "n", 2, 1, self.start_tile))
        self.imgsavetype = ".png"

    def create_textbox(self, mMaster, mWidth, mRow, mCol, mSticky="n", mPadX=0, mPadY=0):
        mTextbox = tk.Entry(master=mMaster, width=mWidth)
        mTextbox.grid(row=mRow, column=mCol, sticky=mSticky, padx=mPadX, pady=mPadY)
        return mTextbox

    def create_button(self, mMaster, mText, mWidth, mHeight, mRow, mCol, mSticky="n", mPadX=0, mPadY=0, mCommand=None):
        mButton = tk.Button(master=mMaster, text=mText, width=mWidth, height=mHeight, command=mCommand)
        mButton.grid(row=mRow, column=mCol, sticky=mSticky, padx=mPadX, pady=mPadY)
        return mButton

    def create_label(self, mMaster, mText, mRow, mCol, mSticky="n", mPadX=0, mPadY=0):
        mLabel = tk.Label(master=mMaster, text=mText)
        mLabel.grid(row=mRow, column=mCol, sticky=mSticky, padx=mPadX, pady=mPadY)
        return mLabel

    def createospath(self):
        #mfolder = fd.askdirectory()
        fpath = fd.askopenfilename()
        if fpath:
            self.widgets["textbox"][0].delete(0, last=tk.END)
        self.widgets["textbox"][0].insert(0, fpath)
        print(self.widgets["textbox"][0].get())

    def start_tile(self):
        self.startimgpath = self.widgets["textbox"][0].get()
        self.imgname = self.startimgpath.split("/")[-1]
        self.filedirectory = self.startimgpath[0:len(self.startimgpath) - len(self.imgname)]
        self.startimg = self.imgname.split(".")[0]
        self.imgtype = self.imgname.split(".")[-1]
        self.tileoperation()
        #print("File directory:", self.filedirectory, "\n imgname:", self.imgname, "\n startimg:", self.startimg, "\n imgtype:", self.imgtype)

    def tileoperation(self):
        mtilecol = self.widgets["textbox"][1].get()
        try:
            mtilecol = int(mtilecol)
        except:
            print("Not an integer value!")
        mfiles = listdir(self.filedirectory)
        mstart = mfiles.index(self.imgname)
        #mtempimg1 = self.filedirectory + mfiles[mstart]
        mtempimg1 = None
        mtempimg2 = None
        mcolcount = 0
        mnewtileline = False
        for midx in range(mstart, len(mfiles)):
            #mcolcount += 1
            #print("check col counter:", mcolcount, "midx:", midx)
            #if mcolcount >= mtilecol - 1:
            #print("logic:", (midx - mstart + 1) % mtilecol)
            if mtempimg1 is None:
                mtempimg1 = self.filedirectory + mfiles[midx]
            else:
                mtempimg1 = PEPIL.editImgHor(mtempimg1, self.filedirectory + mfiles[midx])

            if (midx - mstart + 1) % mtilecol == 0:
                if mtempimg2 is None:
                    mtempimg2 = mtempimg1.copy()
                    # mtempimg2 = PEPIL.editImgHor(mtempimg1, self.filedirectory + mfiles[midx + 1])
                else:
                    #print("mcolcount:", mcolcount, "mtilecol:", mtilecol, "\n mstart:", mstart,"vertical activated idx:", midx)
                    mtempimg2 = PEPIL.editImgVer(mtempimg2, mtempimg1)
                mtempimg1 = None
                #mtempimg1 = self.filedirectory + mfiles[midx + 1]
                #mcolcount = -1

        if (midx - mstart + 1) % mtilecol != 0:
            mtempimg1 = PEPIL.editImgFillTrans(mtempimg2, mtempimg1)
            mtempimg2 = PEPIL.editImgVer(mtempimg2, mtempimg1)
        mtempimg2.save(self.widgets["textbox"][2].get() + self.imgsavetype)

        #print(mfiles, "\n Place to start:", mfiles.index(self.imgname))
        #PEPIL.editImgHor()]
        #editImgHor(imgfile1,imgfile2,imgtosave="testing1.png")
        #editImgVer(imgfile1,imgfile2,imgtosave="testing1.png")


    def debugwidgets(self):
        """For debugging purposes, prints the dictionary of widget list and returns the dictionary of widgets"""
        print(self.widgets)
        return self.widgets

root = tk.Tk()
mWin = MainWindow(master=root)
mWin.mainloop()