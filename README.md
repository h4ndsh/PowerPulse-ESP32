# ⚡ PowerPulse-ESP32

<div align="center">

[![GitHub license](https://img.shields.io/github/license/h4ndsh/PowerPulse-ESP32?style=for-the-badge)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/h4ndsh/PowerPulse-ESP32?style=for-the-badge)](https://github.com/h4ndsh/PowerPulse-ESP32/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/h4ndsh/PowerPulse-ESP32?style=for-the-badge)](https://github.com/h4ndsh/PowerPulse-ESP32/network)

**A real-time power monitoring system using an ESP32 and Python server, with Telegram alerts for power outages.**

</div>

## 📖 Overview

**PowerPulse-ESP32** is an intelligent system designed to monitor and log power consumption in real time. It uses an **ESP32 microcontroller** to collect readings and a **Python server** to process, store, and analyze the data.  

When a power outage or abnormal event is detected, the system sends **instant Telegram alerts** to configured chats, ensuring fast notifications and quick action.  

The ESP32 operates as a client, sending regular **heartbeat** signals to the server, enabling continuous and reliable monitoring.

## ✨ Features

- Real-time power consumption tracking via ESP32.
- Data logging and storage on a Python server.
- Instant Telegram alerts for power outages.
- Simple and easy-to-deploy architecture.
- Heartbeat-based monitoring to ensure continuous operation.

## 🛠️ Tech Stack

**Backend:**

- Python

**Embedded:**

- ESP32 Microcontroller

## 🚀 Quick Start

This project requires an **ESP32 microcontroller** and a system capable of running the Python server.

### Prerequisites

- Python 3.x (version compatible with listed libraries in `requirements.txt`)
- ESP32 development environment (Arduino IDE recommended)
- `pyserial` Python library

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/h4ndsh/PowerPulse-ESP32.git
   cd PowerPulse-ESP32
