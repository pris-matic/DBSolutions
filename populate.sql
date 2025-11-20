INSERT INTO BUILDING (building_name, building_street, building_district, building_city) VALUES
('Revana Peak', '81st Street', '3rd District', 'Metro City');

INSERT INTO VENUE (venue_ID, venue_name, venue_type, venue_capacity, venue_floor_area, building_ID) VALUES
(2018631, 'Agila Room', 'Meeting room', 22, 30.00, 1);

INSERT INTO AMENITY (amenity_ID, amenity_type, amenity_description) VALUES
(1, 'LCD TV', '45" widescreen Samsung TV LCD screen'),
(2, 'Table', '8ft x 3ft wooden table with glass top'),
(3, 'Chair', 'Micaiah C33 office chair');

INSERT INTO VENUE_AMENITY (venue_ID, amenity_ID, venueamenity_quantity) VALUES
(2018631, 1, 1),
(2018631, 2, 1),  
(2018631, 3, 22);