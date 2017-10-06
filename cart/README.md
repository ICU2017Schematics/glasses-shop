# Cart - Cart as a Service

Multi-tenant shopping cart service. A cart is defined as a guid, a collection of `lineitems`, and a total. A `lineitem` is an object with the properties:

- `product_id`
- `qty`
- `unit_price`

## RESTful API Patterns

Cart implements a RESTful API based on linked data concepts. Patterns here are not meant to say that clients manipulate the URI for a resource. The URI of a resource is idempotent and opaque.

|Verb|Resource|Description|
|GET|/|returns all carts. Request must have credential indicating is_admin|
|GET|/:id|returns specific cart|
|POST|/:id|add lineitem to cart. Returns the cart|
|PUT|/:id|replace contents of cart|
|DELETE|/:id|delete cart|
