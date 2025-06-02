


# 📊 Bulk Deal Volume Analyzer

This project helps you identify bulk deals in Indian stock markets (NSE/BSE) where the traded quantity exceeds **1% of the total volume traded that day** — a potential indicator of institutional activity or major market interest.

The data is sourced from NSE bulk deal disclosures and cross-referenced with historical trading volumes fetched using Yahoo Finance (`yfinance`). The app exposes a Flask API with multiple endpoints for data access.

---

## 🚀 `uv` as the package manager?

[`uv`](https://github.com/astral-sh/uv) is a modern, high-performance Python package manager and virtual environment tool written in Rust. This project uses `uv` for managing dependencies and environments.

### ✅ Benefits of `uv` over pip/venv:

- ⚡ **Faster** installs & dependency resolution
- 🧪 **Built-in virtual environment** support
- 🔒 **Secure** and reproducible installs with hash checking
- 🧼 **Cleaner** and zero-config setup

---

## 🧑‍💻 How to Setup the Project (with `uv`)

### 1. 🔧 Install `uv`:

```bash
curl -Ls https://astral.sh/uv/install.sh | bash
````

Or install via pipx:

```bash
pipx install uv
```
or we can use pip 
```bash
pip install uv
```
---

### 2. 📦clone the repo
```bash
https://github.com/Nkmeoo7/MarketStock_indicator.git
```
---

### 3. ▶️ Run the app:

```bash
uv run app.py
```



> By default, it runs at `http://127.0.0.1:5000/`

---

## 🌐 API Endpoints

### 1. `/bulk-deals` (GET)

* **Purpose**: Returns all stocks from the past **3 months** where:

  ```
  (bulk_deal_quantity / daily_volume) > 1%
  ```

* **Note**: This endpoint processes all data before responding, which may take time.make hit on ```http://127.0.0.1:5000/bulk-deals ```

---

### 2. `/fast-dumps` (GET)

* **Purpose**: Similar to `/bulk-deals` but optimized for **speed**.it will directly dump the raw json data on screen
* **Difference**: same as /bulk-deal endpoint but look at app.py 
function bulk deal store data inside result then after completing the operation it will return the result 

---

### 3. `/valid-symbols` (GET)

* **Purpose**: Returns only the **valid stock symbols** (from NSE/BSE) which are supported by `yfinance`.
* **Why**: Not all symbols in bulk deals are available on Yahoo Finance. This endpoint helps identify symbols with retrievable data.yfinance gives us limited data for particular symbols so we need to figure out the real symbols

---

## 📂 Project Structure

```
├── app.py                # Main Flask app with defined API routes
├── .python-version        #telling the python version  
├── pyproject.toml     # Python dependencies
├── README.md             # Project documentation (this file)
└── bulk.csv/                 # bulk trade that happen
```

---

## 📋 Requirements

* Python 3.10+
* `uv` (to manage environment & dependencies)
* Libraries:

  * Flask
  * yfinance
  * pandas
 `

---



## 🤝 Contributing

Feel free to fork, modify, and open PRs to contribute improvements or new features!

---

