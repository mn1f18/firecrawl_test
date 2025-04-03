Quickstart
Firecrawl allows you to turn entire websites into LLM-ready markdown

Hero Light
​
Welcome to Firecrawl
Firecrawl is an API service that takes a URL, crawls it, and converts it into clean markdown. We crawl all accessible subpages and give you clean markdown for each. No sitemap required.

​
How to use it?
We provide an easy to use API with our hosted version. You can find the playground and documentation here. You can also self host the backend if you’d like.

Check out the following resources to get started:

 API: Documentation
 SDKs: Python, Node, Go, Rust
 LLM Frameworks: Langchain (python), Langchain (js), Llama Index, Crew.ai, Composio, PraisonAI, Superinterface, Vectorize
 Low-code Frameworks: Dify, Langflow, Flowise AI, Cargo, Pipedream
 Others: Zapier, Pabbly Connect
 Want an SDK or Integration? Let us know by opening an issue.
Self-host: To self-host refer to guide here.

​
API Key
To use the API, you need to sign up on Firecrawl and get an API key.

​
Features
Scrape: scrapes a URL and get its content in LLM-ready format (markdown, structured data via LLM Extract, screenshot, html)
Crawl: scrapes all the URLs of a web page and return content in LLM-ready format
Map: input a website and get all the website urls - extremely fast
Extract: get structured data from single page, multiple pages or entire websites with AI.
​
Powerful Capabilities
LLM-ready formats: markdown, structured data, screenshot, HTML, links, metadata
The hard stuff: proxies, anti-bot mechanisms, dynamic content (js-rendered), output parsing, orchestration
Customizability: exclude tags, crawl behind auth walls with custom headers, max crawl depth, etc…
Media parsing: pdfs, docx, images.
Reliability first: designed to get the data you need - no matter how hard it is.
Actions: click, scroll, input, wait and more before extracting data
You can find all of Firecrawl’s capabilities and how to use them in our documentation

​
Crawling
Used to crawl a URL and all accessible subpages. This submits a crawl job and returns a job ID to check the status of the crawl.

​
Installation

Python

Node

Go

Rust

Copy
pip install firecrawl-py
​
Usage

Python

Node

Go

Rust

cURL

Copy
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Crawl a website:
crawl_status = app.crawl_url(
  'https://firecrawl.dev', 
  params={
    'limit': 100, 
    'scrapeOptions': {'formats': ['markdown', 'html']}
  },
  poll_interval=30
)
print(crawl_status)
If you’re using cURL or async crawl functions on SDKs, this will return an ID where you can use to check the status of the crawl.


Copy
{
  "success": true,
  "id": "123-456-789",
  "url": "https://api.firecrawl.dev/v1/crawl/123-456-789"
}
​
Check Crawl Job
Used to check the status of a crawl job and get its result.


Python

Node

Go

Rust

cURL

Copy
crawl_status = app.check_crawl_status("<crawl_id>")
print(crawl_status)
​
Response
The response will be different depending on the status of the crawl. For not completed or large responses exceeding 10MB, a next URL parameter is provided. You must request this URL to retrieve the next 10MB of data. If the next parameter is absent, it indicates the end of the crawl data.


Scraping

Completed

Copy
{
  "status": "scraping",
  "total": 36,
  "completed": 10,
  "creditsUsed": 10,
  "expiresAt": "2024-00-00T00:00:00.000Z",
  "next": "https://api.firecrawl.dev/v1/crawl/123-456-789?skip=10",
  "data": [
    {
      "markdown": "[Firecrawl Docs home page![light logo](https://mintlify.s3-us-west-1.amazonaws.com/firecrawl/logo/light.svg)!...",
      "html": "<!DOCTYPE html><html lang=\"en\" class=\"js-focus-visible lg:[--scroll-mt:9.5rem]\" data-js-focus-visible=\"\">...",
      "metadata": {
        "title": "Build a 'Chat with website' using Groq Llama 3 | Firecrawl",
        "language": "en",
        "sourceURL": "https://docs.firecrawl.dev/learn/rag-llama3",
        "description": "Learn how to use Firecrawl, Groq Llama 3, and Langchain to build a 'Chat with your website' bot.",
        "ogLocaleAlternate": [],
        "statusCode": 200
      }
    },
    ...
  ]
}
​
Scraping
To scrape a single URL, use the scrape_url method. It takes the URL as a parameter and returns the scraped data as a dictionary.


Python

Node

Go

Rust

cURL

Copy
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape a website:
scrape_result = app.scrape_url('firecrawl.dev', params={'formats': ['markdown', 'html']})
print(scrape_result)
​
Response
SDKs will return the data object directly. cURL will return the payload exactly as shown below.


Copy
{
  "success": true,
  "data" : {
    "markdown": "Launch Week I is here! [See our Day 2 Release 🚀](https://www.firecrawl.dev/blog/launch-week-i-day-2-doubled-rate-limits)[💥 Get 2 months free...",
    "html": "<!DOCTYPE html><html lang=\"en\" class=\"light\" style=\"color-scheme: light;\"><body class=\"__variable_36bd41 __variable_d7dc5d font-inter ...",
    "metadata": {
      "title": "Home - Firecrawl",
      "description": "Firecrawl crawls and converts any website into clean markdown.",
      "language": "en",
      "keywords": "Firecrawl,Markdown,Data,Mendable,Langchain",
      "robots": "follow, index",
      "ogTitle": "Firecrawl",
      "ogDescription": "Turn any website into LLM-ready data.",
      "ogUrl": "https://www.firecrawl.dev/",
      "ogImage": "https://www.firecrawl.dev/og.png?123",
      "ogLocaleAlternate": [],
      "ogSiteName": "Firecrawl",
      "sourceURL": "https://firecrawl.dev",
      "statusCode": 200
    }
  }
}
​
Extraction
With LLM extraction, you can easily extract structured data from any URL. We support pydantic schemas to make it easier for you too. Here is how you to use it:

