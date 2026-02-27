CREATE TYPE status_type AS ENUM('submitted', 'denied', 'ready', 'in_progress', 'done');

CREATE TABLE IF NOT EXISTS location (
    id SERIAL NOT NULL PRIMARY KEY,
    location_name VARCHAR(250) NOT NULL,
    address VARCHAR,
    city VARCHAR(25),
    state VARCHAR(2),
    zip VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    price DOUBLE PRECISION,
    description VARCHAR,
    link VARCHAR,
    craft VARCHAR(100),
    kids BOOLEAN,
    location_id INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    business VARCHAR(250) NOT NULL,
    approved BOOLEAN NOT NULL DEFAULT FALSE,
    submitted_by VARCHAR NOT NULL,
    CONSTRAINT fk_location
        FOREIGN KEY (location_id)
        REFERENCES location(id)
);

CREATE TABLE IF NOT EXISTS user_submitted_event (
    id SERIAL PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    price DOUBLE PRECISION,
    description VARCHAR,
    link VARCHAR,
    craft VARCHAR(100),
    kids BOOLEAN,
    location_name VARCHAR(250) NOT NULL,
    address VARCHAR,
    city VARCHAR(25),
    state VARCHAR(2),
    zip VARCHAR(10),
    date DATE NOT NULL,
    time TIME NOT NULL,
    business VARCHAR(250) NOT NULL,
    approved BOOLEAN NOT NULL DEFAULT FALSE,
    email VARCHAR(100) NOT NULL,
    date_submitted DATE NOT NULL,
    status status_type NOT NULL DEFAULT 'submitted',
    note VARCHAR(250)
);

ALTER TABLE user_submitted_event
ADD CONSTRAINT unique_event_name_link_date
UNIQUE (name, link, date);

INSERT INTO location (location_name, address, city, state, zip) VALUES
    ('Community Center', '123 Main St', 'Seattle', 'WA', '98101'),
    ('Art Studio Downtown', '456 Art Ave', 'Portland', 'OR', '97201'),
    ('Creative Space', '789 Maker Blvd', 'Austin', 'TX', '78701');

INSERT INTO event (name, price, description, link, craft, kids, location_id, date, time, business, approved, submitted_by) VALUES
    ('Pottery Workshop', 45.00, 'Learn basic pottery techniques', 'https://example.com/pottery', 'pottery', true, 1, '2026-02-15', '14:00:00', 'Clay Masters', true, 'admin@example.com'),
    ('Painting Class', 35.00, 'Beginner watercolor painting', 'https://example.com/painting', 'painting', true, 2, '2026-02-20', '10:00:00', 'Art Studio Downtown', true, 'admin@example.com'),
    ('Woodworking 101', 60.00, 'Introduction to woodworking', 'https://example.com/wood', 'woodworking', false, 3, '2026-03-01', '09:00:00', 'Makers Guild', false, 'user@example.com');

INSERT INTO user_submitted_event (name, price, description, link, craft, kids, location_name, date, time, business, email, date_submitted) VALUES
    ('Pottery Workshop', 45.00, 'Learn basic pottery techniques', 'https://example.com/pottery', 'pottery', true, 'test location', '2026-02-15', '14:00:00', 'Test Business', 'test@example.com', '2026-02-03');
