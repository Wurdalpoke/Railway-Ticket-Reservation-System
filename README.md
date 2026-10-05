# Railway Reservation System

A console-based train reservation system built with **Python** and **MySQL**. Passengers can search trains by route, see departure and arrival timings along with the seats left, book a ticket, cancel it, and view their bookings.

This project was originally built as a Class XII Computer Science (083) school project and later improved with a normalized database design and transaction-safe booking.

## Features

- Search trains by departure and destination, with **departure/arrival timings** and **seats left**
- Book a ticket on any train that has at least one empty seat (**first come, first served**, no seat numbers)
- Cancel a booking, which frees the seat for others
- View all active bookings using a phone number
- Input validation (10-digit phone numbers, valid Train IDs)
- Safe handling of simultaneous bookings, so the last seat can never be booked twice
- Parameterized SQL queries (protects against SQL injection)

## Tech Stack

- Python 3.6+
- MySQL 8.x (also works with MariaDB)
- `mysql-connector-python`

## Database Design

The schema is normalized into three tables:

| Table | Purpose | Key columns |
|---|---|---|
| `trains` | One row per train | `train_id` (PK), `train_name`, `start_point`, `end_point`, `start_time`, `end_time`, `total_seats` |
| `passengers` | One row per person | `phone` (PK), `name` |
| `bookings` | One row per ticket | `ticket_id` (PK, auto-increment), `train_id` (FK), `phone` (FK), `booked_at`, `status` (`CONFIRMED` / `CANCELLED`) |

Seats left on a train = `total_seats` - number of `CONFIRMED` bookings on that train. Cancelled tickets stay on record with status `CANCELLED`.

## How Booking Stays Consistent

Booking runs inside a database transaction. The train's row is locked (`SELECT ... FOR UPDATE`), the seats are counted, and the ticket is inserted only if a seat is free. If anything fails, the transaction is rolled back and nothing is saved.

## Setup and Run

1. **Install MySQL Server** and remember your root password.
2. **Install the Python connector:**
   ```
   pip install -r requirements.txt
   ```
3. **Create the database.** Run `railway_schema.sql` in MySQL Workbench (open it in a SQL editor and execute all), or from the command line:
   ```
   mysql -u root -p < railway_schema.sql
   ```
   This creates the `railway_reservation` database, the three tables and some sample trains. Running it again resets all data.
4. **Set your password.** Open `railway_reservation_simple.py` and replace `your_password` with your MySQL root password. Do not commit your real password.
5. **Run the program:**
   ```
   python railway_reservation_simple.py
   ```

## Sample Run

Try the route **Guwahati to Delhi** with the sample data. The program lists matching trains with timings and seats left, for example:

```
Train ID  Name                 Departure          Arrival            Seats left
--------------------------------------------------------------------------------
100234    Rajdhani Express     20-Oct-2026 06:30 21-Oct-2026 09:45 3
101252    Northeast Express    20-Oct-2026 14:15 22-Oct-2026 03:10 5
234587    Brahmaputra Mail     21-Oct-2026 20:00 23-Oct-2026 08:30 2
```

## Project Files

| File | Description |
|---|---|
| `railway_reservation_simple.py` | The Python program (menu, booking, cancelling) |
| `railway_schema.sql` | Database schema and sample data |
| `requirements.txt` | Python dependency |

## Limitations

- Tickets are tied to a train, not to specific seat numbers
- No payment or refund handling
- Console-only interface (no web or GUI front end)
- No user login; a passenger is identified by phone number

## Possible Improvements

- Seat numbers and coach classes
- Fare calculation and payments
- A GUI (Tkinter) or web interface (Flask)
- Admin login for adding and removing trains

## Author

Your Name, Class XII, Manav Rachna International School, Noida
