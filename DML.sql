--Task A
INSERT INTO LeadCustomer (CustomerID, FirstName, Surname, BillingAddress, email) VALUES (101, 'Rana', 'Pratap', '38 The Street, Reading', 'rana.p@gmail.com');

--Task B
INSERT INTO Passenger (PassengerID, FirstName, Surname, PassportNo, Nationality, Dob) VALUES (201, 'David', 'Smith', '32781883', 'British', '30/01/1986');

--Task C
INSERT INTO Flight (FlightID, FlightDate, Origin, Destination, MaxCapacity, PricePerSeat) VALUES (4001, '29/07/2022', 'STN', 'BHD', 100, 70);

--Task D
DELETE FROM LeadCustomer WHERE CustomerID = 101;

--Task P
SELECT * FROM seat_availability;

--Task Q
SELECT FlightID, "Reserved Seats" FROM seat_availability WHERE FlightID = 4001;

--Task R
SELECT * FROM customer_rank;

--Task S
INSERT INTO SeatBooking values(500,1001,'1A');

--Task T
SELECT * FROM LeadCustomer WHERE CustomerID = 12;
SELECT flight_booking(12, null, null, null, null, 513, 103, 2, 'R');

SELECT flight_booking(9, 'Dan', 'Sayers', '9a Morley Lane, Southampton', 'D.Smith@hotmail.com', 514, 103, 3, 'R');

SELECT flight_booking(13, ‘Ben’, ' Morgan', ‘1 The Street, Norwich', 'b.morgan@hotmail.com', 515, 103, 3, 'R');

SELECT flight_booking(14, 'Peter', 'Brown', '3a Hill Street, Southampton', 'P.Brown@hotmail.com', 516, 104, 2, 'R');
--Task U
SELECT * FROM Passenger AS p WHERE p.PassengerID NOT IN (SELECT s.PassengerID FROM SeatBooking s);

--Task V
SELECT * FROM SeatBooking;

--Task Y
SELECT * FROM FlightBooking;

--Task W
SELECT COUNT(*) AS "Allocated Seats" FROM SeatBooking WHERE BookingID = 101;
UPDATE FlightBooking SET Status = 'C' WHERE BookingID = 101;