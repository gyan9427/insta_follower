from databaseManager import DatabaseManager
from tkinter import *
from tkinter import  messagebox


PANEL_HEIGHT = 440
PANEL_WIDTH = 304
MANAGE_ACC_BKG_IMG = "./backgrounds/manage_acc_ui_bkg.png"
BTN_ADD_ACC_IMG = "./icons/add_insta.png"
BTN_EDIT_ACC_IMG = "./icons/edit_insta.png"
BTN_COLOR = "white"
FONT = "Times 14"
BG_BLUE = "#038ABF"
IS_MANAGE_ACCOUNT_OPEN = False
LAVENDER = "#E6E6FA"

class ManageAccount:

    def __init__(self):
        global IS_MANAGE_ACCOUNT_OPEN

        if IS_MANAGE_ACCOUNT_OPEN == False:
            IS_MANAGE_ACCOUNT_OPEN = True
            self.acPanel = Toplevel()
            panel = self.create_manage_acc_panel(self.acPanel)

            self.canvas = Canvas(panel, width=2 * PANEL_WIDTH, height=2 * PANEL_HEIGHT)
            canvas = self.canvas
            img = PhotoImage(file=MANAGE_ACC_BKG_IMG)
            canvas.create_image(PANEL_WIDTH, PANEL_HEIGHT, image=img)
            canvas.place(x=-(PANEL_WIDTH / 2), y=-(PANEL_HEIGHT / 2))
            add_insta_img = PhotoImage(file=BTN_ADD_ACC_IMG)
            add_insta_btn = Button(panel, image=add_insta_img, command=self.add_insta_account, bg=BTN_COLOR,
                                   highlightthicknes=0)
            add_insta_btn.place(x=126, y=101)
            status_lbl = Label(panel, text="Add Insta Account", fg='white', bg=BG_BLUE, font=FONT).place(x=78, y=52)

            manage_acc_img = PhotoImage(file=BTN_EDIT_ACC_IMG)
            manage_acc_btn = Button(panel, image=manage_acc_img, bg=BTN_COLOR, highlightthicknes=0,command=self.edit_insta_account)
            manage_acc_btn.place(x=121, y=264)
            manage_acc_lbl = Label(panel, text="Edit Insta Account", fg='white', bg=BG_BLUE, font=FONT, ).place(x=78,
                                                                                                              y=220)

            panel.protocol('WM_DELETE_WINDOW', self.makeFalseTrue)
            panel.resizable(0, 0)
            self.acPanel.mainloop()

    def create_manage_acc_panel(self,panel):
        panel.title("Front Panel")
        # panel.config(width=PANEL_WIDTH, height=PANEL_HEIGHT)
        self.screen_width = panel.winfo_screenwidth()

        self.screen_height = panel.winfo_screenheight()
        panel.geometry(
            f"{PANEL_WIDTH}x{PANEL_HEIGHT}+{int((self.screen_width - PANEL_WIDTH) / 2)}+{int((self.screen_height - PANEL_HEIGHT) / 2)}")

        return panel

    def makeFalseTrue(self):
        global IS_MANAGE_ACCOUNT_OPEN
        IS_MANAGE_ACCOUNT_OPEN = False
        self.acPanel.destroy()



    # Add insta Panel Adds credentials to the Database
    def add_insta_account(self):

        self.acPanel.geometry(f"{3*PANEL_WIDTH}x{PANEL_HEIGHT}+{int((self.screen_width - 3* PANEL_WIDTH) / 2)}+{int((self.screen_height - PANEL_HEIGHT) / 2)}")
        self.frame = Frame(self.acPanel,bg=LAVENDER,width=3 * PANEL_WIDTH, height=PANEL_HEIGHT)
        self.frame.place(x=0,y=0)

        btn_back = Button(self.frame,width=16,height=2, text="Back", fg="black",command = lambda:self.kill(self.frame,
                                                                                        self.acPanel,
                                                                                        PANEL_WIDTH,
                                                                                        PANEL_HEIGHT,
                                                        int((self.screen_width - PANEL_WIDTH) / 2),
                                                        int((self.screen_height - PANEL_HEIGHT) / 2)))
        btn_back.place(x=316,y=348)

        btn_add = Button(self.frame, width=16, height=2, text="Add", fg="black",command=self.credentials)
        btn_add.place(x=488, y=348)

        self.h_canvas = Canvas(self.frame,width=3*PANEL_WIDTH,height=73,bg=BG_BLUE)
        self.h_canvas.create_text(460,35,text="MANAGE ACCOUNT",font=FONT,fill="white")
        self.h_canvas.place(x=-2,y=0)

        self.l_labelFrame = LabelFrame(self.frame,width=355,height=152,text="Account Credentials",bg=LAVENDER)
        self.l_labelFrame.place(x=84,y=180)

        self.rt_labelFrame = LabelFrame(self.frame,text="Comment Text", width=355, height=152,bg=LAVENDER)
        self.rt_labelFrame.place(x=488, y=180)
