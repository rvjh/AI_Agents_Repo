import os
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv
from agno.agent import Agent 
from agno.models.google import Gemini


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = Gemini(
    id="gemini-2.0-flash-exp",
    api_key=os.getenv("GEMINI_API_KEY")  # ✅ THIS is what was missing
)


def compare_stocks(symbols):
    data = {}
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="6mo")
            if hist.empty:
                print(f"No data for {symbol}")
                continue
            data[symbol] = hist['Close'].pct_change().sum()
        except Exception as e:
            print(f"Error retrieving {symbol}: {e}")
    return data

def get_company_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return {
        "name": info.get("longName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "summary": info.get("longBusinessSummary", "N/A"),
    }

def get_company_news(symbol):
    stock = yf.Ticker(symbol)
    try:
        return stock.news[:5]
    except Exception:
        return []


market_analyst = Agent(
    model=model,
    description="Analyzes and compares stock performance over time.",
    instructions=[
        "Retrieve and compare stock performance from Yahoo Finance.",
        "Calculate percentage change over a 6-month period.",
        "Rank stocks based on their relative performance."
    ],
    show_tool_calls=True,
    markdown=True
)

company_researcher = Agent(
    model=model,
    description="Fetches company profiles, financials, and latest news.",
    instructions=[
        "Retrieve company information from Yahoo Finance.",
        "Summarize latest company news relevant to investors.",
        "Provide sector, market cap, and business overview."
    ],
    markdown=True
)

stock_strategist = Agent(
    model=model,
    description="Provides investment insights and recommends top stocks.",
    instructions=[
        "Analyze stock performance trends and company fundamentals.",
        "Evaluate risk-reward potential and industry trends.",
        "Provide top stock recommendations for investors."
    ],
    markdown=True
)

team_lead = Agent(
    model=model,
    description="Aggregates stock analysis, company research, and investment strategy.",
    instructions=[
        "Compile stock performance, company analysis, and recommendations.",
        "Ensure all insights are structured in an investor-friendly report.",
        "Rank the top stocks based on combined analysis."
    ],
    markdown=True
)


def get_market_analysis(symbols):
    performance_data = compare_stocks(symbols)
    if not performance_data:
        return "No valid stock data found."
    response = market_analyst.run(f"Compare these stock performances: {performance_data}")
    return response.content

def get_company_analysis(symbol):
    info = get_company_info(symbol)
    news = get_company_news(symbol)
    response = company_researcher.run(
        f"Provide an analysis for {info['name']} in the {info['sector']} sector.\n"
        f"Market Cap: {info['market_cap']}\n"
        f"Summary: {info['summary']}\n"
        f"Latest News: {news}"
    )
    return response.content

def get_stock_recommendations(symbols):
    market_analysis = get_market_analysis(symbols)
    company_data = {symbol: get_company_analysis(symbol) for symbol in symbols}
    recommendations = stock_strategist.run(
        f"Based on the market analysis: {market_analysis}, and company news {company_data}, "
        f"which stocks would you recommend for investment?"
    )
    return recommendations.content

def get_final_investment_report(symbols):
    market_analysis = get_market_analysis(symbols)
    company_analyses = [get_company_analysis(symbol) for symbol in symbols]
    stock_recommendations = get_stock_recommendations(symbols)

    final_report = team_lead.run(
        f"Market Analysis:\n{market_analysis}\n\n"
        f"Company Analyses:\n{company_analyses}\n\n"
        f"Stock Recommendations:\n{stock_recommendations}\n\n"
        f"Provide the full analysis of each stock with fundamentals and market news. "
        f"Generate a final ranked list in ascending order on which should I buy."
    )
    return final_report.content

# --------------------- Streamlit UI --------------------- #

st.set_page_config(page_title="AI Investment Strategist", page_icon="📈", layout="wide")

st.markdown("""
    <h1 style="text-align: center; color: #4CAF50;">📈 AI Investment Strategist</h1>
    <h3 style="text-align: center; color: #6c757d;">Generate personalized investment reports with the latest market insights.</h3>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <h2 style="color: #343a40;">Configuration</h2>
    <p style="color: #6c757d;">Enter the stock symbols you want to analyze. The AI will provide detailed insights, performance reports, and top recommendations.</p>
""", unsafe_allow_html=True)

input_symbols = st.sidebar.text_input("Enter Stock Symbols (separated by commas)", "AAPL, TSLA, GOOG")
symbols = [symbol.strip().upper() for symbol in input_symbols.split(",") if symbol.strip()]

if st.sidebar.button("Generate Investment Report"):
    if not symbols:
        st.sidebar.warning("Please enter at least one stock symbol.")
    else:
        st.subheader("Investment Report")
        with st.spinner("Generating report..."):
            report = get_final_investment_report(symbols)
        st.markdown(report)

        st.info("This report provides detailed insights, including market performance, company analysis, and investment recommendations.")

        st.markdown("### 📊 Stock Performance (6-Months)")
        try:
            stock_data = yf.download(symbols, period="6mo")['Close']
            fig = go.Figure()
            for symbol in symbols:
                if symbol in stock_data.columns:
                    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data[symbol], mode='lines', name=symbol))
            fig.update_layout(title="Stock Performance Over the Last 6 Months",
                              xaxis_title="Date",
                              yaxis_title="Price (in USD)",
                              template="plotly_dark")
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Could not plot stock performance: {e}")
