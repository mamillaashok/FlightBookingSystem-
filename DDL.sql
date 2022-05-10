--CREATE Schema 
CREATE SCHEMA coursework2021;

--Set search path
SET SEARCH_PATH TO coursework2021;

--CREATE LeadCustomer table
CREATE TABLE LeadCustomer 
(
CustomerID INTEGER PRIMARY KEY NOT NULL,
FirstName VARCHAR(20) NOT NULL CHECK (FirstName <> ' '),
Surname VARCHAR(40) NOT NULL CHECK (Surname <> ' '),
BillingAddress VARCHAR(200) NOT NULL CHECK (BillingAddress <> ' '),
email VARCHAR(30) NOT NULL CHECK (email <> ' ')
)

--CREATE Passenger table
CREATE TABLE Passenger 
(
PassengerID INTEGER PRIMARY KEY NOT NULL,
FirstName VARCHAR(20) NOT NULL CHECK (FirstName <> ' '),
Surname VARCHAR(40) NOT NULL CHECK (Surname <> ' '),
PassportNo VARCHAR(30) NOT NULL CHECK (PassportNo <> ' '),
Nationality VARCHAR(30) NOT NULL CHECK (Nationality <> ' '),
Dob DATE NOT NULL CHECK (Dob <= CURRENT_DATE) 
)

--CREATE Flight table
CREATE TABLE Flight 
(
FlightID INTEGER PRIMARY KEY NOT NULL,
FlightDate TIMESTAMP NOT NULL CHECK (FlightDate >= CURRENT_DATE) , 
Origin VARCHAR(30) NOT NULL CHECK (Origin <> ' '),
Destination VARCHAR(30) NOT NULL CHECK (Destination <> ' '),
MaxCapacity INTEGER NOT NULL,
PricePerSeat DECIMAL NOT NULL
)

--ALTER Flight table
ALTER TABLE Flight ADD CONSTRAINT check_origin_dest CHECK (Origin <> Destination);

--CREATE FlightBooking table
CREATE TABLE FlightBooking 
(
BookingID INTEGER PRIMARY KEY NOT NULL,
CustomerID INTEGER NOT NULL,
FlightID INTEGER NOT NULL, 
NumSeats INTEGER NOT NULL CHECK (NumSeats >= 1 AND NumSeats <= 4),
Status CHAR(1) DEFAULT 'R' NOT NULL,
BookingTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
TotalCost DECIMAL,
FOREIGN KEY (CustomerID) REFERENCES LeadCustomer ON DELETE RESTRICT ON UPDATE CASCADE,
FOREIGN KEY (FlightID) REFERENCES Flight ON DELETE RESTRICT ON UPDATE CASCADE
)

--ALTER FlightBooking table
ALTER TABLE FlightBooking ADD CONSTRAINT check_status CHECK (Status IN ('R', 'C') );

--CREATE SeatBooking table
CREATE TABLE SeatBooking
(
BookingID INTEGER NOT NULL,
PassengerID INTEGER NOT NULL,
SeatNumber CHAR(4),
PRIMARY KEY(BookingID, PassengerID),
FOREIGN KEY (BookingID) REFERENCES FlightBooking ON DELETE CASCADE ON UPDATE CASCADE
)

--Trigger for Task D before deleting customer from table
CREATE FUNCTION remove_customer() RETURNS TRIGGER AS $remove_customer$
	DECLARE 
        cust_status integer;
    BEGIN
		SELECT count(*) FROM FlightBooking WHERE CustomerID = OLD.CustomerID AND Status = 'R' INTO cust_status;
		IF cust_status > 0 THEN
			RAISE EXCEPTION 'There are active bookings for the given customer.';
		ELSE
			DELETE FROM FlightBooking WHERE CustomerID = OLD.CustomerID;
		END IF;
		RETURN OLD;
	END;
$remove_customer$ LANGUAGE plpgsql;

