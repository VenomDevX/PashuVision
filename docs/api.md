# REST API Documentation

## `POST /api/v1/predict/`
Analyzes an image and returns the predicted breed.

**Parameters (FormData):**
- `image`: The image file.
- `species_hint`: "auto", "cattle", or "buffalo".

**Response (JSON):**
```json
{
  "species": "Cattle",
  "species_confidence": 99.4,
  "breed": "Gir",
  "breed_confidence": 98.1,
  "image_url": "/static/uploads/image.jpg"
}
```

## `GET /api/v1/scans/`
Returns history of scans.

**Query Params:**
- `skip` (default 0)
- `limit` (default 100)
