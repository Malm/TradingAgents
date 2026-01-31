# MCP Integration Plan for TradingAgents

## Goal
Replace LLM "knowledge" with verified real-time data from MCP servers.

## MCP Servers to Integrate

### 1. Yahoo Finance MCP (Already available)
- **Tools:** get_ticker_info, get_ticker_news, ticker_earning
- **Use:** Company info, news, earnings calendar
- **Analysts:** Fundamental, News

### 2. Trading MCP Server (LobeHub)
- **Repo:** https://github.com/lobehub/lobe-mcp-servers/tree/main/packages/trading
- **Tools:** 
  - Stock screening
  - Insider trading data
  - Social sentiment (Twitter, Reddit)
  - News analysis
- **Analysts:** News, Sentiment

### 3. Financial Datasets MCP
- **Tools:**
  - Income statements
  - Balance sheets
  - Cash flow statements
  - Stock prices
- **Analysts:** Fundamental

### 4. Financial Modeling Prep (FMP) MCP
- **Tools:**
  - Company profile
  - Financial ratios (P/E, P/B, ROE)
  - Key metrics (EPS, FCF, dividends)
- **Analysts:** Fundamental

### 5. Trading Economics API (not MCP, but similar)
- **Tools:**
  - Economic calendar (Fed, ECB, Riksbanken)
  - Macro indicators (CPI, jobs, PMI)
  - Country-specific data (China, USA, EU)
- **Analysts:** Macro (NEW agent)

## Implementation Steps

### Step 1: Add MCP Client to TradingAgents

```python
# tradingagents/mcp_client.py

from mcp import ClientSession
import asyncio

class MCPToolManager:
    """Manages MCP server connections and tools"""
    
    def __init__(self):
        self.sessions = {}
        
    async def connect_yahoo_finance(self):
        """Connect to Yahoo Finance MCP server"""
        # Using stdio or HTTP connection
        self.sessions['yahoo'] = await ClientSession.connect_stdio(
            command="uvx",
            args=["yahoo-finance-server"]
        )
        
    async def connect_trading_mcp(self):
        """Connect to Trading MCP (LobeHub)"""
        self.sessions['trading'] = await ClientSession.connect_http(
            url="http://localhost:3000/mcp"
        )
        
    async def connect_fmp(self):
        """Connect to FMP MCP"""
        self.sessions['fmp'] = await ClientSession.connect_http(
            url="https://api.fmp.mcp",
            headers={"X-API-KEY": os.getenv("FMP_API_KEY")}
        )
        
    def get_tools_for_analyst(self, analyst_type):
        """Return MCP tools for specific analyst"""
        if analyst_type == "fundamentals":
            return [
                self.sessions['yahoo'].tools['get_ticker_info'],
                self.sessions['fmp'].tools['get_key_metrics'],
                self.sessions['fmp'].tools['get_financial_ratios'],
            ]
        elif analyst_type == "news":
            return [
                self.sessions['yahoo'].tools['get_ticker_news'],
                self.sessions['trading'].tools['get_news_sentiment'],
                self.sessions['trading'].tools['get_insider_trading'],
            ]
        # ... etc
```

### Step 2: Modify Analyst Tool Nodes

```python
# tradingagents/graph/trading_graph.py

from tradingagents.mcp_client import MCPToolManager

class TradingAgentsGraph:
    def __init__(self, ...):
        # ... existing code ...
        
        # Initialize MCP
        self.mcp_manager = MCPToolManager()
        asyncio.run(self._init_mcp())
        
        # Create tool nodes with MCP tools
        self.tool_nodes = self._create_mcp_tool_nodes()
        
    async def _init_mcp(self):
        """Initialize all MCP connections"""
        await self.mcp_manager.connect_yahoo_finance()
        await self.mcp_manager.connect_trading_mcp()
        await self.mcp_manager.connect_fmp()
        
    def _create_mcp_tool_nodes(self):
        """Create tool nodes using MCP instead of vendors"""
        return {
            "fundamentals": ToolNode(
                self.mcp_manager.get_tools_for_analyst("fundamentals")
            ),
            "news": ToolNode(
                self.mcp_manager.get_tools_for_analyst("news")
            ),
            "market": ToolNode([
                get_stock_data,  # Keep yfinance for OHLCV
                get_indicators,
            ]),
        }
```

