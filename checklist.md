# Development Plan: PriceQuake

## Project Structure & Setup

 - ~~Set up GitHub repo with proper .gitignore~~

 - ~~Set up Python project in PyCharm with correct interpreter~~

 - ~~Dockerized PostgreSQL database is running and accessible~~

 - ~~Database schema created (stocks, users, watchlist, notifications)~~


## Server Application (Backend)

 - Handle incoming client connections via socket

 - Parse and validate client requests (e.g., subscribe to stock, view price)

 - Fetch stock prices (from real API or mock for now)

 - Connect to PostgreSQL database and:

   - Authenticate user credentials

   - Store/retrieve watchlist items

   - Store notification settings

 - Trigger email notifications (SMTP) when stock prices hit thresholds

 - Handle multiple clients (threading or asyncio)


## Client Application (Frontend)

 - Build GUI using Tkinter

 - User login/register

 - Search/add stocks to watchlist

 - Set price alerts

 - View current prices and notification status

 - Connect to server and send/receive requests over socket

 - Display responses in GUI (use threading to avoid freezing)



## Email Notification System

 - Set up SMTP (e.g., Gmail or other provider)

 - Format email content (stock symbol, current price, threshold hit)

 - Integrate with server logic when price triggers are hit



## Testing

 - Unit tests for database interaction code

 - Integration tests (client ↔ server ↔ DB)

 - Manual GUI testing

 - Simulate multiple users and edge cases



## Final Touches

 - Polish GUI (error handling, loading indicators, UI tweaks)

 - Write usage instructions in README.md

 - Record short demo video or screenshots (optional but great for portfolio)

 - Add Docker Compose setup if needed to simplify running services