v1 is only supported on node, python and cURL at this time.


Python

Node

cURL

Copy
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field

# Initialize the FirecrawlApp with your API key
app = FirecrawlApp(api_key='your_api_key')

class ExtractSchema(BaseModel):
    company_mission: str
    supports_sso: bool
    is_open_source: bool
    is_in_yc: bool

data = app.scrape_url('https://docs.firecrawl.dev/', {
    'formats': ['json'],
    'jsonOptions': {
        'schema': ExtractSchema.model_json_schema(),
    }
})
print(data["json"])
Output:

JSON

Copy
{
    "success": true,
    "data": {
      "json": {
        "company_mission": "Train a secure AI on your technical resources that answers customer and employee questions so your team doesn't have to",
        "supports_sso": true,
        "is_open_source": false,
        "is_in_yc": true
      },
      "metadata": {
        "title": "Mendable",
        "description": "Mendable allows you to easily build AI chat applications. Ingest, customize, then deploy with one line of code anywhere you want. Brought to you by SideGuide",
        "robots": "follow, index",
        "ogTitle": "Mendable",
        "ogDescription": "Mendable allows you to easily build AI chat applications. Ingest, customize, then deploy with one line of code anywhere you want. Brought to you by SideGuide",
        "ogUrl": "https://docs.firecrawl.dev/",
        "ogImage": "https://docs.firecrawl.dev/mendable_new_og1.png",
        "ogLocaleAlternate": [],
        "ogSiteName": "Mendable",
        "sourceURL": "https://docs.firecrawl.dev/"
      },
    }
}
​
Extracting without schema (New)
You can now extract without a schema by just passing a prompt to the endpoint. The llm chooses the structure of the data.


cURL

Copy
curl -X POST https://api.firecrawl.dev/v1/scrape \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev/",
      "formats": ["json"],
      "jsonOptions": {
        "prompt": "Extract the company mission from the page."
      }
    }'
Output:

JSON

Copy
{
    "success": true,
    "data": {
      "json": {
        "company_mission": "Train a secure AI on your technical resources that answers customer and employee questions so your team doesn't have to",
      },
      "metadata": {
        "title": "Mendable",
        "description": "Mendable allows you to easily build AI chat applications. Ingest, customize, then deploy with one line of code anywhere you want. Brought to you by SideGuide",
        "robots": "follow, index",
        "ogTitle": "Mendable",
        "ogDescription": "Mendable allows you to easily build AI chat applications. Ingest, customize, then deploy with one line of code anywhere you want. Brought to you by SideGuide",
        "ogUrl": "https://docs.firecrawl.dev/",
        "ogImage": "https://docs.firecrawl.dev/mendable_new_og1.png",
        "ogLocaleAlternate": [],
        "ogSiteName": "Mendable",
        "sourceURL": "https://docs.firecrawl.dev/"
      },
    }
}
​
Extraction (v0)

Python

JavaScript

Go

Rust

cURL

Copy

app = FirecrawlApp(version="v0")

class ArticleSchema(BaseModel):
    title: str
    points: int 
    by: str
    commentsURL: str

class TopArticlesSchema(BaseModel):
top: List[ArticleSchema] = Field(..., max_items=5, description="Top 5 stories")

data = app.scrape_url('https://news.ycombinator.com', {
'extractorOptions': {
'extractionSchema': TopArticlesSchema.model_json_schema(),
'mode': 'llm-extraction'
},
'pageOptions':{
'onlyMainContent': True
}
})
print(data["llm_extraction"])
​
Interacting with the page with Actions
Firecrawl allows you to perform various actions on a web page before scraping its content. This is particularly useful for interacting with dynamic content, navigating through pages, or accessing content that requires user interaction.

Here is an example of how to use actions to navigate to google.com, search for Firecrawl, click on the first result, and take a screenshot.

It is important to almost always use the wait action before/after executing other actions to give enough time for the page to load.

​
Example

Python

Node

cURL

Copy
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape a website:
scrape_result = app.scrape_url('firecrawl.dev', 
    params={
        'formats': ['markdown', 'html'], 
        'actions': [
            {"type": "wait", "milliseconds": 2000},
            {"type": "click", "selector": "textarea[title=\"Search\"]"},
            {"type": "wait", "milliseconds": 2000},
            {"type": "write", "text": "firecrawl"},
            {"type": "wait", "milliseconds": 2000},
            {"type": "press", "key": "ENTER"},
            {"type": "wait", "milliseconds": 3000},
            {"type": "click", "selector": "h3"},
            {"type": "wait", "milliseconds": 3000},
            {"type": "scrape"},
            {"type": "screenshot"}
        ]
    }
)
print(scrape_result)
​
Output

JSON

