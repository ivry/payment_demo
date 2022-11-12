CREATE TABLE IF NOT EXISTS payment_schema.payment_request
(
    payment_request_id UUID PRIMARY KEY,
    user_id            UUID,
    payee_id           UUID,
    payment_method_id  UUID,
    amount             NUMERIC(20, 6),
    currency           VARCHAR(10),
    created_at        TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
