# Website Prospector Workflow - OpenAI Agents SDK PoC

An agentic workflow for discovering and analyzing outdated websites using OpenAI Agents SDK and Playwright.

## 🎯 What This PoC Does

This proof-of-concept implements a multi-agent workflow that:

1. **🔍 Discovers Prospects**: Searches for businesses with potentially outdated websites based on audience configurations
2. **📊 Analyzes Websites**: Uses Playwright to analyze websites for improvement opportunities
3. **📧 Extracts Contacts**: Finds contact information for outreach
4. **🤖 Coordinates Workflow**: Uses OpenAI Agents SDK to orchestrate the entire process

## 🏗️ Architecture

### Agents:

- **Coordinator Agent**: Orchestrates the entire workflow with handoffs
- **Search Agent**: Discovers prospects using audience configurations
- **Analysis Agent**: Analyzes websites using Playwright
- **Contact Agent**: Extracts contact information

### Tools:

- `search_prospects_for_audience()`: Web search using audience patterns
- `analyze_prospect_website()`: Comprehensive site analysis
- `extract_contact_info()`: Contact information extraction

## 🚀 Quick Setup

### Prerequisites

- Python 3.11+
- OpenAI API key
- Internet connection

### 1. Install Dependencies

```bash
cd apps/workflow
python setup.py
```

### 2. Set OpenAI API Key

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run the PoC

```bash
python main.py
```

## 📋 Available Audiences

The workflow uses predefined audience configurations:

- **local_business**: General local businesses (restaurants, shops, services)
- **professional_services**: Lawyers, accountants, consultants
- **home_services**: Plumbers, electricians, contractors

Each audience has specific search patterns and target keywords for finding prospects.

## 🧪 Testing the PoC

### Basic Test

```bash
python main.py
```

This runs a test workflow with 2 local business prospects in San Francisco.

### Custom Test

```python
import asyncio
from main import run_prospect_workflow

# Test with different parameters
asyncio.run(run_prospect_workflow(
    audience_name="professional_services",
    location="New York",
    max_prospects=3
))
```

## 📊 Expected Output

The workflow will output:

1. **Prospect Discovery**: URLs and business names found
2. **Website Analysis**: Scores for mobile, performance, SEO, security
3. **Contact Information**: Emails, phones, contact pages, social links
4. **Improvement Suggestions**: Specific recommendations for each site

## 🔧 Configuration

### Audience Configs

Edit `website_prospector/config/audience_configs.py` to:

- Add new audience types
- Modify search patterns
- Adjust target keywords
- Change prospect limits

### Analysis Weights

Modify scoring weights in `main.py`:

```python
scoring_weights = {
    'mobile_responsiveness': 0.25,
    'performance': 0.25,
    'seo': 0.20,
    'security': 0.15,
    'outdated': 0.15
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **Missing OpenAI API Key**

    ```
    export OPENAI_API_KEY="your-key"
    ```

2. **Playwright Browsers Not Installed**

    ```bash
    playwright install
    ```

3. **Import Errors**

    ```bash
    pip install -e .
    ```

4. **Network Timeouts**
    - Check internet connection
    - Some websites may block automated access

### Debug Mode

Set environment variable for verbose logging:

```bash
export DEBUG=1
python main.py
```

## 📈 Scaling & Production

### Next Steps for Production:

1. **Database Integration**: Persist prospects and analysis results
2. **Error Handling**: Robust retry mechanisms
3. **Rate Limiting**: Respect website policies
4. **Monitoring**: Track success rates and performance
5. **Contact Outreach**: Automated email campaigns

### Performance Optimizations:

- Parallel prospect processing
- Caching of analysis results
- Incremental updates
- Background job processing

## 🔍 Viewing Traces

The OpenAI Agents SDK provides built-in tracing. After running workflows, you can view traces in the OpenAI Dashboard to debug and optimize your agent interactions.

## 📝 License

This is a proof-of-concept for educational and testing purposes.