#
# ID LIST
#
        self.account_list = Listbox(self.frame,width=48,height=2)
        try:
            self.listElement(self.account_list)
        except:
            pass
        self.account_list.place(x=309,y=113)

        self.account_list_label = Label(self.frame,text="Insta Account List:",bg=LAVENDER)
        self.account_list_label.place(x=309,y=93)

        self.acc_id = Entry(self.frame,width=30)
        self.acc_id.place(x=94,y=230)
        self.acc_id_label = Label(self.frame,text="Insta Acount Id :",bg=LAVENDER)
        self.acc_id_label.place(x=94,y=208)

        self.acc_password = Entry(self.frame, width=30,show="*")
        self.acc_password.place(x=94, y=283)
        self.acc_password_label = Label(self.frame, text="Insta Acount password :", bg=LAVENDER)
        self.acc_password_label.place(x=94, y=260)

        self.comment_text = Text(self.frame,width=40,height=4)
        self.comment_text.place(x=498, y=230)

    # Collects credentials and Adds to the Database on Add-button (btn_add) click
    def credentials(self):
        VALIDATE_ADD = False
        id = self.acc_id.get()
        pwd = self.acc_password.get()
        comment = self.comment_text.get("1.0","end-1c")

        if id != "" and pwd != "" and comment != "":
            VALIDATE_ADD = True
        if VALIDATE_ADD:
            self.acc_id.delete(0,END)
            self.acc_password.delete(0,END)
            self.comment_text.delete("1.0",END)
            self.acc_id.focus()
            dm = DatabaseManager(pwd=pwd,id=id,msg=comment)
            dm.prepare_credentials()
            # self.listElement()
        else:
            messagebox.showerror("Empty Credentials",message="You cannot leave any Credentials empty")

    def edit_insta_account(self):
        self.acPanel.geometry(
            f"{3 * PANEL_WIDTH}x{PANEL_HEIGHT}+{int((self.screen_width - 3 * PANEL_WIDTH) / 2)}+{int((self.screen_height - PANEL_HEIGHT) / 2)}")
        self.edit_acc_frame = Frame(self.acPanel, bg=LAVENDER, width=3 * PANEL_WIDTH, height=PANEL_HEIGHT)
        self.edit_acc_frame.place(x=0, y=0)

        ## EDIT PANEL user LIST
        self.rt_labelFrame = LabelFrame(self.edit_acc_frame, text="Insta Account List", width=355, height=152, bg=LAVENDER)
        self.rt_labelFrame.place(x=488, y=180)
        curr_acc_lbl = Label(self.edit_acc_frame, text="Insta account IDs :", bg=LAVENDER)
        self.user_list = Listbox(self.edit_acc_frame,width=54, height=7)
        try:
            self.listElement(self.user_list)
        except:
            pass
        self.user_list.bind('<<ListboxSelect>>', self.curSelect)
        self.user_list.place(x=500, y=203)

        self.h_canvas = Canvas(self.edit_acc_frame, width=3 * PANEL_WIDTH, height=73, bg=BG_BLUE)
        self.h_canvas.create_text(460, 35, text="EDIT ACCOUNT", font=FONT, fill="white")
        self.h_canvas.place(x=-2, y=0)

        btn_back = Button(self.edit_acc_frame, width=16, height=2, text="Back", fg="black", command=lambda: self.kill(self.edit_acc_frame,
                                                                                                             self.acPanel,
                                                                                                             PANEL_WIDTH,
                                                                                                             PANEL_HEIGHT,
                                                                                                             int((self.screen_width - PANEL_WIDTH) / 2),
                                                                                                             int((self.screen_height - PANEL_HEIGHT) / 2)))

        btn_back.place(x=266, y=348)

        self.btn_edit = Button(self.edit_acc_frame, width=16, height=2, text="Edit", fg="black",state='disabled',command=self.edit_message)
        self.btn_edit.place(x=416, y=348)

        self.btn_delete = Button(self.edit_acc_frame, width=16, height=2, text="Delete Account", fg="black",state='disabled'
                                 ,command=self.delete_user)
        self.btn_delete.place(x=566, y=348)

        self.l_labelFrame = LabelFrame(self.edit_acc_frame, width=355, height=152, text="Details", bg=LAVENDER)
        self.l_labelFrame.place(x=84, y=180)

    # Panel: Edit Accounts :: Frame: Insta Account List :: Action: fetching message from database on item selection
    def curSelect(self,event):
        try:
            dm = DatabaseManager()
            self.selected_user_id = (self.user_list.get(self.user_list.curselection()))
            msg = dm.fetch_message(self.selected_user_id)
            self.show_details(msg[0][0])
            self.btn_delete.config(state='active')
            self.btn_edit.config(state='active')
        except:
            pass

    # Panel: Edit Accounts :: Frame: Details :: Action: Appearance of messages
    def show_details(self,msg):
        message = StringVar()
        message.set(msg)

        try:
            self.lbl_detail.destroy()
            self.msg_text.destroy()
            self.btn_update.destroy()
        except:
            pass
        self.lbl_detail = Label(self.edit_acc_frame, bg=LAVENDER)
        self.lbl_detail.config(textvariable= message)
        self.lbl_detail.place(x=104, y=200)

    # Panel: Edit Accounts :: Frame: Details :: Action: Editing pre-existing messages
    def edit_message(self):
        self.msg_text = Text(self.edit_acc_frame,width=39,height=3)
        self.msg_text.place(x=104, y=230)
        self.btn_update = Button(self.edit_acc_frame, width=8, height=1, text="Update", fg="black",command=self.message_to_db,
                                 state='disabled')
        self.btn_update.place(x=104, y=290)
        self.msg_text.bind('<FocusIn>',self.message_update)

    # Panel: Edit Accounts :: Frame: Details :: Action: Activating update message
    def message_update(self,event):
        self.btn_update.config(state='active')

    # Panel: Edit Accounts :: Frame: Details :: Action: Updating message to Database
    def message_to_db(self):
        msg = self.msg_text.get("1.0","end-1c")
        if msg == "":
            messagebox.showerror("Empty box",message="You can't update empty message")
        else:
            dm = DatabaseManager()
            dm.update_message(msg,self.selected_user_id)

    # Panel: Edit Accounts :: Frame: Details :: Action: Deleting selected ID Database
    def delete_user(self):
        dm = DatabaseManager()
        dm.delete_data(self.selected_user_id)
        selection = self.user_list.curselection()
        self.user_list.delete(selection)
    def kill(self,frame,prev_frame,W,H,X,Y):
        frame.destroy()
        prev_frame.geometry(f"{W}x{H}+{X}+{Y}")

    def listElement(self,acc):
        dm = DatabaseManager()
        data = dm.fetch_all()
        i=1
        for tup in data:
            acc.insert(i,tup[1])
            i+=1