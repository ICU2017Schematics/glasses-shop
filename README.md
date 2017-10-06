# Cloud University 2017 - Schematics Sample App

Demo application for the Cloud Schematics Hands On Lab @ Cloud University 2017.

## Status

- `docker-compose.yml` script set up for local execution
- `session-id` and overall cart handling needs to be redone but it currently minimally functions
- `docker-build-lab.sh` creates docker images on public dockerhub

## TODO

## Scenario

This is an ecommerce application consisting of 5 services:

- Catalog                                                         (Port: 5001)
- Shopping Cart / Checkout                                        (Port: 5002)
- UI                                                              (Port: 8080)
- Gateway service routing to individual microservices             (Port: 5000)
- Fulfillment                                                     (Port: 3000)

The application demonstrates the use of Schematics to deploy/manage IBM Cloud infrastructure of:

- Containers cluster
- Cloudant (DB as a Bluemix service)
- Scale Group of virtual machines
