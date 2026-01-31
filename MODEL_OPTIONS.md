# Model Options for TradingAgents via OpenRouter

## 💰 Cost Comparison (per 1M tokens)

| Model | Input | Output | Est. cost/stock/day | Quality | Speed |
|-------|-------|--------|---------------------|---------|-------|
| **Google Gemini 2.0 Flash** ⭐ | $0.075 | $0.30 | **$0.005** (~0.15 SEK) | Good | Very Fast |
| DeepSeek V3 | $0.27 | $1.10 | $0.015 (~0.45 SEK) | Very Good | Fast |
| Llama 3.3 70B | $0.35 | $0.40 | $0.018 (~0.55 SEK) | Good | Fast |
| Mistral Large | $2 | $6 | $0.10 (~3 SEK) | Very Good | Fast |
| Claude Sonnet 4 | $3 | $15 | **$0.20** (~6 SEK) | Excellent | Fast |
| GPT-4o | $2.50 | $10 | $0.15 (~4.50 SEK) | Excellent | Fast |

**Estimated for 10 stocks:**
- **Gemini Flash**: ~$0.05/dag (~1.50 SEK) 🎯
- **Claude Sonnet 4**: ~$2/dag (~60 SEK)

**40x billigare med Gemini Flash!**

---

## 🎯 Recommended Setup

### **Budget (Recommended for testing/paper trading)**
```python
"deep_think_llm": "google/gemini-2.0-flash-exp:free",
"quick_think_llm": "google/gemini-2.0-flash-exp:free",
```
- Cost: ~$0.05/dag (~1.50 SEK)
- Good enough for most trading decisions
- FREE tier available on OpenRouter!

### **Balanced (Good quality, reasonable cost)**
```python
"deep_think_llm": "deepseek/deepseek-chat",
"quick_think_llm": "google/gemini-2.0-flash-exp:free",
```
- Cost: ~$0.10/dag (~3 SEK)
- Deep thinking with DeepSeek
- Quick analysis with Gemini

### **Premium (Best quality, expensive)**
```python
"deep_think_llm": "anthropic/claude-sonnet-4",
"quick_think_llm": "anthropic/claude-sonnet-3.5",
```
- Cost: ~$1.50/dag (~45 SEK)
- Best reasoning and analysis
- Use for live trading with real money

---

## 📝 How to Change Model

Edit `/Users/bot/Code/TradingAgents/tradingagents/default_config.py`:

```python
DEFAULT_CONFIG = {
    # ...
    "llm_provider": "openrouter",
    "deep_think_llm": "google/gemini-2.0-flash-exp:free",  # Change this
    "quick_think_llm": "google/gemini-2.0-flash-exp:free", # Change this
    "backend_url": "https://openrouter.ai/api/v1",
    # ...
}
```

**Available models on OpenRouter:**
- See full list: https://openrouter.ai/models

---

## 🧪 Testing Strategy

**Phase 1: Paper Trading (2-4 weeks)**
- Use **Gemini Flash** (~$0.05/dag)
- Validate strategy works
- Total cost: ~$2-4 for entire testing period

**Phase 2: Small Live Trading (2 weeks)**
- Use **DeepSeek V3** (~$0.15/dag)
- Start with 1000-2000 SEK
- Better reasoning for real money

**Phase 3: Full Live Trading**
- Use **Claude Sonnet 4** (~$2/dag)
- Full 5000 SEK portfolio
- Best decision quality

---

## ⚠️ Quality vs Cost

**When to use cheaper models:**
- ✅ Paper trading / backtesting
- ✅ Learning the system
- ✅ Testing strategies
- ✅ Low-risk positions

**When to use premium models:**
- ✅ Real money trading
- ✅ Large positions
- ✅ High-volatility markets
- ✅ Complex analysis needed

**Remember:** A $0.15 better decision can save you $100+ on a bad trade!

---

## 🎯 My Recommendation

**Start with Gemini Flash:**
1. Test with US stocks (AAPL, NVDA)
2. Test with Swedish stocks (ABB.ST, VOLV-B.ST)
3. Paper trade for 1-2 weeks
4. If decisions look good → keep it!
5. If quality is lacking → upgrade to DeepSeek or Claude

**Cost savings:** ~$60/month vs Claude = ~1800 SEK saved!

That's 36% of your starting capital saved in API costs. 💰