--Invocation of remove_customer trigger
CREATE TRIGGER remove_customer BEFORE DELETE ON LeadCustomer
    FOR EACH ROW EXECUTE PROCEDURE remove_customer();

--View for Task P to check availability of seats on all flights
CREATE VIEW seat_availability AS
SELECT DISTINCT f.FlightID, f.FlightDate, destination,
COALESCE((SELECT sum(NumSeats) FROM FlightBooking WHERE Status = 'R' and flightid = f.flightid GROUP BY flightId),0) AS "Booked Seats",
COALESCE((SELECT sum(NumSeats) FROM FlightBooking WHERE Status = 'C' and flightid = f.flightid GROUP BY flightId), 0) AS "Cancelled Seats",
COALESCE((maxcapacity-COALESCE((SELECT sum(NumSeats) FROM FlightBooking WHERE Status = 'R' and flightid = f.flightid GROUP BY flightId),0)))
AS "Available Seats", MaxCapacity AS "Maximum Capacity"
FROM Flight AS f LEFT JOIN FlightBooking fb ON fb.flightid = f.flightid;

--View for Task R to produce ranked list of lead customers
CREATE VIEW customer_rank AS
SELECT lc.CustomerID, CONCAT(firstname, ' ', surname) AS fullname, COALESCE(SUM(numseats), 0) AS totalbookings, COALESCE(SUM(totalcost), 0) AS TotalSpend 
FROM LeadCustomer lc LEFT JOIN FlightBooking fb ON lc.CustomerID = fb.CustomerID GROUP BY lc.CustomerID ORDER BY TotalSpend DESC;

--Trigger for Task S before inserting into SeatBooking table to check if seats are already booked
CREATE FUNCTION seat_allocation() RETURNS TRIGGER AS $seat_allocation$
	DECLARE 
        seat_count integer;
    BEGIN
		SELECT count(*) FROM SeatBooking WHERE BookingID = NEW.BookingID INTO seat_count;
		IF seat_count = (SELECT NumSeats FROM FlightBooking WHERE BookingID = NEW.BookingID) THEN
			RAISE EXCEPTION 'Number of seats allocated for the flight are already booked.';
		END IF;
		RETURN NEW;
	END;
$seat_allocation$ LANGUAGE plpgsql;

--Invocation of seat_allocation trigger
CREATE TRIGGER seat_allocation BEFORE INSERT ON SeatBooking
    FOR EACH ROW EXECUTE PROCEDURE seat_allocation();
	
--Function for Task T
CREATE OR REPLACE FUNCTION flight_booking(customer_id integer, first_name text, sur_name text, billing_address text, email text, 
								booking_id integer, flight_id integer, num_seats integer, status char) RETURNS VOID AS $flight_booking$
    BEGIN
		IF customer_id IN (SELECT CustomerID FROM LeadCustomer) AND first_name IN (SELECT FirstName FROM LeadCustomer WHERE CustomerID = customer_id)  THEN
			INSERT INTO FlightBooking VALUES (booking_id, customer_id, flight_id, num_seats, status, NOW(), (SELECT PricePerSeat FROM Flight WHERE FlightID = flight_id) * num_seats);
		ELSEIF first_name IS NULL THEN
			RAISE EXCEPTION 'Flight booking is Cancelled as insertion failed';
		ELSE
			INSERT INTO LeadCustomer VALUES (customer_id, first_name, sur_name, billing_address, email);
			INSERT INTO FlightBooking VALUES (booking_id, customer_id, flight_id, num_seats, status, NOW(), (SELECT PricePerSeat FROM Flight WHERE FlightID = flight_id) * num_seats);
		END IF;
		EXCEPTION  
  			WHEN OTHERS THEN 
    	BEGIN 
    		RAISE EXCEPTION 'Flight booking is Cancelled as insertion failed';
  		END;
	END;
$flight_booking$ LANGUAGE plpgsql;