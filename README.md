# Cribl API CLI Tool (Python)

A modular Python-based CLI for managing and automating tasks against the [Cribl API](https://docs.cribl.io/api/), now with an interactive command-line interface using `InquirerPy`.

## Features

- Interactive CLI menu with multi-layer navigation powered by `InquirerPy`
- Health checks to verify Cribl system status
- Packs management (view and install)
- Groups configuration fetching
- Global variables management (create and view)
- Lookups (upload, view, delete)
- Authorization policies and roles
- Regex management (create, view, update, delete)
- Worker operations (info, count, restart)
- System process operations (restart Cribl, list upgrades, get processes)
- Certificates inspection

## Folder Structure

```
cribl-api-cli/
├── main.py
├── README.md
├── requirements.txt
├── cribl/
│   ├── __init__.py
│   ├── auth.py
│   ├── authorize.py
│   ├── certificates.py
│   ├── global_variables.py
│   ├── groups.py
│   ├── lookups.py
│   ├── packs.py
│   ├── processes.py
│   ├── regex.py
│   ├── worker.py
├── config/
│   ├── __init__.py
│   └── config.py
```

## Prerequisites

- Python 3.7 or higher
- Required Python libraries (see `requirements.txt`)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Start the CLI tool:

```bash
python main.py
```

You will be prompted with a multi-choice interactive menu, allowing you to navigate and perform operations across the available Cribl modules.

## Authentication

Authentication is handled using bearer tokens retrieved via the `auth` module. It supports:

- Cribl.Cloud – Obtain tokens from the API Reference in the UI
- Customer-managed – Token retrieved by logging in with credentials (`POST /auth/login`)

Once authenticated, the token is automatically added to all API requests.

## API Coverage

This CLI covers the following Cribl API capabilities:

- `/auth/login`
- `/system/health`
- `/system/lookups`
- `/system/metrics/query`
- `/packs`
- `/m/<group>/inputs`, `/outputs`, `/routes`, `/pipelines`
- `/m/<group>/variables`
- `/workers`
- `/regex`
- `/certificates`

Refer to the [Cribl API Documentation](https://docs.cribl.io/api/) for the complete endpoint list and behavior.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Cribl Python API Wrapper](https://github.com/criblio/python-api-wrapper)
- [Cribl Official Documentation](https://docs.cribl.io/)