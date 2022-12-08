CREATE DATABASE godelv;
use godelv;

CREATE TABLE Carrier(carrierID varchar(10),
					carrierName varchar(500),
                    CONSTRAINT PK_Carrier PRIMARY KEY(carrierID, carrierName)
					);
CREATE TABLE DeliveryService(deliveryServiceName varchar(500),
							carrierID varchar(10),
							carrierName varchar(500),
							dimension varchar(20),
							price float(10, 2),
							CONSTRAINT PK_DeliveryService PRIMARY KEY(deliveryServiceName, carrierID)
);

CREATE TABLE Login(email varchar(50),
				   username varchar(50),
                   password varchar(500),
                   userType varchar(50),
                   otpSecret varchar(50),
                   CONSTRAINT PK_Login PRIMARY KEY(email)
                  );

CREATE TABLE Customer(email varchar(50),
                      firstName varchar(50),
                      lastName varchar(50),
                      dateOfBirth varchar(50),
                      mobileNo varchar(10),
                      CONSTRAINT PK_Customer PRIMARY KEY(email)
                     );

CREATE TABLE Administrator(email varchar(50),
                      firstName varchar(50),
                      lastName varchar(50),
                      dateOfBirth varchar(50),
                      mobileNo varchar(10),
                      carrierID varchar(10),
                      CONSTRAINT PK_Administrator PRIMARY KEY(email),
                      CONSTRAINT FK_Administrator_carrierID FOREIGN KEY (carrierID) REFERENCES Carrier(carrierID) ON DELETE CASCADE
                     );


CREATE TABLE DeliveryDriver(email varchar(50),
					  deliveryManagerID varchar(50),
                      firstName varchar(50),
                      lastName varchar(50),
                      dateOfBirth varchar(50),
                      mobileNo varchar(10),
                      isEngage varchar(10) DEFAULT 'FALSE',
                      carrierID varchar(10),
                      CONSTRAINT PK_DeliveryDriver PRIMARY KEY(email, deliveryManagerID),
                      CONSTRAINT FK_DeliveryDriver_carrierID FOREIGN KEY (carrierID) REFERENCES Carrier(carrierID)

                     );

CREATE TABLE Shippment (SID varchar(50),
						fname varchar(200),
                        faddress varchar(200),
                        fapartment varchar(200),
                        fzip varchar(6),
                        fcity varchar(200),
                        fstate varchar(200),
                        fmobileNo varchar(10),
                        femail varchar(50),

                        rname varchar(200),
                        raddress varchar(200),
                        rapartment varchar(200),
                        rzip varchar(6),
                        rcity varchar(200),
                        rstate varchar(200),
                        rmobileNo varchar(10),
                        remail varchar(50),

                        carrierName varchar(500),
                        deliveryServiceName varchar(500),
                        dimension varchar(20),
                        price float(10, 2),
                        weight float(10, 2),
                        deliveryDriverID varchar(50),
                        customerID varchar(50),
                        CONSTRAINT PK_Shippment PRIMARY KEY(SID)                        
);
CREATE TABLE Tracking (TID varchar(50),
						deliveryStatus varchar(200),
                        address varchar(200),
                        apartment varchar(200),
                        zip varchar(6),
                        city varchar(200),
                        state varchar(200),
                        CONSTRAINT PK_Tracking PRIMARY KEY(TID)
);

INSERT INTO Carrier(carrierID, carrierName) VALUES
('101', 'FedEx'),
('102', 'USPS'),
('103', 'DHL'),
('104', 'UPS'),
('105', 'APL'),
('106', 'C.H.Robinson'),
('107', 'Hyundai Glovis');