Copy
{
  "success": true,
  "data": {
    "markdown": "Our first Launch Week is over! [See the recap 🚀](blog/firecrawl-launch-week-1-recap)...",
    "actions": {
      "screenshots": [
        "https://alttmdsdujxrfnakrkyi.supabase.co/storage/v1/object/public/media/screenshot-75ef2d87-31e0-4349-a478-fb432a29e241.png"
      ],
      "scrapes": [
        {
          "url": "https://www.firecrawl.dev/",
          "html": "<html><body><h1>Firecrawl</h1></body></html>"
        }
      ]
    },
    "metadata": {
      "title": "Home - Firecrawl",
      "description": "Firecrawl crawls and converts any website into clean markdown.",
      "language": "en",
      "keywords": "Firecrawl,Markdown,Data,Mendable,Langchain",
      "robots": "follow, index",
      "ogTitle": "Firecrawl",
      "ogDescription": "Turn any website into LLM-ready data.",
      "ogUrl": "https://www.firecrawl.dev/",
      "ogImage": "https://www.firecrawl.dev/og.png?123",
      "ogLocaleAlternate": [],
      "ogSiteName": "Firecrawl",
      "sourceURL": "http://google.com",
      "statusCode": 200
    }
  }
}
​
Launch Week II (New)
Check out what’s new coming to Firecrawl in Launch Week II (Oct 28th - Nov 3rd)

​
Day 7 - Faster Markdown Parsing
We’ve rebuilt our Markdown parser from the ground up with a focus on speed and performance. This enhancement ensures that your web scraping tasks are more efficient and deliver higher-quality results.

​
What’s New?
Speed Improvements: Experience parsing speeds up to 4 times faster than before, allowing for quicker data processing and reduced waiting times.
Enhanced Reliability: Our new parser handles a wider range of HTML content more gracefully, reducing errors and improving consistency.
Cleaner Markdown Output: Get cleaner and more readable Markdown, making your data easier to work with and integrate into your workflows.
​
Day 6 - Mobile Scraping (+ Mobile Screenshots)
Firecrawl now introduces mobile device emulation for both scraping and screenshots, empowering you to interact with sites as if from a mobile device. This feature is essential for testing mobile-specific content, understanding responsive design, and gaining insights from mobile-specific elements.

​
Why Mobile Scraping?
Mobile-first experiences are increasingly common, and this feature enables you to:

Take high-fidelity mobile screenshots for a more accurate representation of how a site appears on mobile.
Test and verify mobile layouts and UI elements, ensuring the accuracy of your scraping results for responsive websites.
Scrape mobile-only content, gaining access to information or layouts that vary from desktop versions.
​
Usage
To activate mobile scraping, simply add "mobile": true in your request, which will enable Firecrawl’s mobile emulation mode.


Python

Node

cURL

Copy
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape a website:
scrape_result = app.scrape_url('google.com', 
    params={
        'formats': ['markdown', 'html'], 
        'mobile': true
    }
)
print(scrape_result)
For further details, including additional configuration options, visit the API Reference.

​
Day 5 - Actions (2 new actions)
Firecrawl allows you to perform various actions on a web page before scraping its content. This is particularly useful for interacting with dynamic content, navigating through pages, or accessing content that requires user interaction.

We’re excited to introduce two powerful new actions:

Scrape: Capture the current page content at any point during your interaction sequence, returning both URL and HTML.
Wait for Selector: Wait for a specific element to appear on the page before proceeding, ensuring more reliable automation.

Copy
actions = [
    {"type": "scrape"},
    {"type": "wait", "selector": "#my-element"},
]
Here is an example of how to use actions to navigate to google.com, search for Firecrawl, click on the first result, scrape the current page content, and take a screenshot.

For more precise control, you can now use {type: "wait", selector: "#my-element"} to wait for a specific element to appear on the page.

​
Example

Python

Node

cURL

Copy
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape a website:
scrape_result = app.scrape_url('firecrawl.dev', 
    params={
        'formats': ['markdown', 'html'], 
        'actions': [
            {"type": "wait", "milliseconds": 2000},
            {"type": "click", "selector": "textarea[title=\"Search\"]"},
            {"type": "wait", "milliseconds": 2000},
            {"type": "write", "text": "firecrawl"},
            {"type": "wait", "milliseconds": 2000},
            {"type": "press", "key": "ENTER"},
            {"type": "wait", "milliseconds": 3000},
            {"type": "click", "selector": "h3"},
            {"type": "wait", "milliseconds": 3000},
            {"type": "scrape"},
            {"type": "screenshot"}
        ]
    }
)
print(scrape_result)
​
Output

JSON

Copy
{
  "success": true,
  "data": {
    "markdown": "Our first Launch Week is over! [See the recap 🚀](blog/firecrawl-launch-week-1-recap)...",
    "actions": {
      "screenshots": [
        "https://alttmdsdujxrfnakrkyi.supabase.co/storage/v1/object/public/media/screenshot-75ef2d87-31e0-4349-a478-fb432a29e241.png"
      ],
      "scrapes": [
        {
          "url": "https://www.firecrawl.dev/",
          "html": "<html><body><h1>Firecrawl</h1></body></html>"
        }
      ]
    },
    "metadata": {
      "title": "Home - Firecrawl",
      "description": "Firecrawl crawls and converts any website into clean markdown.",
      "language": "en",
      "keywords": "Firecrawl,Markdown,Data,Mendable,Langchain",
      "robots": "follow, index",
      "ogTitle": "Firecrawl",
      "ogDescription": "Turn any website into LLM-ready data.",
      "ogUrl": "https://www.firecrawl.dev/",
      "ogImage": "https://www.firecrawl.dev/og.png?123",
      "ogLocaleAlternate": [],
      "ogSiteName": "Firecrawl",
      "sourceURL": "http://google.com",
      "statusCode": 200
    }
  }
}
For more details about the actions parameters, refer to the API Reference.

​
Day 4 - Advanced iframe scraping
We’re excited to announce comprehensive iframe scraping support in Firecrawl. Our scraper can now seamlessly handle nested iframes, dynamically loaded content, and cross-origin frames - solving one of web scraping’s most challenging technical hurdles.

​
Technical Innovation
Firecrawl now implements:

