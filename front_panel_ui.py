from manage_acc_ui import ManageAccount
from instafollower import processRunStatus
from status_panel import StatusPanel
from tkinter import *
from tkinter import messagebox


PANEL_WIDTH = 776
PANEL_HEIGHT = 448
BKG_IMG = "./backgrounds/Wireframe- welcome screen – 1.png"
BTN_STATUS_IMG = "./icons/status.png"
BTN_MANAGE_ACC_IMG = "./icons/manage_account.png"
BTN_ABOUT_IMG = "./icons/about.png"
BTN_COLOR = "#2A5464"
FONT = "Times 12"




class FrontPanel(Tk,Canvas):

    def __init__(self):

        self.panel = Tk()
        panel = self.panel
        panel.title("QBot Front Panel")

        panel.config(width = PANEL_WIDTH,height = PANEL_HEIGHT)
        screen_width = panel.winfo_screenwidth()
        screen_height = panel.winfo_screenheight()
        panel.geometry(f"{PANEL_WIDTH}x{PANEL_HEIGHT}"
                       f"+{int((screen_width - PANEL_WIDTH)/2)}+{int((screen_height - PANEL_HEIGHT)/2)}")

        self.canvas = Canvas(panel,width=2*PANEL_WIDTH, height=2*PANEL_HEIGHT)
        canvas = self.canvas
        img = PhotoImage(file=BKG_IMG)
        canvas.create_image(PANEL_WIDTH,PANEL_HEIGHT,image=img)
        canvas.place(x=-(PANEL_WIDTH/2),y=-(PANEL_HEIGHT/2))

        btn_status_img = PhotoImage(file=BTN_STATUS_IMG)
        status_btn = Button(image=btn_status_img,bg=BTN_COLOR,highlightthicknes=0,command=self.status_panel_caller)
        status_btn.place(x=567,y=64)
        status_lbl = Label(text="Status",bg="white",font=FONT).place(x=502,y=93)

        btn_manage_acc_img = PhotoImage(file=BTN_MANAGE_ACC_IMG)
        manage_acc_btn = Button(image=btn_manage_acc_img, bg=BTN_COLOR, highlightthicknes=0,command=self.manage_account_caller)
        manage_acc_btn.place(x=567, y=184)
        manage_acc_lbl = Label(text="Manage Account", bg="white",font=FONT).place(x=435, y=213)

        btn_abt_img = PhotoImage(file=BTN_ABOUT_IMG)
        abt_btn = Button(image=btn_abt_img, bg=BTN_COLOR, highlightthicknes=0)
        abt_btn.place(x=567, y=304)
        abt_lbl = Label(text="About", bg="white", font=FONT).place(x=500, y=332)

        panel.resizable(0, 0)
        panel.protocol('WM_DELETE_WINDOW', self.killProcess)

        panel.mainloop()


    def manage_account_caller(self):
        self.ma = ManageAccount()

    def status_panel_caller(self):
        self.sp = StatusPanel()

    def killProcess(self):
        if processRunStatus() == False:
            self.panel.destroy()
        else:
            messagebox.showinfo("Process Running",message="Please terminate ongoing Process")


