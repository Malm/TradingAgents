# Claude Integration for TradingAgents

## ✅ What's Done

TradingAgents **already has full support for Anthropic Claude**! 

We've configured it to use:
- **LLM Provider**: `anthropic`
- **Deep Thinking Model**: `claude-sonnet-4-20250514` (Claude Sonnet 4)
- **Quick Thinking Model**: `claude-sonnet-4-20250514` (same, for consistency)

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
# Create conda environment
conda create -n tradingagents python=3.13
conda activate tradingagents

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

**RECOMMENDED: Use OpenRouter** (easiest + cheapest)

Create `.env` file in project root:

```bash
# Alpha Vantage API (for market data)
ALPHA_VANTAGE_API_KEY=6ZLKX5ZXMJHBMXQB

# OpenRouter API (for Claude via OpenRouter)
OPENAI_API_KEY=your_openrouter_api_key_here
```

**Get your OpenRouter API key:**
1. Go to: https://openrouter.ai/
2. Sign up + add $5-10 credits
3. Settings → Keys → Create Key
4. Add to `.env` file above

**Alternative: Direct Anthropic API**
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```
- Get key: https://console.anthropic.com/settings/keys
- Change config: `"llm_provider": "anthropic"`

### 3. Test with US Stock

```bash
python -m cli.main
# Select ticker: AAPL
# Select date: 2024-12-01 (or recent date)
```

### 4. Test with Swedish Stock

Swedish stocks on Alpha Vantage use `.ST` suffix (Stockholm Stock Exchange).

Example: `ABB.ST` for ABB Ltd

```bash
python test_swedish_stock.py
```

## 🔄 Keeping Up with Upstream

This is a fork of TauricResearch/TradingAgents. To sync with upstream:

```bash
# Fetch latest from upstream
git fetch upstream

# Merge upstream changes into our branch
git merge upstream/main

# Or rebase our changes on top of upstream
git rebase upstream/main
```

## 🇸🇪 Swedish Stocks Support

Alpha Vantage supports Stockholm Stock Exchange stocks with `.ST` suffix:

**Example tickers:**
- `ABB.ST` - ABB Ltd
- `VOLV-B.ST` - Volvo B
- `ERIC-B.ST` - Ericsson B
- `HM-B.ST` - H&M B
- `ATCO-A.ST` - Atlas Copco A

**Note:** Not all Swedish stocks may have full fundamental data on Alpha Vantage.

## 🚀 Next Steps

1. Get Anthropic API key and add to `.env`
2. Test with AAPL (US stock)
3. Test with ABB.ST (Swedish stock)
4. Build Nordnet integration wrapper
5. Add Notion logging
6. Add Telegram notifications

## 📊 Model Costs (Claude Sonnet 4 via OpenRouter)

**OpenRouter pricing (same as direct Anthropic):**
- **Input**: ~$3 per million tokens
- **Output**: ~$15 per million tokens

**Estimated cost per stock analysis:**
- ~50,000 input tokens (all agents + debates)
- ~5,000 output tokens (decisions + reasoning)
= **~$0.15-0.30 per stock per day**

With 10 stocks: **~$2-3/day** (~60 SEK/dag)

**Why OpenRouter?**
- One API for all models (Claude, GPT-4, etc.)
- Easy to switch models without code changes
- Simple billing (one account, one invoice)
- No monthly subscription needed
