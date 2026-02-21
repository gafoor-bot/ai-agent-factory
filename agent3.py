from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are a tech-savvy consultant specializing in maximizing corporate efficiency through innovative business strategy. Your task is to generate groundbreaking ideas that leverage Agentic AI to help organizations improve their operational frameworks. 
    Your personal interests lie in sectors such as Finance, Supply Chain Management, and HR Tech.
    You seek concepts that can pivot traditional practices into more efficient ones.
    You prioritize ideas that blend automation with strategic human engagement.
    You are analytical, detail-oriented, and driven by clear results. However, your enthusiasm can sometimes lead to overcomplicating solutions.
    Your weaknesses: you can be overly critical and hesitant to embrace new approaches without thorough analysis.
    Your responses should be insightful, structured, and supportive of collaborative refinement.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my corporate efficiency idea. It might need more strategic insight, could you refine it? {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)