from tkinter import *
import tkinter as tk
import tkinter.font as font
from tkinter.messagebox import showinfo, askquestion
from Train import Train, Ticket
from datetime import date, time
from time import localtime, strftime
from PIL import ImageTk, Image
import sys
import os
"""
Imran Diva
Revision date: 21-05-05
"""


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        """The menu page where the user chooses which train it wants to book

                :parent: container where the page is located in Program class
                :param controller: Switcher that switches between pages
           """
        tk.Frame.__init__(self, parent, bg="green")
        self.controller = controller

        # Background of page
        background = ImageTk.PhotoImage(Image.open("background3.jpg"))
        label = tk.Label(self, image=background)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.image = background

        welcome = Label(self,
                        text="  Välkommen till SJs bokningssida. Välj den avgång som du vill boka/avboka i menyn: ", bg="green", fg="white")
        choices = []
        for train in self.controller.shared_data["all_trains"]:
            choices.append(f"Tåg-ID: {train.id} -- {train.date} {train.time} "
              f"-- {train.train_model}: {train.start} - {train.destination}")
        
        # No trains available
        if len(choices) == 0:
            welcome = Label(self,
                        text="  INGA BOKBARA TÅG ", bg="green", fg="white")
        else:
            menu = OptionMenu(self, tkvar, *choices, command=self.go_to_action)
            menu.grid(row=2, column=2, sticky="nsew", columnspan=2)



        myfont = font.Font(family='Helvetica', size=20, weight='bold')
        tkvar = self.controller.shared_data["chosen"]
        tkvar.set('Välj avgång')
        quit_button = Button(self, text="Avsluta program", fg="red", command=self.quit_app)
        welcome["font"] = myfont
        Label(self,text="", bg="green").grid(row=0, columnspan=2)

        welcome.grid(row=1, column=2, columnspan=2, pady=10)
        quit_button.grid(row=2, column=4, sticky="nsew", columnspan=2, padx=10)

    # Show the button that takes the user to the action page
    def go_to_action(self, value):
        Button(self, text="Gå vidare", command=lambda: self.controller.show_frame("Action")).grid(row=3, column=2, pady=3, sticky="nsew", columnspan=2)

    # Quit the app
    def quit_app(self):
        root.quit()


class Action(tk.Frame):
    """The action page where the user chooses whether it wants to book or cancel seats

            :parent: container where the page is located in Program class
            :param controller: Switcher that switches between pages
       """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="green")
        self.controller = controller


        # Background of page
        background = ImageTk.PhotoImage(Image.open("background3.jpg"))
        label = tk.Label(self, image=background)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.image = background

        myfont = font.Font(family='Helvetica', size=20, weight='bold')
        Label(self, text="Vad vill du göra:", font=myfont, bg='green', fg="white").grid(row=0, column=0, padx=80, pady=150, sticky="ew")
        Button(self, text="Boka plats", font=myfont, command=self.choose_book).grid(row=0, column=2, padx=80, sticky="ew")
        Button(self, text="Avboka plats", font=myfont, command=self.choose_cancel).grid(row=0, column=4, padx=80,sticky="ew")
        Button(self, text="Välj annan avgång", font=myfont, command=lambda: self.controller.show_frame("Menu")).grid(row=0, column=6, padx=80, sticky="ew")

    # Declare that the user wants to book seats and go to the seat booking page
    def choose_book(self):
        self.controller.shared_data["book"] = True
        self.controller.show_frame("TrainSeats")

    # Declare that the user wants to cancel seats and go to the seat booking page
    def choose_cancel(self):
        self.controller.shared_data["book"] = False
        self.controller.show_frame("TrainSeats")



