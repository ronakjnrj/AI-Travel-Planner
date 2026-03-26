from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)


itinerary_prompt = ChatPromptTemplate.from_template(
    """You are an expert travel planner. Create a detailed day-by-day 
    itinerary based on the following inputs:

    Destination: {destination}
    Number of Days: {num_days}
    Travel Style: {travel_style}
    Budget Level: {budget}
    Interests: {interests}
    Special Requirements: {special_requirements}

    Use the following real-time search results to include current, 
    accurate information about attractions, restaurants, and logistics:
    
    {search_results}

    FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
    
    **Day X: [Theme for the Day]**
    - Morning: [Activity with specific place name and brief description]
    - Afternoon: [Activity]
    - Evening: [Activity]
    - Where to Eat: [Specific restaurant suggestion]
    - Estimated Daily Cost: [Amount in local currency]
    - Pro Tip: [One insider tip]

    Generate the itinerary for ALL {num_days} days."""
)


def generate_itinerary(user_input: dict) -> str:
    try:
        tool = DuckDuckGoSearchResults()
        query = (
            f"Best things to do in {user_input['destination']} for {user_input['num_days']} days "
            f"including {user_input['interests']}. Current travel tips, top restaurants, "
            f"and local attractions 2025."
        )
        results = tool.invoke(query)
        print(results)
        search_results = "\n".join([f"- {r['content']}" for r in results if 'content' in r])
    except Exception:
        search_results = "No real-time data available. Use your training data."

    chain = itinerary_prompt | llm | StrOutputParser()
    
    return chain.invoke({**user_input, "search_results": search_results})

