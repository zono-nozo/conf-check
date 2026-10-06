CREATE TABLE conferences (
    conference_id INTEGER GENERATED ALWAYS AS IDENTITY,
    conference_name VARCHAR NOT NULL,
    location VARCHAR,
    start_date DATE,
    end_date DATE,
    url VARCHAR NOT NULL,
    checked_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (conference_id)
);
CREATE TABLE deadlines (
    deadline_id INTEGER GENERATED ALWAYS AS IDENTITY,
    conference_id INTEGER NOT NULL,
    deadline_type VARCHAR NOT NULL,
    deadline_date DATE,
    PRIMARY KEY (deadline_id),
    FOREIGN KEY (conference_id) REFERENCES conferences (conference_id)
);
CREATE TABLE change_logs (
    change_log_id INTEGER GENERATED ALWAYS AS IDENTITY,
    deadline_id INTEGER NOT NULL,
    before_date DATE,
    after_date DATE NOT NULL,
    changed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (change_log_id),
    FOREIGN KEY (deadline_id) REFERENCES deadlines (deadline_id)
);