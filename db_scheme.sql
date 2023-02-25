CREATE TYPE "states" AS ENUM (
  'created',
  'formed',
  'in_delivery',
  'received'
);

CREATE TABLE "genres" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE "authors" (
  "id" SERIAL PRIMARY KEY,
  "first_name" VARCHAR(100) NOT NULL,
  "second_name" VARCHAR(100) NOT NULL,
  "surname" VARCHAR(100)
);

CREATE TABLE "publishers" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE "books" (
  "id" SERIAL PRIMARY KEY,
  "isbn" VARCHAR,
  "title" VARCHAR(100) NOT NULL,
  "publication_date" DATE,
  "available_quantity" INT NOT NULL DEFAULT 0,
  "price" "NUMERIC(6, 2)",
  "author" SERIAL,
  "publisher" SERIAL
);

CREATE TABLE "books_genres" (
  "book_id" VARCHAR,
  "genre_id" SERIAL,
  PRIMARY KEY ("book_id", "genre_id")
);

CREATE TABLE "customers" (
  "id" SERIAL PRIMARY KEY,
  "first_name" VARCHAR(100) NOT NULL,
  "last_name" VARCHAR(100) NOT NULL,
  "surname" VARCHAR(100),
  "login" VARCHAR(100) UNIQUE NOT NULL,
  "passwordHash" VARCHAR(100),
  "postal_code" VARCHAR(6) NOT NULL,
  "street" VARCHAR(100) NOT NULL,
  "building_no" VARCHAR(5) NOT NULL,
  "flat_no" VARCHAR(5),
  "city" VARCHAR(100) NOT NULL,
  "phone_number" VARCHAR(9)
);

CREATE TABLE "orders" (
  "id" SERIAL PRIMARY KEY,
  "customer_id" SERIAL NOT NULL,
  "date" DATE DEFAULT (now()),
  "shipper" BIGINT NOT NULL,
  "state" states
);

CREATE TABLE "shippers" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(100) NOT NULL,
  "phone_number" VARCHAR(9),
  "price" "NUMERIC(6, 2)" DEFAULT 0
);

CREATE TABLE "carts" (
  "id" SERIAL PRIMARY KEY,
  "customer_id" integer
);

CREATE TABLE "carts_products" (
  "cart_id" integer,
  "book_id" integer
);

CREATE TABLE "images" (
  "id" SERIAL PRIMARY KEY
);

CREATE TABLE "books_images" (
  "image_id" SERIAL,
  "book_id" SERIAL
);

ALTER TABLE "books" ADD FOREIGN KEY ("author") REFERENCES "authors" ("id") ON DELETE CASCADE;

ALTER TABLE "books" ADD FOREIGN KEY ("publisher") REFERENCES "publishers" ("id") ON DELETE CASCADE;

ALTER TABLE "books_genres" ADD FOREIGN KEY ("book_id") REFERENCES "books" ("id");

ALTER TABLE "books_genres" ADD FOREIGN KEY ("genre_id") REFERENCES "genres" ("id");

ALTER TABLE "orders" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") ON DELETE CASCADE;

ALTER TABLE "orders" ADD FOREIGN KEY ("shipper") REFERENCES "shippers" ("id") ON DELETE CASCADE;

ALTER TABLE "carts" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") ON DELETE CASCADE;

ALTER TABLE "carts_products" ADD FOREIGN KEY ("cart_id") REFERENCES "carts" ("id") ON DELETE CASCADE;

ALTER TABLE "carts_products" ADD FOREIGN KEY ("book_id") REFERENCES "books" ("id") ON DELETE CASCADE;

ALTER TABLE "books_images" ADD FOREIGN KEY ("image_id") REFERENCES "images" ("id") ON DELETE CASCADE;

ALTER TABLE "books_images" ADD FOREIGN KEY ("book_id") REFERENCES "books" ("id") ON DELETE CASCADE;
