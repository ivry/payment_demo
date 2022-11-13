curl -X POST localhost:8000/payment_methods -H 'Content-Type: application/json' -d '{"payment_method_id":"4d39aa4c-09ae-4f2d-adcc-27d02d473524", "name": "internal_balance"}'
curl -X POST localhost:8000/payment_methods -H 'Content-Type: application/json' -d '{"payment_method_id":"7b04d8da-d914-4a76-8700-1e32347cdaab", "name": "debit_card"}'
curl -X POST localhost:8000/payment_methods -H 'Content-Type: application/json' -d '{"payment_method_id":"3c65b6c9-08d6-442a-bfed-9da266bec018", "name": "ach"}'
