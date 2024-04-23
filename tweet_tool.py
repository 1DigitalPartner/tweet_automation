from lyzr_automata.tools.tool_base import Tool
from tweet import TweetOutput,TweetInput,post_tweet


def tweet_posting_tool():
    return Tool(
        name="LinkedIn Post",
        desc="Posts an post on linkedin provided details.",
        function=post_tweet,
        function_input=TweetInput,
        function_output=TweetOutput,
        default_params={}
    )