### Step 3: Add Macro Analyst

```python
# tradingagents/agents/analysts/macro_analyst.py

MACRO_ANALYST_PROMPT = """
You are a Macroeconomic Analyst for trading decisions.

Your job:
1. Check economic calendar for upcoming events (Fed meetings, ECB decisions, jobs reports)
2. Analyze recent macro data (CPI, PMI, unemployment, etc.)
3. Assess impact on target stock's sector and geography
4. Provide macro sentiment (bullish/bearish/neutral)

Tools available:
- get_economic_calendar: Upcoming central bank decisions, data releases
- get_macro_indicator: CPI, PMI, jobs data for specific countries
- get_fed_rate: Current and expected Fed funds rate

Format your report as:
### Macro Environment for {ticker}

**Upcoming Events (Next 7 days):**
- List key events

**Recent Data:**
- Key macro indicators

**Impact Assessment:**
- How macro affects this stock

**Macro Sentiment:** Bullish/Bearish/Neutral
"""

def create_macro_analyst(llm, tools):
    """Create macro analyst agent"""
    return create_react_agent(
        llm,
        tools,
        state_modifier=MACRO_ANALYST_PROMPT
    )
```

### Step 4: Update Workflow

```python
# Add macro step BEFORE investment debate

workflow.add_node("macro_analyst", macro_analyst_node)
workflow.add_node("macro_tools", macro_tool_node)

# Flow: market → fundamentals → news → MACRO → debate
workflow.add_edge("news_analyst", "macro_analyst")
workflow.add_edge("macro_analyst", "macro_tools")
workflow.add_conditional_edges("macro_tools", ...)
workflow.add_edge("macro_done", "investment_debate_start")
```

## Testing Plan

### Test 1: Verify MCP Data Quality
```bash
python test_mcp_integration.py --ticker=ABB.ST --date=2024-12-01
```

Expected output:
```
Fundamental Analyst:
- Revenue (Q3 2024): $8.2B [Source: FMP MCP]
- China revenue: 14.6% ($1.2B) [Source: FMP geographic breakdown]
- Operating margin: 16.1% [Source: Financial Datasets MCP]
- P/E ratio: 22.3x [Source: FMP MCP]

News Analyst:
- Latest news: "ABB wins $500M contract in India" [Source: Yahoo Finance MCP]
- Insider trades: CEO sold 10,000 shares on Nov 15 [Source: Trading MCP]
- Social sentiment: 72% positive (Reddit: 68%, Twitter: 76%) [Source: Trading MCP]

Macro Analyst:
- Upcoming: ECB rate decision Dec 12 (hold expected) [Source: Trading Economics]
- China PMI: 49.1 (contraction) [Source: Trading Economics]
- Eurozone GDP: -0.1% QoQ [Source: Trading Economics]
- Impact: Bearish on ABB (Eurozone exposure + China weakness)
```

### Test 2: Compare LLM vs MCP
Run same stock with:
1. Old system (LLM knowledge only)
2. New system (MCP verified data)

Compare:
- Data accuracy
- Source citations
- Decision quality

## Rollout

1. **Week 1:** Setup all MCP servers locally
2. **Week 2:** Integrate into TradingAgents
3. **Week 3:** Test with paper trading
4. **Week 4:** Go live with verified data

## Cost Estimate

| MCP Server | Cost | Requests/day | Monthly Cost |
|------------|------|--------------|--------------|
| Yahoo Finance | Free | Unlimited | $0 |
| Trading MCP | Free | Self-hosted | $0 |
| FMP | Free tier | 250/day | $0 (upgrade $14/mo if needed) |
| Trading Economics | Free tier | 300/month | $0 (upgrade $30/mo if needed) |

**Total: $0 initially, ~$44/mo for premium tiers if needed**

## Success Criteria

✅ All analysts cite data sources  
✅ No "LLM guesses" in reports  
✅ Fresh data (<24h old)  
✅ Macro events factored into decisions  
✅ Paper trading shows improved decision quality  
