# Hospital Management System (HMS) – Python Flask Project

## Overview

This project is a **Hospital Management System (HMS)** built using Python and Flask. The application is designed to manage information related to healthcare, supporting healthcare providers in efficiently handling various aspects of hospital management.

It demonstrates integration with ReplAuth for authentication and showcases how to access and display user information from Replit headers in a Flask web app.

---

## Features

- **User Authentication with ReplAuth**: Supports both Node.js and Python Flask implementations for ReplAuth.
- **Manage Hospital Data**: Handles information for all hospital departments, including:
  - Clinical
  - Financial
  - Laboratory
  - Inpatient & Outpatient
  - Operation Theater
  - Materials
  - Nursing
  - Pharmaceutical
  - Radiology
  - Pathology and more
- **Modern Web UI**: Uses Bootstrap for styling (see `templates/navbar.html`, `footer.html`).
- **Custom Registration Page**: User can register via a custom form (`templates/registernow.html`).
- **About Page**: Simple about section for project details.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Flask
- (For Replit: See `replit.nix` for environment setup)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BirendraKSharma/softwareProject.git
   cd softwareProject
   ```

2. Set up the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   *(For Replit users, the environment is configured using `replit.nix`.)*

3. Run the application:
   ```bash
   flask run
   ```

### Usage

- Access the homepage at `http://localhost:5000/`.
- Registration form at `/templates/registernow.html`.
- About page at `/templates/about.html`.

---

## Authentication with ReplAuth (Python Flask)

**Example code to fetch user data from headers:**
```python
from flask import Flask, render_template, request
app = Flask('app')

@app.route('/')
def hello_world():
    print(request.headers)
    return render_template(
        'index.html',
        user_id=request.headers['X-Replit-User-Id'],
        user_name=request.headers['X-Replit-User-Name'],
        user_roles=request.headers['X-Replit-User-Roles'],
        user_bio=request.headers['X-Replit-User-Bio'],
        user_profile_image=request.headers['X-Replit-User-Profile-Image'],
        user_teams=request.headers['X-Replit-User-Teams'],
        user_url=request.headers['X-Replit-User-Url']
    )
```

**Available Replit Headers:**
```
X-Replit-User-Bio
X-Replit-User-Id
X-Replit-User-Name
X-Replit-User-Profile-Image
X-Replit-User-Roles
X-Replit-User-Teams
X-Replit-User-Url
```

Display a username in a template:
```html
<h1>{{ user_name }}</h1>
```

---

## FAQ

<details>
  <summary>ReplAuth FAQ</summary>
  
  > *How many ReplAuths are there?*
  
  - There are 2 repl auths!
 ---
  > *Which ReplAuths are there?*
  
  - Node.js and Python Flask
---
  > *Is there a Replit Documentation on ReplAuths?*

  - Yes! You can find it in the [Replit Docs](https://docs.replit.com)
</details>

---

## Support

If you have any questions, please refer to:
- [Replit Docs](https://docs.replit.com)
- [Ask forum](https://ask.replit.com)

---

## License

This project is for educational purposes. Please see individual files for license information if present.
