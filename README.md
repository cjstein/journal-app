# Time Capsule Journal

## Overview

Time Capsule Journal is a Django-based web application originally deployed on Heroku, created as a showcase of my skills in web development. This project is not intended for practical use, but rather to demonstrate various features and technologies.

## Purpose
The purpose of this web application was to be able to write journal entries, then add and tag contacts to the entries, or mark them as public for all contacts to see.  There's a check-in feature that after 5 days without going to the site and checking in, your entries would be shared with those that were tagged with them.  It's a way to safely say your deepest thoughts and feelings without worrying about what others will think about until you are ready to share them with the world.    

## Features

- **Journal Entries:** Users can create personal journal entries to document their thoughts, experiences, and feelings.

- **Check-In System:** The application encourages users to check in at regular intervals. If a user fails to check in, the system can automatically notify selected contacts.

- **Contact Integration:** Users can add contacts to their Time Capsule Journal. If a user misses a check-in, the journal entry for that day can be automatically shared with selected contacts.

- **Payment Integration:** The project includes integration with the Stripe payment system that was used as a subscription service.

- **Recall Feature:** It was possible to recall your entries if check-in was accidentally missed.  


## Showcase

This project serves as a showcase of my skills in:
- Django
  - Setup using Django Cookie Cutter
  - Model Design Structure
  - Timed Custom Management Commands
- Integration of third-party services
  - Stripe for subscription based service
  - TinyMCE for a rich text editor
  - Mailgun for emails
  - Twilio for Text messages
  - AWS S3 Bucket for static files
- Deployment on Heroku
- Version control using Git

---
Thank you for exploring Time Capsule Journal! This project is intended to showcase various skills in web and Django development and is not intended for production use.
