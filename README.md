# FatEar Web Application

Live Demo: [FatEar Web Application on Render](https://fatear-web-application.onrender.com)

## Overview

**FatEar** is a music-based social media platform where users can:
- Rate and review music.
- Connect with other music lovers.
- Stay updated with friends' recent activities, new song releases, and reviews.

This platform provides an interactive experience for users to discover new music, share opinions, and engage with a music-focused community.

## Features

- **User Accounts:** Register a new account or use the sample login below to explore a pre-filled user experience.
- **Music Ratings & Reviews:** Share your thoughts and ratings on your favorite (or not-so-favorite) tracks.
- **Friends & Social Interaction:** Connect with friends to see their reviews, song recommendations, and recent activities.
- **Artist and User Search:** Discover new artists or find other users with similar music tastes.
- **PostgreSQL Integration:** Secure and efficient data management, hosted on Supabase.

## Sample Login Credentials

- **Username:** gwash
- **Password:** one

Use the sample login to see a filled-out profile, view user interactions, and explore music reviews.

## Technical Details

- **Database:** PostgreSQL hosted on [Supabase](https://supabase.com/).
- **Database Structure:** Find the detailed database structure in the [ER-Diagram.pdf](ER-Diagram.PDF).
- **SQL Scripts:** The database schema and sample data insertions are available in the provided SQL files for reference or setup.

## Getting Started

### Requirements:
- Python 3.x
- Flask
- PostgreSQL
- Supabase account (for database hosting)
  
### Local Setup:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/FatEar-web-application.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd FatEar-web-application
    ```
   
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your PostgreSQL database and configure the environment variables. Comment out lines 28-36 in app.py (production environment variables), and uncomment lines 17-27 for local variables. You'll need to configure a secret key, and the database credentials from your database in a "secrets.env" file. 

5. Run the application:
    ```bash
    flask run
    ```

6. Visit `http://localhost:5000` to view the app locally.