class TrainSeats(tk.Frame):
    """The page where the user chooses which seats it wants to book

            :parent: container where the page is located in Program class
            :param controller: Switcher that switches between pages
       """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.canvas = tk.Canvas(self, borderwidth=0, bg="black", width=1200, height=200)
        self.frame = tk.Frame(self, bg='black', width=100, height=40)
        self.scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.grid(row=0, column=0)
        self.canvas.create_window((0, 0), window=self.frame, anchor="w",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        Button(self, text="Visa tåg", command=self.train_view).grid(row=3, column=0, padx=0, pady=10, sticky="ew")

    # Creates the train view of all the seat on the chosen train
    def train_view(self):
        self.key()
        self.chosen = ""
        self.index = 0
        self.counter = 0
        info = self.controller.shared_data["chosen"].get()
        info = info.split(' ')
        train_id = info[1]

        for row, train in enumerate(self.controller.shared_data["all_trains"]):
            if train.id == train_id:
                self.chosen = train
                self.index = row
                self.controller.shared_data["index"] = self.index

        booked = [seat for seat in self.chosen.reserved]
        self.cell = {}
        quiet = []
        # Shows the train seats for all coaches
        for c in range(int(self.chosen.coaches)):
            row_elements = []
            start = (self.chosen.rows*self.chosen.columns) * c
            tk.Label(self.frame, background="black", foreground="white", width=4, text="Vagn " + str(c+1)).grid(row=0, column=(start)+1, sticky="nsew")
            for row in range(1, self.chosen.rows+1):
                start = (self.chosen.rows*self.chosen.columns) * c
                seat_add = [1, 7, 5, 3]
                previous_seat = row
                for count, col in enumerate(range(1, self.chosen.columns+1)):
                    seat = previous_seat
                    if col > 1:
                        seat += seat_add[seat % 4]
                    if row == 1:
                        self.controller.shared_data["window_seats"].append(seat + start)
                    if count < 4:
                        self.controller.shared_data["quiet_area"].append(seat+start)
                    cell = tk.Label(self.frame, foreground="white", width=4, text=str(seat+start))
                    row_elements.append(seat+start)
                    if seat+start in booked:
                        cell.configure(background="red")
                        if 0 < col < 5:  # quiet area seat and booked
                            quiet.append(seat+start)
                    elif 0 < col < 5: # quiet area seat
                        cell.configure(background="#72bcd4")
                        quiet.append(seat+start)
                    else:
                        cell.configure(background="darkgray")

                    if self.controller.shared_data["book"] is True:
                        cell.bind("<1>", lambda event, col=seat+start, row=row: self.book_mechanism(row, col, quiet))

                    else:
                        cell.bind("<1>", lambda event, col=seat+start, row=row: self.cancel_mechanism(row, col))
                    # Spacing between seats
                    x_spacing, y_spacing = 2, 2

                    if col == 1:
                        x_spacing = (10, 2)
                    if row == self.chosen.rows / 2:
                        y_spacing = (2, 20)

                    cell.grid(row=row, column=col + start, sticky="nsew", padx=x_spacing, pady=y_spacing)
                    self.cell[(row, seat+start)] = cell

                    previous_seat = seat
            self.chosen.seats.append(row_elements)

        self.booking_guide()

    # Shows a guide to help the user with what is supposed to do to book or cancel a seat
    def booking_guide(self):
        if self.controller.shared_data["book"] is False:
            to_do = "avb"
        else:
            to_do = "b"

        Label(self,text=f"Vald avgång: {self.chosen.date} {self.chosen.time}"
            f" -- {self.chosen.train_model}: {self.chosen.start} - {self.chosen.destination}"
            f"\n\nTryck på de platser som du vill {to_do}oka. Tryck sen på FORTSÄTT för att gå bekräfta dina {to_do}okningar."
            f" Vill du inte {to_do}oka några platser, tryck också på FORTSÄTT"
            ).grid(row=3, column=0, padx=0, pady=10, sticky="ew")
        self.key()
        Button(self, text="Forsätt", command=self.confirm_message).grid(row=4, column=0, pady=10, sticky="ew")

    # Creates a confirm message of what the user has done
    def confirm_message(self):

        if self.controller.shared_data["book"] is False:
            action = "avbokat"

        else:
            action = "bokat"

            Button(self, text="Skriv ut biljetter", command=self.print_ticket).grid(row=3, column=0, sticky="nsew", rowspan=3)

        if self.counter > 0: # If user has chosen seats to reserve or cancel
            Label(self, text=f"Du har nu {action} dina biljetter. Tryck på en knapp för att bestämma vad "
                            "du vill göra nu").grid(row=0, column=0, sticky="nsew")
        else:
            Label(self, text=f"Du har inte {action} några biljetter. Tryck på en knapp för att bestämma vad "
                             "du vill göra nu").grid(row=0, column=0, sticky="nsew")

        Button(self, text="Gör nya bokningar eller avbokningar", command=self.to_restart).grid(row=7, column=0, sticky="nsew", rowspan=3)
        Button(self, text="Avsluta program", command=self.quit_program).grid(row=10, column=0, sticky="nsew", rowspan=2)

    def onFrameConfigure(self, event):
        """Resets the scroll region to encompass the inner frame"""

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def book_mechanism(self, row, col, quiet):
        """Books the chosen seat and adds it to the booked list

            :param row: the row of where the seat is located on the train
            :param col: the column where the seat is located on the train
            :param quiet: A list that includes all the seats that are in the quiet area on the train
        """
        self.seat_num = col
        colour = self.cell[(row, col)].cget("background")
        if colour == "red": # If seat is already booked by another person
            self.bell()

        elif colour == "green": # If seat is reserved by user
            self.chosen.reserved.remove(self.seat_num)
            self.controller.shared_data["user_bookings"].remove(self.seat_num)
            self.counter -= 1
            if self.seat_num in quiet:
                self.cell[(row, col)].configure(text=self.seat_num, bg="#72bcd4")
            else:
                self.cell[(row, col)].configure(text=self.seat_num, bg="darkgray")

        else: # If seat is not booked by anyone
            if neighbor_check(self.chosen, self.seat_num, self.controller.shared_data["user_bookings"]):
                self.cell[(row, col)].configure(text=self.seat_num, bg="green")
                self.controller.shared_data["user_bookings"].append(self.seat_num)
                self.chosen.reserved.append(self.seat_num)
                self.counter += 1
            else:
                pass


    def cancel_mechanism(self, row, col):
        """Removes the chosen seat from the booked list

            :param row: the row of where the seat is located on the train
            :param col: the column where the seat is located on the train
        """
        self.seat_num = col
        colour = self.cell[(row, col)].cget("background")
        if colour == "red":  # Already booked seats
            if len(self.chosen.reserved) > 0:
                self.chosen.reserved.remove(self.seat_num)
                self.counter += 1

            self.cell[(row, col)].configure(text=self.seat_num, bg="gold")

        elif colour == "gold": # The seats that the user wants to cancel
            self.counter -= 1
            self.chosen.reserved.append(self.seat_num)
            self.cell[(row, col)].configure(text=self.seat_num, bg="red")

        else:
            self.bell()

    # Creates a key to help user with what the colors on the seats on the train represents
    def key(self):
        tk.Label(self, text="Platserna är märkta med en särskild färg. Nedan finns information om vad varje färg innebär.", background="white", foreground="black").grid(row=7, column=0, padx=0, sticky="ew")
        tk.Label(self, text="Tyst avdelning", background="#72bcd4", foreground="black").grid(row=8, column=0, sticky="ew")
        tk.Label(self, text="Vanlig avdelning", background="darkgray", foreground="black").grid(row=9, column=0, sticky="ew")
        tk.Label(self, text="Redan bokad", background="red", foreground="black").grid(row=10, column=0, sticky="ew")

        if self.controller.shared_data["book"] is False:
            tk.Label(self, text="Plats du vill avboka", background="gold", foreground="black").grid(row=11, column=0, sticky="ew")
        else:
            tk.Label(self, text="Plats du vill boka", background="green", foreground="black").grid(row=11, column=0, sticky="ew")

    # Quits the program and updates txt file with booked/canceled seats
    def quit_program(self):
        all_trains = self.controller.shared_data["all_trains"]
        index = self.controller.shared_data["index"]
        update_file(all_trains, self.chosen, index)
        root.quit()

    # Restarts the program and updates txt file with booked/canceled seats
    def to_restart(self):
        all_trains = self.controller.shared_data["all_trains"]
        index = self.controller.shared_data["index"]
        update_file(all_trains, self.chosen, index)
        restart_program()

    def print_ticket(self):
        """Prints out all the seats that are booked and have not been printed

            :return 1: if there are no tickets to print
        """
        train = self.chosen
        user_bookings = self.controller.shared_data["user_bookings"]
        if len(user_bookings) < 1:
            showinfo(title="SJ",
                                message="Det finns bokningar att skriva ut!")

            return 1

        else:
            # w_seat is a list of all window seat numbers
            w_seats = self.controller.shared_data["window_seats"]
            for num in user_bookings: # Goes through all the booked seats by user
                area = ""
                if num in w_seats:
                    pos = "Fönsterplats"
                else:
                    pos = "Mittplats"

                if num in self.controller.shared_data["quiet_area"]:
                        area = "TYST AVDELNING"

                coach = 0
                for number,coaches in enumerate(train.seats):
                    if num in coaches:
                        coach = number + 1
                coach = str(coach)
                seat = str(num)
                t1 = Ticket(seat, pos, area, coach)
                showinfo(title="SJ",
                                    message=f"Biljett {seat} finns nu tillgänglig i en separat fil")

                with open(f"biljett_{num}.txt", "w") as f:
                    f.write("**********************\n")
                    f.write(t1.info(train))
                    f.write("Tänk på miljön. Undvik att skriva ut denna biljett på papper.\n")
                    f.write("**********************")

        Label(self, text=f"Du har nu skrivit ut dina biljetter. Tryck på en knapp för "
                          "för att antingen fotsätta använda"
                          "programmet eller för att avsluta").grid(row=0, column=0, sticky="nsew")

# Class that stores shared data for whole program and switches between different pages
class Program(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)

        self.shared_data = {
            "all_trains": read_file(),
            "user_bookings": [],
            "chosen": StringVar(),
            "book": False,
            "window_seats": [],
            "quiet_area": [],
            "index": 0
        }
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (Menu, Action, TrainSeats): # Creates the different pages
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Menu")

    def show_frame(self, page_name):
        """Shows a frame for the given page name

            :param page_name: the name of the page we want to show
        """

        frame = self.frames[page_name]
        frame.tkraise()


def read_file():
    """Reads the txt file and returns object for choice of train, its position in departure list,
    and list with all trains

        :return chosen: the object for chosen train
        :return index: an int that shows row of chosen train in txt file
        :return all_trains: list of all bookable train objects
    """
    train_ids = []  # list that stores the train numbers of all bookable trains
    all_trains = []     # Stores all bookable train objects
    with open("trains.txt", "r") as f:
        train = [[value for value in row.split(",")] for row in f]  # Saves all info of a row in txt file for each train
        for r in range(trains()):
            p_reserved = list(filter(None, (i for i in train[r][7:-1])))  # list of all the reserved seats already
            one_train = Train(train[r][0], train[r][1], train[r][2], train[r][3], train[r][4], train[r][5], train[r][6])

            if bookable_train(one_train, train_ids) is True: # If train has not already departed
                for seat in p_reserved:
                    one_train.reserved.append(int(seat))
                all_trains.append(one_train)

            else:
                continue

    return all_trains


def bookable_train(train, train_ids):
    """Checks if departure has not expired yet and prints its information

        :param train train: train object of chosen train
        :param train_ids: list of the ID of all bookable trains
        :return False: if the train has already departured
        :return True: if the train has not already departured, therefore is bookable
    """
    today = date.today()
    current_hour, current_min = strftime("%H:%M", localtime()).split(":")
    current_time = time(int(current_hour), int(current_min))
    year, month, day = train.date.split("-")
    hour, minute = train.time.split(":")
    dep_date, dep_time = date(int(year), int(month), int(day)), time(int(hour), int(minute))

    if dep_date < today or (dep_time < current_time and dep_date == today):
        return False

    else:
        train_ids.append(train.id)
        return True


def trains():
    """Finds the number of available train departures

        :return len(lines): the number of trains in txt file
    """
    with open("trains.txt", "r") as text_file:
        lines = text_file.readlines()
    return len(lines)


def update_file(all_trains, chosen, index):
    """Updates the txt file after the user has quit the program

        :param all_trains: list of all bookable train objects
        :param chosen: train object of chosen train
        :param index: row number where the chosen and changed train is located
    """

    all_trains[index] = chosen
    all_trains[index].reserved.sort()
    with open("/Users/imrandiva/PycharmProjects/SJ/trains.txt", "w") as text_file:
        for row in all_trains:
            row.reserved = ','.join(map(str, row.reserved))     # Turns list into string of reserved seat numbers
            new_line = str(row.file_row())
            text_file.write(new_line)


def neighbor_check(train, number, user_seats):
    """Checks if the chosen number is next to a previously reserved seat

        :param train: train object of chosen train
        :param number: seat number to check
        :param user_seats: list of all seats booked by user
        :return True: if there is a neighbor or there are no seats booked yet
        :return False: if the there is not a neighbor and user has to confirm one more time

    """

    seat_row = find_row(number, train)
    seat_col = find_col(number, train)

    if len(user_seats) == 0:
        return True
    else:
        if not_neighbor(seat_row, seat_col, number, user_seats):
            neighbor = askquestion(title="SJ",
                                              message="Din valda plats ligger inte bredvid en av dina andra bokade platser. Är det ok?")

            if neighbor == "yes":
                return True

            else:
                showinfo(title="SJ",
                                    message="Du har inte bokat denna plats. Välj att boka en plats som ligger bredvid dina andra bokade platser "
                                            "eller slutför dina bokningar.")
                return False
        else:
            return True

def not_neighbor(row, col, num, reserved):
    """Checks if seat is in an odd or even row and column, is not a neighbor seat, and is not reserved

        :param row: the row location of seat on train
        :param num: chosen seat number
        :param reserved: reserved seats
        :return num not in reserved: conditions for neighbor_check()
    """
    if row % 2 == 1:
        if col % 2 == 0:
            num = num - 1

        else:
            num = num + 1

    else:
        if col % 2 == 0:
            num = num + 1

        else:
            num = num - 1

    return num not in reserved

def find_row(number, train):
    """Find the row on the train where the seat number is located

        :param number: the seat number
        :param train: train object of chosen train
    """

    for coach_num, coach in enumerate(train.seats): # Searches all coaches
        row_num = 1
        index = 0
        for seat in coach: # Searches all seats in each coach to find matching one
            if index == train.columns:
                index = 0
                row_num += 1
            index += 1

            if seat == number:
                return int(row_num)


def find_col(number, train):
    """Finds the column index of seat and returns that index

        :param number: chosen seat number
        :param train: the chosen train object
        :return int(index): column location of seat number on train
    """
    column = 0
    for coach_num, coach in enumerate(train.seats): # Searches all coaches
        counter = 0
        for seat in coach: # Searches all seats in each coach to find matching one
            if counter == train.columns:
                counter = 0
                column = train.columns * coach_num
            column += 1
            counter += 1

            if seat == number:
                return int(column)


# Restarts the current program
def restart_program():  # https://stackoverflow.com/questions/41655618/restart-program-tkinter
    python = sys.executable
    os.execl(python, python, *sys.argv)


# Program function that runs the program
if __name__ == "__main__":
    root = Program()
    root.geometry("1200x460")
    root.title("SJ Tågbokningssida")
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(
        file='sj2.png'))  # https://stackoverflow.com/questions/31815007/change-icon-for-tkinter-messagebox

    root.mainloop()



