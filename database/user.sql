CREATE TABLE IF NOT EXISTS payment_schema.user
(
    user_id    UUID PRIMARY KEY,
    first_name VARCHAR(50),
    last_name  VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
