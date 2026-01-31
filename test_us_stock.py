#!/usr/bin/env python
"""
Test TradingAgents with Claude on a US stock (AAPL)
"""

import os
from datetime import datetime
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def main():
    print("=" * 60)
    print("TradingAgents - US Stock Test (Claude-powered)")
    print("=" * 60)
    
    # Check API keys
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY not set in .env file")
        print("Please add your Anthropic API key to .env")
        return
    
    if not os.getenv("ALPHA_VANTAGE_API_KEY"):
        print("⚠️  WARNING: ALPHA_VANTAGE_API_KEY not set")
    
    print(f"\n✅ Using Claude model: {DEFAULT_CONFIG['deep_think_llm']}")
    print(f"✅ LLM Provider: {DEFAULT_CONFIG['llm_provider']}")
    
    # Configure TradingAgents
    config = DEFAULT_CONFIG.copy()
    config["max_debate_rounds"] = 1  # Keep it simple for testing
    config["max_risk_discuss_rounds"] = 1
    
    # Initialize TradingAgents
    print("\n🔧 Initializing TradingAgents graph...")
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Test stock
    ticker = "AAPL"
    trade_date = "2024-12-01"  # Recent date with data
    
    print(f"\n📊 Analyzing {ticker} for {trade_date}...")
    print("-" * 60)
    
    try:
        # Run analysis
        final_state, decision = ta.propagate(ticker, trade_date)
        
        print("\n" + "=" * 60)
        print("📈 TRADING DECISION")
        print("=" * 60)
        print(f"\nStock: {ticker}")
        print(f"Date: {trade_date}")
        print(f"\nDecision: {decision}")
        print(f"\nFull reasoning:")
        print(final_state.get("final_trade_decision", "N/A"))
        
        # Show analyst reports summary
        print("\n" + "=" * 60)
        print("📋 ANALYST REPORTS SUMMARY")
        print("=" * 60)
        if final_state.get("fundamentals_report"):
            print(f"\n🔍 Fundamentals: {final_state['fundamentals_report'][:200]}...")
        if final_state.get("market_report"):
            print(f"\n📊 Technical: {final_state['market_report'][:200]}...")
        if final_state.get("news_report"):
            print(f"\n📰 News: {final_state['news_report'][:200]}...")
        if final_state.get("sentiment_report"):
            print(f"\n💭 Sentiment: {final_state['sentiment_report'][:200]}...")
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
