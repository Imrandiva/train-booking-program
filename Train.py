
class Train:
    """A representation of a departure and the train used for the departure

        :param id: An int, the unique train-ID of the deparutre
        :param model: A string, the the train model used for the departure
        :param start: A string, the location where the train departs
        :param des: A string, the location where the train arrives
        :param date: A date, the date the train departs
        :param time: A time, the time the train departs
        :param coaches: An int, the number of coaches on the train
    """
    def __init__(self, id, model, start, des, date, time, coaches):
        self.id = id
        self.train_model = model
        self.start = start
        self.destination = des
        self.date = date
        self.time = time
        self.coaches = coaches
        self.rows = 4   # train has 4 rows of seats per coach
        self.columns = 8    # train has 8 columns of seats
        self.seats = list()     # list of all seat numbers on train
        self.reserved = list()  # list of all reserved seats on train

    # Reserve seat on train
    def reserve(self, num):
        num = int(num)
        if num > 0 and num not in self.reserved:
            self.reserved.append(num)

    # Cancel seat on train
    def cancel(self, num):
        num = int(num)
        if num in self.reserved:
            self.reserved.remove(num)

    # Function that updates each row in txt.file in the correct format
    def file_row(self):
        file_row = str(self.id) + "," + self.train_model + "," + self.start + "," + self.destination + "," + str(self.date) + "," + str(self.time)\
                  + "," + str(self.coaches) + "," + str(self.reserved) + ",\n"
        return file_row


class Ticket:
    """A representation of a train ticket

        :param seat: An int, the unique train-ID of the deparutre
        :param pos: A string, shows whether the seat is a window or a middle seat
        :param section: A string, shows if the seat is located in a quiet section, otherwise empty
    """
    def __init__(self, seat, pos, section, coach):
        self.seat = seat
        self.position = pos
        self.section = section
        self.coach = coach

    def info(self, train):
        """Prints out the ticket for each seat on the train

                    :param train: train object for chosen train
                    :return info, the format for the information of ticket
                """
        info = "PLATSBILJETT\n" + "Tåg-ID: " + train.id + "\n" + train.train_model + "\n" + train.start + " - " + \
               train.destination + "\n" + "Plats " + self.seat + "\n" + "Vagn " + self.coach + "\n" + train.date + "\n" + train.time +\
               "\n" + self.position + "\n" + self.section + "\n\n"

        return info


