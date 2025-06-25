# Microearthquake Monitoring Data Analysis Dashboard

<div align='center'>
    <img src='documentation/demo.gif'>
</div>

## Overview

The **Microearthquake Monitoring Data Analysis Dashboard** is a web application built with **Django** designed specifically for internal development and operational use. This dashboard allows for the analysis and visualization of microearthquake data stored in a PostgreSQL database. Utilizing **Plotly**, it provides interactive visualizations including various plotting capabilities for efficient data exploration.

---

## Features

- Interactive visualizations of microearthquake events.
- Integration with a PostgreSQL/PostGIS database for effective geographical data handling.
- Automated data querying and processing using Django ORM, Pandas and NumPy.
- Vanilla JavaScript (fetch API) front-end interactions for real-time data updates and analysis.
- User-friendly interface for managing and navigating through data analysis tasks.
- Dynamic data filtering and downloading (microearthquake catalog).

---

## Getting Started

If you'd like to test this app using **Docker** on your local machine, the following instructions will help you set it up and run it locally.

Please note that, due to data confidentiality policies, the database contents are not included—so the app will appear blank. Which means you also have to set the Admin setting and credentials manually.

If you're interested in the database structure, feel free to contact me via email at [edelo.arham@gmail.com](mailto:edelo.arham@gmail.com), i will provide you full dummy database.

### Prerequisites

Ensure you have the following installed:

- **Docker**: For containerization.
- **Docker Compose**: For managing multi-container Docker applications.

### Cloning the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/microearthquake-dashboard.git
cd microearthquake-dashboard
```

### Running the Application

1. **Setup Environment Variables**: Create a `.env` file and configure the necessary variables (check webapp/settings.py):
    ```env
    DB_URL=postgres://yourusername:yourpassword@db:5432/yourdbname
    MAPBOX_API_TOKEN=your_mapbox_token
    ```

2. **Building and Running Docker Containers**:
   ```bash
   docker-compose up --build
   ```

3. **Access the Dashboard**: Open your browser and go to [http://localhost:8000](http://localhost:8000). 

---

## Project Structure

```plaintext
microearthquake-dashboard/
│
├── .github
│   └── workflows
│       └── build-push-deploy.yml
├── .gitignore
├── LICENSE
├── README.md
├── dir_tree.txt
├── django_project
│   ├── account
│   ├── db.sqlite3
│   ├── frontpage
│   ├── manage.py
│   ├── project
│   ├── static
│   │   └── js
│   │   └── media
│   └── webapp
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── docker-compose.yml
├── documentation
│   ├── demo.gif
│   └── schematic.png
├── fastapi_service
│   ├── app
│   │   ├── __init__.py
│   │   └── main.py
│   └── requirements.txt
└── infrastructure
    └── docker
        ├── django
        │   ├── .dockerignore
        │   ├── Dockerfile
        │   └── entrypoint.prod.sh
        └── nginx
            ├── Dockerfile.nginx
            └── nginx.conf
```

---

## Architecture and Scheme
<div align='center'>
    <img src='documentation/schematic.png'>
</div>


## Future Improvements

### Enhancements in Automatic Hypocenter Processing

Current improvements are focused on developing advanced backend data engine functionalities with FastAPI to enable:

- **Automatic Hypocenter Determination**: Implement algorithms that can automatically identify hypocenter locations from seismic data.
- **Hypocenter Relocation Methods**: Improve existing methodologies for relocating hypocenters based on improved data input and processing techniques.
- **Moment Magnitude Calculations**: Enable automatic computation of moment magnitudes for detected seismic events.
- **Post Data Analytics**: Incorporate analytical methods such as **Gutenberg-Richter analysis** to better understand the distribution and frequency of seismic events.

These enhancements will make the application more robust for internal development, streamline workflows, and provide more accurate analyses of seismic data in microearthquake monitoring.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Technology Stacks

- **Django**: For the robust web framework.
- **FastAPI**: For backend data processing, way faster than Django Rest Framework.
- **PostgreSQL/PostGIS**: For database/handling geographical data.
- **AWS RDS**: Relational database cloud service for hosting postgreSQL.
- **Plotly**: For rich interactive data visualizations.
- **Docker**: For containerizing the application.
- **DigitalOcean Droplets**: For deployment.

For more information on project usage, please refer to the codebase or contact the project maintainers to [edelo.arham@gmail.com](mailto:edelo.arham@gmail.com).
