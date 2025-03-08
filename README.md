# LinkedIn Bot

This LinkedIn bot automates the process of sending connection requests on LinkedIn. It uses Selenium to interact with the LinkedIn website and can run in both headless and visible modes.

## Features

- Automatically logs into LinkedIn using credentials from a `.env` file.
- Searches for people using a specified keyword.
- Sends connection requests to people found in the search results.
- Handles pagination and retries if the next page is not found.
- Saves the current page number to a file to resume from the last processed page.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:

   ```sh
   git clone git@github.com:bruak/linkedn_bot.git
   cd linkedn_bot
   ```

2. Create a `.env` file in the project root with your LinkedIn credentials:

   ````ini
   // filepath: /home/bsoykan/myfolders/linkedn/linkedn_bot/.env
   LINKEDIN_USERNAME=your_linkedin_username
   LINKEDIN_PASSWORD=your_linkedin_password
   ````

3. Build and start the Docker container:

   ```sh
   make up
   ```

## Usage

The bot will automatically start and run in headless mode. It will log into LinkedIn, search for people using the keyword "42", and send connection requests.

### Commands

- Start the bot in the background:

  ```sh
  make up
  ```

- Start the bot services:

  ```sh
  make start
  ```

- Stop the bot:

  ```sh
  make down
  ```

- Stop the bot services (keeping containers):

  ```sh
  make stop
  ```

- Restart the bot:

  ```sh
  make restart
  ```

- Rebuild the bot images:

  ```sh
  make build
  ```

- Show the bot logs:

  ```sh
  make logs
  ```

- Show the bot containers status:

  ```sh
  make ps
  ```

- Remove the bot containers and volumes:

  ```sh
  make clean
  ```

- Full cleanup of the bot (containers, images, volumes):

  ```sh
  make fclean
  ```

- Aggressive Docker system cleanup:

  ```sh
  make f
  ```

## Notes

- The bot saves the current page number to `/app/data/page_number.txt` to resume from the last processed page.
- The bot can be configured to run in visible mode by modifying the `a.py` script.

## License

This project is licensed under the MIT License.