Recursive iframe traversal and content extraction
Cross-origin iframe handling with proper security context management
Smart automatic wait for iframe content to load
Support for dynamically injected iframes
Proper handling of sandboxed iframes
​
Why it matters
Many modern websites use iframes for:

Embedded content and widgets
Payment forms and secure inputs
Third-party integrations
Advertisement frames
Social media embeds
Previously, these elements were often black boxes in scraping results. Now, you get complete access to iframe content just like any other part of the page.

​
Usage
No additional configuration needed! The iframe scraping happens automatically when you use any of our scraping or crawling endpoints. Whether you’re using /scrape for single pages or /crawl for entire websites, iframe content will be seamlessly integrated into your results.

​
Day 3 - Credit Packs
Credit Packs allow you to you can easily top up your plan if your running low. Additionally, we now offer Auto Recharge, which automatically recharges your account when you’re approaching your limit. To enable visit the pricing page at https://www.firecrawl.dev/pricing

​
Credit Packs
Flexible monthly credit boosts for your projects.

$9/mo for 1000 credits
Add to any existing plan
Choose the amount you need
​
Auto Recharge Credits
Automatically top up your account when credits run low.

$11 per 1000 credits
Enable auto recharge with any subscription plan
​
Day 2 - Geolocation
Introducing location and language settings for scraping requests. Specify country and preferred languages to get relevant content based on your target location and language preferences.

​
How it works
When you specify the location settings, Firecrawl will use an appropriate proxy if available and emulate the corresponding language and timezone settings. By default, the location is set to ‘US’ if not specified.

​
Usage
To use the location and language settings, include the location object in your request body with the following properties:

country: ISO 3166-1 alpha-2 country code (e.g., ‘US’, ‘AU’, ‘DE’, ‘JP’). Defaults to ‘US’.
languages: An array of preferred languages and locales for the request in order of priority. Defaults to the language of the specified location.

Python

Node

cURL

Copy
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape a website:
scrape_result = app.scrape_url('airbnb.com', 
    params={
        'formats': ['markdown', 'html'], 
        'location': {
            'country': 'BR',
            'languages': ['pt-BR']
        }
    }
)
print(scrape_result)
​
Day 1 - Batch Scrape
You can now scrape multiple URLs at the same time with our new batch endpoint. Ideal for when you don’t need the scraping results immediately.

​
How it works
It is very similar to how the /crawl endpoint works. It submits a batch scrape job and returns a job ID to check the status of the batch scrape.

The sdk provides 2 methods, synchronous and asynchronous. The synchronous method will return the results of the batch scrape job, while the asynchronous method will return a job ID that you can use to check the status of the batch scrape.

​
Usage

Python

Node

cURL

Copy
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape multiple websites:
batch_scrape_result = app.batch_scrape_urls(['firecrawl.dev', 'mendable.ai'], {'formats': ['markdown', 'html']})
print(batch_scrape_result)

# Or, you can use the asynchronous method:
batch_scrape_job = app.async_batch_scrape_urls(['firecrawl.dev', 'mendable.ai'], {'formats': ['markdown', 'html']})
print(batch_scrape_job)

# (async) You can then use the job ID to check the status of the batch scrape:
batch_scrape_status = app.check_batch_scrape_status(batch_scrape_job['id'])
print(batch_scrape_status)
​
Response
If you’re using the sync methods from the SDKs, it will return the results of the batch scrape job. Otherwise, it will return a job ID that you can use to check the status of the batch scrape.

​
Synchronous
Completed

Copy
{
  "status": "completed",
  "total": 36,
  "completed": 36,
  "creditsUsed": 36,
  "expiresAt": "2024-00-00T00:00:00.000Z",
  "next": "https://api.firecrawl.dev/v1/batch/scrape/123-456-789?skip=26",
  "data": [
    {
      "markdown": "[Firecrawl Docs home page![light logo](https://mintlify.s3-us-west-1.amazonaws.com/firecrawl/logo/light.svg)!...",
      "html": "<!DOCTYPE html><html lang=\"en\" class=\"js-focus-visible lg:[--scroll-mt:9.5rem]\" data-js-focus-visible=\"\">...",
      "metadata": {
        "title": "Build a 'Chat with website' using Groq Llama 3 | Firecrawl",
        "language": "en",
        "sourceURL": "https://docs.firecrawl.dev/learn/rag-llama3",
        "description": "Learn how to use Firecrawl, Groq Llama 3, and Langchain to build a 'Chat with your website' bot.",
        "ogLocaleAlternate": [],
        "statusCode": 200
      }
    },
    ...
  ]
}
​
Asynchronous
You can then use the job ID to check the status of the batch scrape by calling the /batch/scrape/{id} endpoint. This endpoint is meant to be used while the job is still running or right after it has completed as batch scrape jobs expire after 24 hours.


Copy
{
  "success": true,
  "id": "123-456-789",
  "url": "https://api.firecrawl.dev/v1/batch/scrape/123-456-789"
}

Welcome to V1
Firecrawl allows you to turn entire websites into LLM-ready markdown

Firecrawl V1 is here! With that we introduce a more reliable and developer friendly API.

Here is what’s new:

Output Formats for /scrape. Choose what formats you want your output in.
New /map endpoint for getting most of the URLs of a webpage.
Developer friendly API for /crawl/{id} status.
2x Rate Limits for all plans.
Go SDK and Rust SDK
Teams support
API Key Management in the dashboard.
onlyMainContent is now default to true.
/crawl webhooks and websocket support.
​
Scrape Formats
You can now choose what formats you want your output in. You can specify multiple output formats. Supported formats are:

