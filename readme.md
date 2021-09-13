### Setup

Create `paku/paku/secrets.py`.

Fill with following content:

New `SECRET_KEY` can be generated with:
` django.core.management.utils.get_random_secret_key()`

```
  # put your django SECRET_KEY here
  secret_key = "abc123"
```

Run:

`pip install opencv-python`

`python manage.py runserver`

Add setting profile in
http://127.0.0.1:8000/admin/
