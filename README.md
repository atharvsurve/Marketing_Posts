# 🚀 Marketing Posts — AI-Powered Instagram Campaign Generator

> A multi-agent AI system that generates complete Instagram marketing campaigns — from competitor analysis to ad copy to Midjourney image prompts — all running locally with Ollama.

**Built by [@atharvsurve](https://github.com/atharvsurve)**

---

## 📑 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Code Walkthrough](#code-walkthrough)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Tech Stack](#tech-stack)
- [License](#license)

---

## Overview

This project uses the **CrewAI** framework to orchestrate a team of autonomous AI agents that collaborate to produce a full Instagram marketing campaign for any product. You simply provide a product website URL and optional details, and the system delivers:

1. **Product & competitor analysis** — deep-dive into what makes the product unique
2. **Marketing campaign strategy** — themes, content pillars, audience profiles
3. **Instagram ad copy** — 3 ready-to-post options with hooks, CTAs, and hashtags
4. **Midjourney image prompts** — 3 cinematic, professional photo descriptions

Everything runs **100% locally** using [Ollama](https://ollama.com), so no OpenAI API key is needed.

---

## Architecture

The system is split into **two sequential crews**, each composed of specialized agents:

```
┌──────────────────────────────────────────────────────────┐
│                     COPY CREW                            │
│                                                          │
│  ┌─────────────────┐   ┌─────────────────────────────┐   │
│  │  Lead Market     │──▶│  Chief Marketing Strategist │   │
│  │  Analyst         │   │                             │   │
│  └─────────────────┘   └──────────────┬──────────────┘   │
│                                       │                  │
│                                       ▼                  │
│                          ┌────────────────────────┐      │
│                          │  Creative Content       │      │
│                          │  Creator                │      │
│                          └────────────────────────┘      │
│                                       │                  │
│                                       ▼                  │
│                              [Instagram Ad Copy]         │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                    IMAGE CREW                            │
│                                                          │
│  ┌─────────────────────┐   ┌─────────────────────────┐   │
│  │  Senior Photographer │──▶│  Chief Creative Director │  │
│  └─────────────────────┘   └─────────────────────────┘   │
│                                       │                  │
│                                       ▼                  │
│                          [Midjourney Image Prompts]       │
└──────────────────────────────────────────────────────────┘
```

---

## How It Works

### Phase 1: Copy Crew

The **Copy Crew** runs first with 3 agents executing 4 tasks sequentially:

| # | Task | Assigned Agent | What It Does |
|---|------|---------------|--------------|
| 1 | **Product Analysis** | Lead Market Analyst | Scrapes the product website and analyzes features, brand positioning, USPs, and market appeal |
| 2 | **Competitor Analysis** | Lead Market Analyst | Identifies top 3 competitors and compares branding, social media strategy, and customer engagement |
| 3 | **Campaign Development** | Chief Marketing Strategist | Creates a full campaign: theme, Instagram strategy, content pillars, Reels ideas, CTAs |
| 4 | **Instagram Ad Copy** | Creative Content Creator | Writes 3 punchy ad copies with hooks, main messages, CTAs, and hashtags |

### Phase 2: Image Crew

The **Image Crew** takes the ad copy output from Phase 1 and produces visual concepts:

| # | Task | Assigned Agent | What It Does |
|---|------|---------------|--------------|
| 5 | **Take Photograph** | Senior Photographer | Creates 3 cinematic Midjourney prompts based on the ad copy (no direct product shots) |
| 6 | **Review Photo** | Chief Creative Director | Reviews, refines, and approves the image prompts for brand alignment |

---

## Project Structure

```
Marketing_Posts/
├── main.py                    # Entry point — orchestrates both crews
├── agents.py                  # Defines all 5 AI agents with roles & tools
├── tasks.py                   # Defines all 6 tasks with prompts & expected outputs
├── tools/
│   ├── __init__.py
│   ├── browser_tools.py       # Website scraping & summarization tool
│   └── search_tools.py        # Google & Instagram search tools (via Serper API)
├── pyproject.toml             # Dependencies & project config
├── .env                       # Environment variables (API keys, model name)
├── .env.example               # Template for .env
├── .gitignore
└── uv.lock                    # Dependency lockfile
```

---

## Code Walkthrough

### `main.py` — The Orchestrator

This is the entry point. Here's what happens step by step:

1. **Loads environment variables** from `.env` using `python-dotenv`
2. **Configures the embedder** to use Ollama locally (so crewAI doesn't call OpenAI for embeddings):
   ```python
   embedder_config = {
       "provider": "ollama",
       "config": {
           "model": os.environ.get("MODEL", "openhermes"),
           "url": "http://localhost:11434",
       }
   }
   ```
3. **Prompts the user** for a product website URL and optional details
4. **Creates agents** (from `agents.py`) and **assigns tasks** (from `tasks.py`)
5. **Kicks off Copy Crew** — agents collaborate sequentially on analysis → strategy → ad copy
6. **Kicks off Image Crew** — takes the ad copy output and generates Midjourney image prompts
7. **Prints the final results** — ad copy + image prompts

---

### `agents.py` — The AI Team

Defines 5 specialized agents inside `MarketingAnalysisAgents`. Each agent has:

- **Role** — their job title (e.g., "Lead Market Analyst")
- **Goal** — what they're trying to achieve
- **Backstory** — persona context that shapes their behavior
- **Tools** — what external actions they can perform (search, scrape)
- **LLM** — the local Ollama model, referenced as `ollama/{MODEL}`

| Agent | Role | Tools | Can Delegate? |
|-------|------|-------|---------------|
| `product_competitor_agent` | Lead Market Analyst | Scrape, Search Internet | ❌ |
| `strategy_planner_agent` | Chief Marketing Strategist | Scrape, Search Internet, Search Instagram | ✅ |
| `creative_content_creator_agent` | Creative Content Creator | Scrape, Search Internet, Search Instagram | ✅ |
| `senior_photographer_agent` | Senior Photographer | Scrape, Search Internet, Search Instagram | ❌ |
| `chief_creative_diretor_agent` | Chief Creative Director | Scrape, Search Internet, Search Instagram | ✅ |

The LLM is configured using **litellm** format:
```python
self.llm = f"ollama/{os.environ['MODEL']}"  # e.g., "ollama/openhermes"
```

---

### `tasks.py` — The Task Definitions

Defines 6 tasks inside `MarketingAnalysisTasks`. Each task has:

- **`description`** — a detailed prompt telling the agent exactly what to do
- **`expected_output`** — what the final deliverable should look like
- **`agent`** — which agent is responsible

Tasks are chained sequentially within each crew — the output of one task feeds into the context of the next.

---

### `tools/browser_tools.py` — Website Scraper

The `BrowserTools.scrape_and_summarize_website` tool:

1. Sends the URL to the **Browserless API** to render the page
2. Parses the returned HTML using `unstructured.partition_html`
3. Splits the content into 8000-character chunks
4. For each chunk, spins up a **temporary "Principal Researcher" agent** that summarizes it using the local Ollama model
5. Returns the combined summary

This is the heaviest tool — it creates sub-agents on the fly to process large web pages.

---

### `tools/search_tools.py` — Search Engine

Two tools powered by the **Serper API** (Google Search):

- **`search_internet(query)`** — general web search, returns top 5 results with titles, links, and snippets
- **`search_instagram(query)`** — searches specifically within `site:instagram.com` for Instagram content

---

## Setup & Installation

### Prerequisites

- **Python** 3.10–3.11
- **[Ollama](https://ollama.com)** installed and running
- **[uv](https://docs.astral.sh/uv/)** package manager (recommended)

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/atharvsurve/Marketing_Posts.git
cd Marketing_Posts

# 2. Pull the Ollama model
ollama pull openhermes

# 3. Install dependencies
uv sync

# 4. Create your .env file
cp .env.example .env
# Edit .env with your API keys (see Configuration section)

# 5. Run it
python main.py
```

---

## Configuration

Create a `.env` file based on `.env.example`:

```env
# Google Search API (required for search tools)
SERPER_API_KEY=your_serper_api_key      # Get one free at https://serper.dev/

# Website scraping API (required for browser tools)
BROWSERLESS_API_KEY=your_browserless_key  # Get one free at https://www.browserless.io/

# Local LLM model name (must be pulled in Ollama)
MODEL=openhermes

# These prevent crewAI/litellm from trying to call OpenAI
OPENAI_API_KEY=NA
OPENAI_API_BASE=http://localhost:11434/v1
```

### Changing the Model

You can use any model available in Ollama. Just update `MODEL` in `.env`:

```env
MODEL=llama3        # or mistral, gemma2, etc.
```

Make sure to pull it first: `ollama pull llama3`

---

## Usage

```bash
python main.py
```

You'll be prompted for:

1. **Product website URL** — the website to analyze (e.g., `https://puma.com`)
2. **Extra details** — any specific requirements for the campaign

The system will then run both crews and output:

- **3 Instagram ad copy options** — ready to post
- **3 Midjourney image prompts** — cinematic photo descriptions

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| [CrewAI](https://github.com/crewAIInc/crewAI) v0.152+ | Multi-agent orchestration framework |
| [Ollama](https://ollama.com) | Local LLM inference (no cloud API needed) |
| [LiteLLM](https://github.com/BerriAI/litellm) | Universal LLM API adapter (used internally by CrewAI) |
| [Serper API](https://serper.dev/) | Google Search results |
| [Browserless](https://www.browserless.io/) | Headless browser for web scraping |
| [Unstructured](https://github.com/Unstructured-IO/unstructured) | HTML parsing & content extraction |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment variable management |

---

## License

This project is released under the MIT License.
