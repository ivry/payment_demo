CREATE TABLE IF NOT EXISTS risk_schema.auth_request
(
    auth_request_id   UUID PRIMARY KEY,
    user_id           UUID,
    payee_id          UUID,
    payment_method_id UUID,
    amount            NUMERIC(20, 6),
    currency          VARCHAR(10),
    risk_score        NUMERIC(3),
    created_at        TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