Markdown (markdown)
HTML (html)
Raw HTML (rawHtml) (with no modifications)
Screenshot (screenshot or screenshot@fullPage)
Links (links)
Extract (extract) - structured output
Output keys will match the format you choose.


Python

Node

Go

Rust

cURL

Copy
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape a website:
scrape_result = app.scrape_url('firecrawl.dev', params={'formats': ['markdown', 'html']})
print(scrape_result)
​
Response
SDKs will return the data object directly. cURL will return the payload exactly as shown below.


Copy
{
  "success": true,
  "data" : {
    "markdown": "Launch Week I is here! [See our Day 2 Release 🚀](https://www.firecrawl.dev/blog/launch-week-i-day-2-doubled-rate-limits)[💥 Get 2 months free...",
    "html": "<!DOCTYPE html><html lang=\"en\" class=\"light\" style=\"color-scheme: light;\"><body class=\"__variable_36bd41 __variable_d7dc5d font-inter ...",
    "metadata": {
      "title": "Home - Firecrawl",
      "description": "Firecrawl crawls and converts any website into clean markdown.",
      "language": "en",
      "keywords": "Firecrawl,Markdown,Data,Mendable,Langchain",
      "robots": "follow, index",
      "ogTitle": "Firecrawl",
      "ogDescription": "Turn any website into LLM-ready data.",
      "ogUrl": "https://www.firecrawl.dev/",
      "ogImage": "https://www.firecrawl.dev/og.png?123",
      "ogLocaleAlternate": [],
      "ogSiteName": "Firecrawl",
      "sourceURL": "https://firecrawl.dev",
      "statusCode": 200
    }
  }
}
​
Introducing /map (Alpha)
The easiest way to go from a single url to a map of the entire website.

​
Usage

Python

Node

Go

Rust

cURL

Copy
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Map a website:
map_result = app.map_url('https://firecrawl.dev')
print(map_result)
​
Response
SDKs will return the data object directly. cURL will return the payload exactly as shown below.


Copy
{
  "status": "success",
  "links": [
    "https://firecrawl.dev",
    "https://www.firecrawl.dev/pricing",
    "https://www.firecrawl.dev/blog",
    "https://www.firecrawl.dev/playground",
    "https://www.firecrawl.dev/smart-crawl",
    ...
  ]
}
​
WebSockets
To crawl a website with WebSockets, use the Crawl URL and Watch method.


Python

Node

Copy
# inside an async function...
nest_asyncio.apply()

# Define event handlers
def on_document(detail):
    print("DOC", detail)

def on_error(detail):
    print("ERR", detail['error'])

def on_done(detail):
    print("DONE", detail['status'])

    # Function to start the crawl and watch process
async def start_crawl_and_watch():
    # Initiate the crawl job and get the watcher
    watcher = app.crawl_url_and_watch('firecrawl.dev', { 'excludePaths': ['blog/*'], 'limit': 5 })

    # Add event listeners
    watcher.add_event_listener("document", on_document)
    watcher.add_event_listener("error", on_error)
    watcher.add_event_listener("done", on_done)

    # Start the watcher
    await watcher.connect()

# Run the event loop
await start_crawl_and_watch()
​
Extract format
LLM extraction is now available in v1 under the extract format. To extract structured from a page, you can pass a schema to the endpoint or just provide a prompt.


Python

Node

cURL

Copy
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field

# Initialize the FirecrawlApp with your API key
app = FirecrawlApp(api_key='your_api_key')

class ExtractSchema(BaseModel):
    company_mission: str
    supports_sso: bool
    is_open_source: bool
    is_in_yc: bool

data = app.scrape_url('https://docs.firecrawl.dev/', {
    'formats': ['json'],
    'jsonOptions': {
        'schema': ExtractSchema.model_json_schema(),
    }
})
print(data["json"])
Output:

JSON

Copy
{
    "success": true,
    "data": {
      "json": {
        "company_mission": "Train a secure AI on your technical resources that answers customer and employee questions so your team doesn't have to",
        "supports_sso": true,
        "is_open_source": false,
        "is_in_yc": true
      },
      "metadata": {
        "title": "Mendable",
        "description": "Mendable allows you to easily build AI chat applications. Ingest, customize, then deploy with one line of code anywhere you want. Brought to you by SideGuide",
        "robots": "follow, index",
        "ogTitle": "Mendable",
        "ogDescription": "Mendable allows you to easily build AI chat applications. Ingest, customize, then deploy with one line of code anywhere you want. Brought to you by SideGuide",
        "ogUrl": "https://docs.firecrawl.dev/",
        "ogImage": "https://docs.firecrawl.dev/mendable_new_og1.png",
        "ogLocaleAlternate": [],
        "ogSiteName": "Mendable",
        "sourceURL": "https://docs.firecrawl.dev/"
      },
    }
}
​
Extracting without schema (New)
You can now extract without a schema by just passing a prompt to the endpoint. The llm chooses the structure of the data.


cURL

Copy
curl -X POST https://api.firecrawl.dev/v1/scrape \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev/",
      "formats": ["json"],
      "jsonOptions": {
        "prompt": "Extract the company mission from the page."
      }
    }'
Output:

JSON

Copy
{
    "success": true,
    "data": {
      "json": {
        "company_mission": "Train a secure AI on your technical resources that answers customer and employee questions so your team doesn't have to",
      },
      "metadata": {
        "title": "Mendable",
        "description": "Mendable allows you to easily build AI chat applications. Ingest, customize, then deploy with one line of code anywhere you want. Brought to you by SideGuide",
        "robots": "follow, index",
        "ogTitle": "Mendable",
        "ogDescription": "Mendable allows you to easily build AI chat applications. Ingest, customize, then deploy with one line of code anywhere you want. Brought to you by SideGuide",
        "ogUrl": "https://docs.firecrawl.dev/",
        "ogImage": "https://docs.firecrawl.dev/mendable_new_og1.png",
        "ogLocaleAlternate": [],
        "ogSiteName": "Mendable",
        "sourceURL": "https://docs.firecrawl.dev/"
      },
    }
}
​
New Crawl Webhook
You can now pass a webhook parameter to the /crawl endpoint. This will send a POST request to the URL you specify when the crawl is started, updated and completed.

