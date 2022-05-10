import psycopg2
import pandas as pd
import os


def getConn():
    # Function to retrieve the password, construct
    # the connection string, make a connection and return it.

    pwFile = open("pw.txt", "r")
    pw = pwFile.read()
    pwFile.close()
    connStr = "host='cmpstudb-01.cmp.uea.ac.uk' \
               dbname= 'aak21xqu' user='aak21xqu' password = " + pw
    print(pw)
    conn = psycopg2.connect(connStr)
    return conn


def writeOutput(output):
    with open("output.txt", "a") as myfile:
        myfile.write(output)


try:
    conn = None
    conn = getConn()
    cur = conn.cursor()

    with open("input.txt", "r") as file:
        task = file.readline()
        cnt = 1
        while task:
            if (task.strip() == 'B'):
                data = next(file)
                d = data.split(',')
                try:
                    data = [d[0], d[1], d[2], d[3], d[4], d[5]]
                    cur.execute("SET SEARCH_PATH to coursework2021;")
                    cur.execute("SET datestyle='ISO, DMY';")
                    # SQL query to insert data into Passenger table
                    sql = "INSERT INTO Passenger (PassengerID, FirstName, Surname, PassportNo, Nationality, Dob) VALUES(%s, %s, %s, %s, %s, %s);"
                    cur.execute(sql, data)
                    conn.commit()
                    # SQL query to fetch the inserted record from Passenger table
                    cur.execute('SELECT * FROM Passenger WHERE PassengerID = %s', [d[0]])
                    rows = cur.fetchall()
                    writeOutput("B\n")
                    for row in rows:
                        for item in row:
                            print(item, ", ", end='')
                            s = str(item) + ", \n"
                            writeOutput(s)
                        print()
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("B\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n")
            elif (task.strip() == 'C'):
                data = next(file)
                d = data.split(',')
                try:
                    data = [d[0], d[1], d[2], d[3], d[4], d[5]]
                    cur.execute("SET SEARCH_PATH to coursework2021;")
                    cur.execute("SET datestyle='ISO, DMY';")
                    # SQL query to insert data into Flight table
                    sql = "INSERT INTO Flight (FlightID, FlightDate, Origin, Destination, MaxCapacity, PricePerSeat) VALUES(%s, %s, %s, %s, %s, %s);"
                    cur.execute(sql, data)
                    conn.commit()
                    # SQL query to fetch the inserted record from Flight table
                    cur.execute('SELECT * FROM Flight WHERE FlightID = %s', [d[0]])
                    rows = cur.fetchall()
                    writeOutput("C\n")
                    for row in rows:
                        for item in row:
                            print(item, ", ", end='')
                            s = str(item) + ", \n"
                            writeOutput(s)
                        print()
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("C\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'D'):
                data = next(file)
                d = data.split(',')
                try:
                    cur.execute("SET SEARCH_PATH to coursework2021;")
                    customer_id = int(d[0])
                    cur.execute('DELETE FROM LeadCustomer where CustomerID = %s', [customer_id])
                    conn.commit()
                    writeOutput("D\n")
                    writeOutput(f'Customer with customer id {customer_id} has been deleted')
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("D\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'P'):
                try:
                    cur.execute("SET SEARCH_PATH to coursework2021;")
                    cur.execute("SELECT * FROM seat_availability;")
                    rows = cur.fetchall()
                    seats = pd.DataFrame(rows, columns=['FlightID', 'FlightDate', 'Destination', 'Booked Seats',
                                                        'Cancelled Seats', 'Available Seats', 'Maximum Capacity'])
                    print(seats)
                    seats_str = seats.to_string(header=True, index=False)
                    writeOutput("P\n")
                    writeOutput(seats_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("P\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'P1'):
                data = next(file)
                d = data.split(',')
                try:
                    cur.execute("SET SEARCH_PATH to coursework2021;")
                    cur.execute('SELECT * FROM seat_availability WHERE FlightID = %s', [d[0]])
                    rows = cur.fetchall()
                    seats = pd.DataFrame(rows, columns=['FlightID', 'FlightDate', 'Destination', 'Booked Seats',
                                                        'Cancelled Seats', 'Available Seats', 'Maximum Capacity'])
                    print(seats)
                    seats_str = seats.to_string(header=True, index=False)
                    writeOutput("P1\n")
                    writeOutput(seats_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("P1\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'P2'):
                data = next(file)
                try:
                    cur.execute("SET SEARCH_PATH to coursework2021;")
                    cur.execute('SELECT * FROM seat_availability WHERE destination = %s', [data.strip()])
                    rows = cur.fetchall()
                    seats = pd.DataFrame(rows, columns=['FlightID', 'FlightDate', 'Destination', 'Booked Seats',
                                                        'Cancelled Seats', 'Available Seats', 'Maximum Capacity'])
                    print(seats)
                    seats_str = seats.to_string(header=True, index=False)
                    writeOutput("P2\n")
                    writeOutput(seats_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("P2\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'P3'):
                data = next(file)
                d = data.split(',')
                try:
                    cur.execute("SET SEARCH_PATH to coursework2021;")
                    cur.execute('SELECT * FROM seat_availability WHERE FlightDate = %s', [d[0]])
                    rows = cur.fetchall()
                    seats = pd.DataFrame(rows, columns=['FlightID', 'FlightDate', 'Destination', 'Booked Seats',
                                                        'Cancelled Seats', 'Available Seats', 'Maximum Capacity'])
                    print(seats)
                    seats_str = seats.to_string(header=True, index=False)
                    writeOutput("P3\n")
                    writeOutput(seats_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("P3\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'Q'):
                data = next(file)
                try:
                    cur.execute("SET SEARCH_PATH to coursework2021;")
                    cur.execute('SELECT * FROM seat_availability WHERE FlightID = %s', [data.strip()])
                    rows = cur.fetchall()
                    seats = pd.DataFrame(rows, columns=['FlightID', 'FlightDate', 'Destination', 'Booked Seats',
                                                        'Cancelled Seats', 'Available Seats', 'Maximum Capacity'])
                    print(seats)
                    seats_str = seats.to_string(header=True, index=False)
                    writeOutput("Q\n")
                    writeOutput(seats_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("Q\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'R'):
                try:
                    cur.execute('SELECT * FROM coursework2021.customer_rank;')
                    rows = cur.fetchall()
                    cust_ranks = pd.DataFrame(rows,
                                              columns=['CustomerID', 'Full Name', 'Total bookings', 'Total Spend'])
                    print(cust_ranks)
                    cust_ranks_str = cust_ranks.to_string(header=True, index=False)
                    writeOutput("R\n")
                    writeOutput(cust_ranks_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("R\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'S'):
                data = next(file)
                d = data.split(',')
                try:
                    data = [d[0], d[1], d[2]]
                    cur.execute("SET SEARCH_PATH to coursework2021;")
                    # SQL query to insert data into SeatBooking table
                    sql = "INSERT INTO SeatBooking (BookingID, PassengerID, SeatNumber) VALUES(%s, %s, %s);"
                    cur.execute(sql, data)
                    conn.commit()
                    # SQL query to fetch the inserted record from SeatBooking table
                    cur.execute('SELECT * FROM SeatBooking')
                    rows = cur.fetchall()
                    writeOutput("S\n")
                    for row in rows:
                        for item in row:
                            print(item, ", ", end='')
                            s = str(item) + ", \n"
                            writeOutput(s)
                        print()
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("S\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n")
            elif (task.strip() == 'T'):
                try:
                    data = next(file)
                    d = data.split(':')
                    c_data = d[0]
                    f_data = d[1]
                    lc = c_data.split(',')
                    fl = f_data.split(',')
                    cur.execute("SET SEARCH_PATH to coursework2021;")
                    data = [lc[0], lc[1], lc[2], lc[3] + ',' + lc[4], lc[5], fl[0], fl[2], fl[3], fl[4]]
                    # SQL query to insert data into Flight table
                    sql = "SELECT flight_booking(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    cur.execute(sql, data)
                    conn.commit()
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("T\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n")
            elif (task.strip() == 'T1'):
                try:
                    cur.execute('SELECT * FROM coursework2021.LeadCustomer;')
                    rows = cur.fetchall()
                    customers = pd.DataFrame(rows,
                                             columns=['CustomerID', 'First Name', 'Surname', 'BillingAddress', 'email'])
                    print(customers)
                    customers_str = customers.to_string(header=True, index=False)
                    writeOutput("T1\n")
                    writeOutput(customers_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("T1\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'T4'):
                try:
                    cur.execute('SELECT * FROM coursework2021.FlightBooking;')
                    rows = cur.fetchall()
                    flight_bookings = pd.DataFrame(rows,
                                                   columns=['BookingID', 'CustomerID', 'FlightID', 'Number of Seats',
                                                            'Status', 'Booking Time', 'Total Cost'])
                    print(flight_bookings)
                    flight_bookings_str = flight_bookings.to_string(header=True, index=False)
                    writeOutput("T4\n")
                    writeOutput(flight_bookings_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("T4\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'U'):
                try:
                    cur.execute(
                        'SELECT * FROM coursework2021.Passenger AS p WHERE p.PassengerID NOT IN (SELECT s.PassengerID FROM SeatBooking s);')
                    rows = cur.fetchall()
                    p_list = pd.DataFrame(rows,
                                          columns=['PassengerID', 'First Name', 'Surname', 'BillingAddress', 'email'])
                    print(p_list)
                    p_list_str = p_list.to_string(header=True, index=False)
                    writeOutput("U\n")
                    writeOutput(p_list_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("U\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'V'):
                try:
                    cur.execute("SELECT * FROM coursework2021.SeatBooking")
                    rows = cur.fetchall()
                    booked_seats = pd.DataFrame(rows, columns=['BookingID', 'PassengerID', 'SeatNumber'])
                    print(booked_seats)
                    booked_seats_str = booked_seats.to_string(header=True, index=False)
                    writeOutput("V\n")
                    writeOutput(booked_seats_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("V\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'W1'):
                data = next(file)
                d = data.split(',')
                try:
                    booking_id = int(d[0])
                    cur.execute(
                        'SELECT COUNT(*) AS "Allocated Seats" FROM coursework2021.SeatBooking WHERE BookingID = %s',
                        [booking_id])
                    rows = cur.fetchall()
                    booked_seats = pd.DataFrame(rows, columns=['Allocated Seats'])
                    print(booked_seats)
                    booked_seats_str = booked_seats.to_string(header=True, index=False)
                    writeOutput("W1\n")
                    writeOutput(booked_seats_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("W1\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'W2'):
                data = next(file)
                d = data.split(',')
                try:
                    booking_id = int(d[0])
                    cur.execute('UPDATE coursework2021.FlightBooking SET Status = \'C\' WHERE BookingID = %s',
                                [booking_id])
                    conn.commit()
                    cur.execute('SELECT * FROM coursework2021.FlightBooking WHERE BookingID = %s', [booking_id])
                    if cur.rowcount == 0:
                        writeOutput("W2\n")
                        writeOutput(f"No entry found with the given Booking ID: {booking_id}")
                        writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("W2\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'Y'):
                try:
                    cur.execute("SELECT * FROM coursework2021.FlightBooking")
                    rows = cur.fetchall()
                    flight_bookings = pd.DataFrame(rows,
                                                   columns=['BookingID', 'CustomerID', 'FlightID', 'Number of Seats',
                                                            'Status', 'BookingTime', 'TotalCost'])
                    print(booked_seats)
                    flight_bookings_str = flight_bookings.to_string(header=True, index=False)
                    writeOutput("Y\n")
                    writeOutput(flight_bookings_str)
                    writeOutput("\n\n")
                except Exception as e:
                    cur.execute("ROLLBACK")
                    conn.commit()
                    print(e)
                    writeOutput("Y\n")
                    writeOutput(str(e.args[0]))
                    writeOutput("\n\n")
            elif (task.strip() == 'X'):
                if conn:
                    conn.close()
                print("Exit {}".format(d[0]))
                writeOutput("X\n")
                writeOutput("Flight Booking program closing down!")
            task = file.readline()
            cnt += 1
except Exception as e:
    print(e)

