CREATE TABLE IF NOT EXISTS payment_schema.payment_method
(
    payment_method_id UUID PRIMARY KEY,
    name              VARCHAR(50),
    created_at        TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