The webhook will now trigger for every page crawled and not just the whole result at the end.

cURL

Copy
curl -X POST https://api.firecrawl.dev/v1/crawl \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev",
      "limit": 100,
      "webhook": "https://example.com/webhook"
    }'
​
Webhook Events
There are now 4 types of events:

crawl.started - Triggered when the crawl is started.
crawl.page - Triggered for every page crawled.
crawl.completed - Triggered when the crawl is completed to let you know it’s done.
crawl.failed - Triggered when the crawl fails.
​
Webhook Response
success - If the webhook was successful in crawling the page correctly.
type - The type of event that occurred.
id - The ID of the crawl.
data - The data that was scraped (Array). This will only be non empty on crawl.page and will contain 1 item if the page was scraped successfully. The response is the same as the /scrape endpoint.
error - If the webhook failed, this will contain the error message.
​
Migrating from V0
⚠️ Deprecation Notice: V0 endpoints will be deprecated on April 1st, 2025. Please migrate to V1 endpoints before then to ensure uninterrupted service.

​
/scrape endpoint
The updated /scrape endpoint has been redesigned for enhanced reliability and ease of use. The structure of the new /scrape request body is as follows:


Copy
{
  "url": "<string>",
  "formats": ["markdown", "html", "rawHtml", "links", "screenshot", "json"],
  "includeTags": ["<string>"],
  "excludeTags": ["<string>"],
  "headers": { "<key>": "<value>" },
  "waitFor": 123,
  "timeout": 123
}
​
Formats
You can now choose what formats you want your output in. You can specify multiple output formats. Supported formats are:

Markdown (markdown)
HTML (html)
Raw HTML (rawHtml) (with no modifications)
Screenshot (screenshot or screenshot@fullPage)
Links (links)
JSON (json)
By default, the output will be include only the markdown format.

​
Details on the new request body
The table below outlines the changes to the request body parameters for the /scrape endpoint in V1.

Parameter	Change	Description
onlyIncludeTags	Moved and Renamed	Moved to root level. And renamed to includeTags.
removeTags	Moved and Renamed	Moved to root level. And renamed to excludeTags.
onlyMainContent	Moved	Moved to root level. true by default.
waitFor	Moved	Moved to root level.
headers	Moved	Moved to root level.
parsePDF	Moved	Moved to root level.
extractorOptions	No Change	
timeout	No Change	
pageOptions	Removed	No need for pageOptions parameter. The scrape options were moved to root level.
replaceAllPathsWithAbsolutePaths	Removed	replaceAllPathsWithAbsolutePaths is not needed anymore. Every path is now default to absolute path.
includeHtml	Removed	add "html" to formats instead.
includeRawHtml	Removed	add "rawHtml" to formats instead.
screenshot	Removed	add "screenshot" to formats instead.
fullPageScreenshot	Removed	add "screenshot@fullPage" to formats instead.
extractorOptions	Removed	Use "extract" format instead with extract object.
The new extract format is described in the llm-extract section.

​
/crawl endpoint
We’ve also updated the /crawl endpoint on v1. Check out the improved body request below:


Copy
{
  "url": "<string>",
  "excludePaths": ["<string>"],
  "includePaths": ["<string>"],
  "maxDepth": 2,
  "ignoreSitemap": true,
  "limit": 10,
  "allowBackwardLinks": true,
  "allowExternalLinks": true,
  "scrapeOptions": {
    // same options as in /scrape
    "formats": ["markdown", "html", "rawHtml", "screenshot", "links"],
    "headers": { "<key>": "<value>" },
    "includeTags": ["<string>"],
    "excludeTags": ["<string>"],
    "onlyMainContent": true,
    "waitFor": 123
  }
}
​
Details on the new request body
The table below outlines the changes to the request body parameters for the /crawl endpoint in V1.

Parameter	Change	Description
pageOptions	Renamed	Renamed to scrapeOptions.
includes	Moved and Renamed	Moved to root level. Renamed to includePaths.
excludes	Moved and Renamed	Moved to root level. Renamed to excludePaths.
allowBackwardCrawling	Moved and Renamed	Moved to root level. Renamed to allowBackwardLinks.
allowExternalLinks	Moved	Moved to root level.
maxDepth	Moved	Moved to root level.
ignoreSitemap	Moved	Moved to root level.
limit	Moved	Moved to root level.
crawlerOptions	Removed	No need for crawlerOptions parameter. The crawl options were moved to root level.
timeout	Removed	Use timeout in scrapeOptions instead.

API参考：
https://docs.firecrawl.dev/api-reference/endpoint/map


Get Started
Advanced Scraping Guide
Learn how to improve your Firecrawl scraping with advanced options.

This guide will walk you through the different endpoints of Firecrawl and how to use them fully with all its parameters.

​
Basic scraping with Firecrawl (/scrape)
To scrape a single page and get clean markdown content, you can use the /scrape endpoint.


Python

JavaScript

Go

Rust

cURL

Copy
# pip install firecrawl-py

from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="YOUR_API_KEY")

