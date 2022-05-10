--Task A
INSERT INTO LeadCustomer (CustomerID, FirstName, Surname, BillingAddress, email) VALUES (110, 'Rana', 'Pratap', '38 Lincoln Street, Reading', 'rana.p@gmail.com');

--Task B
INSERT INTO Passenger (PassengerID, FirstName, Surname, PassportNo, Nationality, Dob) VALUES (125, 'David', 'Smith', 'sw081883', 'British', '30/01/1986');

--Task C
INSERT INTO Flight (FlightID, FlightDate, Origin, Destination, MaxCapacity, PricePerSeat) VALUES (208, '29/06/2022', 'BRC', 'LON', 12, 70);

--Task D
DELETE FROM LeadCustomer WHERE CustomerID = 110;

--Task P
SELECT * FROM seat_availability;

--Task P1
SELECT * FROM seat_availability WHERE FlightID = 204;

--Task P2
SELECT * FROM seat_availability WHERE Destination = 'BIR';

--Task P3
SELECT * FROM seat_availability WHERE FlightDate = '2022-09-30';

--Task Q
SELECT * FROM seat_availability WHERE FlightID = 201;

--Task R
SELECT * FROM customer_rank;

--Task T
SELECT flight_booking(114, 'Ben', 'Morgan', '1 The Street, Norwich', 'b.morgan@hotmail.com', 1040, 208, 2, 'R');

--Task T1
SELECT * FROM LeadCustomer;

--Task T2
SELECT * FROM FlightBooking;

--Task U
SELECT * FROM Passenger AS p WHERE p.PassengerID NOT IN (SELECT s.PassengerID FROM SeatBooking s);

--Task S
INSERT INTO SeatBooking values(1006,125,'1A');

--Task V
SELECT * FROM SeatBooking;

--Task W1
SELECT COUNT(*) AS "Allocated Seats" FROM SeatBooking WHERE BookingID = 1004;

--Task W2
UPDATE FlightBooking SET Status = 'C' WHERE BookingID = 1004;

--Task Y
SELECT * FROM FlightBooking;