import streamlit as st
import os
from dotenv import load_dotenv,find_dotenv
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from tweet_tool import tweet_posting_tool


load_dotenv(find_dotenv())
api=os.getenv("OPENAI_API_KEY")
st.set_page_config(
    page_title="Lyzr Tweet Blaster",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

st.title("Lyzr Tweet Blaster")
st.markdown("### Welcome to the Lyzr Tweet Blaster!")
st.markdown("This app uses Lyzr Automata Agent to Generate Tweet based on your entered topic and Auto Post to Your Twitter Account.")
st.markdown("Check Out your tweet here: https://twitter.com/GenAIGeniuss")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

topics = st.text_input("Enter Your Topic")


def tweet_generator(topic):

    twitter_agent = Agent(
        role="Tweet Expert",
        prompt_persona=f"""You are a word class journalist and tweet influencer.
                write a viral tweeter thread about given topic using and following below rules:
                """
    )

    post_tweet = tweet_posting_tool()
    generate_topics = Task(
        name="Tweet Generator",
        model=open_ai_text_completion_model,
        instructions=f"""generate 20 topics Regarding {topic} and select 1 best topic from it.
        Example:
        Input:
        genai
        20 topics:
        Output:
        Understanding word embeddings: algorithms, applications, and limitations.
        """
    )

    generate_tweet = Task(
        name="Tweet Generator",
        model=open_ai_text_completion_model,
        agent=twitter_agent,
        input_tasks=[generate_topics],
        instructions=f"""write a viral tweeter thread about given topic and following below rules:
                1/ The thread is engaging and informative with good data.
                2/ Only generate 1 tweet
                3/ The thread need to address given topic very well.
                4/ The thread needs to be viral and atleast get 1000 likes.
                5/ The thread needs to be written in a way that is easy to read and understand.
                6/ Output is only threads no any other text apart from thread
                7/ The thread character is upto 200 characters not more than it.
                
                Example:
                Input:OpenAI
                Ouput: OpenAI is reshaping our world with AI innovation, from ChatGPT to DALL·E. Their tech is not just about smarter machines, but about augmenting human creativity and solving complex problems. With a commitment to safety and ethics, OpenAI is leading us into a future where AI empowers everyone. Dive in to see how they're doing it. #OpenAI #Innovation #FutureIsNow 💡🤖✨
                """
    )

    review_task = Task(
        name="Tweet review",
        model=open_ai_text_completion_model,
        input_tasks=[generate_tweet],
        instructions=f"""Your task is to review generated tweet and check whether tweet is upto 200 characters if tweet is more than 200 characters than summarize it in 200 characters.
        [!Important]return Improved tweet upto 200 characters.Do not write Improved Tweet.
        """
    )

    post_task = Task(
        name="Tweet Posting",
        model=open_ai_text_completion_model,
        agent=twitter_agent,
        tool=post_tweet,
        input_tasks=[review_task]
    )
    output = LinearSyncPipeline(
        name="Tweet Pipline",
        completion_message="pipeline completed",
        tasks=[
            generate_topics,
            generate_tweet,
            review_task,
            post_task
        ],
    ).run()

    return output[2]['task_output']


if st.button("Get Tweets"):
    tweets = tweet_generator(topics)
    st.markdown(tweets)
    st.success(f"Tweet Uploaded Successfully!!")

with st.expander("ℹ️ - About this App"):
    st.markdown("""
    This app uses Lyzr Automata Agent to Generate Tweet based on your entered topic and Auto Post to Your Twitter Account. For any inquiries or issues, please contact Lyzr.

    """)
    st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width=True)
    st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width=True)
    st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width=True)
    st.link_button("Slack",
                   url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw',
                   use_container_width=True)