content = app.scrape_url("https://docs.firecrawl.dev")
​
Scraping PDFs
Firecrawl supports scraping PDFs by default. You can use the /scrape endpoint to scrape a PDF link and get the text content of the PDF. You can disable this by setting parsePDF to false.

​
Scrape Options
When using the /scrape endpoint, you can customize the scraping behavior with many parameters. Here are the available options:

​
Setting the content formats on response with formats
Type: array
Enum: ["markdown", "links", "html", "rawHtml", "screenshot", "json"]
Description: Specify the formats to include in the response. Options include:
markdown: Returns the scraped content in Markdown format.
links: Includes all hyperlinks found on the page.
html: Provides the content in HTML format.
rawHtml: Delivers the raw HTML content, without any processing.
screenshot: Includes a screenshot of the page as it appears in the browser.
json: Extracts structured information from the page using the LLM.
Default: ["markdown"]
​
Getting the full page content as markdown with onlyMainContent
Type: boolean
Description: By default, the scraper will only return the main content of the page, excluding headers, navigation bars, footers, etc. Set this to false to return the full page content.
Default: true
​
Setting the tags to include with includeTags
Type: array
Description: Specify the HTML tags, classes and ids to include in the response.
Default: undefined
​
Setting the tags to exclude with excludeTags
Type: array
Description: Specify the HTML tags, classes and ids to exclude from the response.
Default: undefined
​
Waiting for the page to load with waitFor
Type: integer
Description: To be used only as a last resort. Wait for a specified amount of milliseconds for the page to load before fetching content.
Default: 0
​
Setting the maximum timeout
Type: integer
Description: Set the maximum duration in milliseconds that the scraper will wait for the page to respond before aborting the operation.
Default: 30000 (30 seconds)
​
Example Usage

Copy
curl -X POST https://api.firecrawl.dev/v1/scrape \
    -H '
    Content-Type: application/json' \
    -H 'Authorization : Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev",
      "formats": ["markdown", "links", "html", "rawHtml", "screenshot"],
      "includeTags": ["h1", "p", "a", ".main-content"],
      "excludeTags": ["#ad", "#footer"],
      "onlyMainContent": false,
      "waitFor": 1000,
      "timeout": 15000
    }'
In this example, the scraper will:

Return the full page content as markdown.
Include the markdown, raw HTML, HTML, links and screenshot in the response.
The response will include only the HTML tags <h1>, <p>, <a>, and elements with the class .main-content, while excluding any elements with the IDs #ad and #footer.
Wait for 1000 milliseconds (1 second) for the page to load before fetching the content.
Set the maximum duration of the scrape request to 15000 milliseconds (15 seconds).
Here is the API Reference for it: Scrape Endpoint Documentation

​
Extractor Options
When using the /scrape endpoint, you can specify options for extracting structured information from the page content using the extract parameter. Here are the available options:

​
Using the LLM Extraction
​
schema
Type: object
Required: False if prompt is provided
Description: The schema for the data to be extracted. This defines the structure of the extracted data.
​
system prompt
Type: string
Required: False
Description: System prompt for the LLM.
​
prompt
Type: string
Required: False if schema is provided
Description: A prompt for the LLM to extract the data in the correct structure.
Example: "Extract the features of the product"
​
Example Usage

Copy
curl -X POST https://api.firecrawl.dev/v0/scrape \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://firecrawl.dev",
      "formats": ["markdown", "json"],
      "json": {
        "prompt": "Extract the features of the product"
      }
    }'

Copy
{
  "success": true,
  "data": {
    "content": "Raw Content",
    "metadata": {
      "title": "Mendable",
      "description": "Mendable allows you to easily build AI chat applications. Ingest, customize, then deploy with one line of code anywhere you want. Brought to you by SideGuide",
      "robots": "follow, index",
      "ogTitle": "Mendable",
      "ogDescription": "Mendable allows you to easily build AI chat applications. Ingest, customize, then deploy with one line of code anywhere you want. Brought to you by SideGuide",
      "ogUrl": "https://docs.firecrawl.dev/",
      "ogImage": "https://docs.firecrawl.dev/mendable_new_og1.png",
      "ogLocaleAlternate": [],
      "ogSiteName": "Mendable",
      "sourceURL": "https://docs.firecrawl.dev/",
      "statusCode": 200
    },
    "extract": {
      "product": "Firecrawl",
      "features": {
        "general": {
          "description": "Turn websites into LLM-ready data.",
          "openSource": true,
          "freeCredits": 500,
          "useCases": [
            "AI applications",
            "Data science",
            "Market research",
            "Content aggregation"
          ]
        },
        "crawlingAndScraping": {
          "crawlAllAccessiblePages": true,
          "noSitemapRequired": true,
          "dynamicContentHandling": true,
          "dataCleanliness": {
            "process": "Advanced algorithms",
            "outputFormat": "Markdown"
          }
        },
        ...
      }
    }
  }
}
​
Actions
When using the /scrape endpoint, Firecrawl allows you to perform various actions on a web page before scraping its content. This is particularly useful for interacting with dynamic content, navigating through pages, or accessing content that requires user interaction.

​
Available Actions
​
wait
Type: object
Description: Wait for a specified amount of milliseconds.
Properties:
type: "wait"
milliseconds: Number of milliseconds to wait.
Example:

Copy
{
  "type": "wait",
  "milliseconds": 2000
}
​
screenshot
Type: object
Description: Take a screenshot.
Properties:
type: "screenshot"
fullPage: Should the screenshot be full-page or viewport sized? (default: false)
Example:

Copy
{
  "type": "screenshot",
  "fullPage": true
}
​
click
Type: object
Description: Click on an element.
Properties:
type: "click"
selector: Query selector to find the element by.
Example:

