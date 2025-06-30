# 🏀 Parlay Tracker Backend

A lightweight backend service for creating, storing, and tracking player-based parlays in real time using NBA data.

Built with:
- 🐍 FastAPI
- 🧬 GraphQL via Ariadne
- 🗂 TinyDB for local storage
- 📊 Live stats integration (e.g., `nba_api` or external APIs)
- ☁️ Terraform setup for cloud deployment (optional)

---

## 🚀 Features

- Create and save parlays made of multiple player stat legs
- Query parlays by user ID
- Fetch live NBA stats to track progress on each leg
- GraphQL API using Ariadne
- Easy to swap TinyDB for DynamoDB or another database
- Periodic fetching of live stats