Copy
{
  "type": "click",
  "selector": "#load-more-button"
}
​
write
Type: object
Description: Write text into an input field.
Properties:
type: "write"
text: Text to type.
selector: Query selector for the input field.
Example:

Copy
{
  "type": "write",
  "text": "Hello, world!",
  "selector": "#search-input"
}
​
press
Type: object
Description: Press a key on the page.
Properties:
type: "press"
key: Key to press.
Example:

Copy
{
  "type": "press",
  "key": "Enter"
}
​
scroll
Type: object
Description: Scroll the page.
Properties:
type: "scroll"
direction: Direction to scroll ("up" or "down").
amount: Amount to scroll in pixels.
Example:

Copy
{
  "type": "scroll",
  "direction": "down",
  "amount": 500
}
For more details about the actions parameters, refer to the API Reference.

​
Crawling Multiple Pages
To crawl multiple pages, you can use the /crawl endpoint. This endpoint allows you to specify a base URL you want to crawl and all accessible subpages will be crawled.


Copy
curl -X POST https://api.firecrawl.dev/v1/crawl \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev"
    }'
Returns a id


Copy
{ "id": "1234-5678-9101" }
​
Check Crawl Job
Used to check the status of a crawl job and get its result.


Copy
curl -X GET https://api.firecrawl.dev/v1/crawl/1234-5678-9101 \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY'
​
Pagination/Next URL
If the content is larger than 10MB or if the crawl job is still running, the response will include a next parameter. This parameter is a URL to the next page of results. You can use this parameter to get the next page of results.

​
Crawler Options
When using the /crawl endpoint, you can customize the crawling behavior with request body parameters. Here are the available options:

​
includePaths
Type: array
Description: URL patterns to include in the crawl. Only URLs matching these patterns will be crawled.
Example: ["/blog/*", "/products/*"]
​
excludePaths
Type: array
Description: URL patterns to exclude from the crawl. URLs matching these patterns will be skipped.
Example: ["/admin/*", "/login/*"]
​
maxDepth
Type: integer
Description: Maximum depth to crawl relative to the entered URL. A maxDepth of 0 scrapes only the entered URL. A maxDepth of 1 scrapes the entered URL and all pages one level deep. A maxDepth of 2 scrapes the entered URL and all pages up to two levels deep. Higher values follow the same pattern.
Example: 2
​
limit
Type: integer
Description: Maximum number of pages to crawl.
Default: 10000
​
allowBackwardLinks
Type: boolean
Description: This option permits the crawler to navigate to URLs that are higher in the directory structure than the base URL. For instance, if the base URL is example.com/blog/topic, enabling this option allows crawling to pages like example.com/blog or example.com, which are backward in the path hierarchy relative to the base URL.
Default: false
​
allowExternalLinks
Type: boolean
Description: This option allows the crawler to follow links that point to external domains. Be careful with this option, as it can cause the crawl to stop only based only on thelimit and maxDepth values.
Default: false
​
scrapeOptions
As part of the crawler options, you can also specify the scrapeOptions parameter. This parameter allows you to customize the scraping behavior for each page.

Type: object
Description: Options for the scraper.
Example: {"formats": ["markdown", "links", "html", "rawHtml", "screenshot"], "includeTags": ["h1", "p", "a", ".main-content"], "excludeTags": ["#ad", "#footer"], "onlyMainContent": false, "waitFor": 1000, "timeout": 15000}
Default: { "formats": ["markdown"] }
See: Scrape Options
​
Example Usage

Copy
curl -X POST https://api.firecrawl.dev/v1/crawl \
    -H 'Content-Type: application/json' \
    -H 'Authorization : Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev",
      "includePaths": ["/blog/*", "/products/*"],
      "excludePaths": ["/admin/*", "/login/*"],
      "maxDepth": 2,
      "limit": 1000
    }'
In this example, the crawler will:

Only crawl URLs that match the patterns /blog/* and /products/*.
Skip URLs that match the patterns /admin/* and /login/*.
Return the full document data for each page.
Crawl up to a maximum depth of 2.
Crawl a maximum of 1000 pages.
​
Mapping Website Links with /map
The /map endpoint is adept at identifying URLs that are contextually related to a given website. This feature is crucial for understanding a site’s contextual link environment, which can greatly aid in strategic site analysis and navigation planning.

​
Usage
To use the /map endpoint, you need to send a GET request with the URL of the page you want to map. Here is an example using curl:


Copy
curl -X POST https://api.firecrawl.dev/v1/map \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev"
    }'
This will return a JSON object containing links contextually related to the url.

​
Example Response

Copy
  {
    "success":true,
    "links":[
      "https://docs.firecrawl.dev",
      "https://docs.firecrawl.dev/api-reference/endpoint/crawl-delete",
      "https://docs.firecrawl.dev/api-reference/endpoint/crawl-get",
      "https://docs.firecrawl.dev/api-reference/endpoint/crawl-post",
      "https://docs.firecrawl.dev/api-reference/endpoint/map",
      "https://docs.firecrawl.dev/api-reference/endpoint/scrape",
      "https://docs.firecrawl.dev/api-reference/introduction",
      "https://docs.firecrawl.dev/articles/search-announcement",
      ...
    ]
  }
​
Map Options
​
search
Type: string
Description: Search for links containing specific text.
Example: "blog"
​
limit
Type: integer
Description: Maximum number of links to return.
Default: 100
​
ignoreSitemap
Type: boolean
Description: Ignore the website sitemap when crawling
Default: true
​
includeSubdomains
Type: boolean
Description: Include subdomains of the website
Default: false
Here is the API Reference for it: Map Endpoint Documentation