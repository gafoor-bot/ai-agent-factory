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
    You are a futuristic tourism innovator. Your task is to conceive groundbreaking travel experiences and redefine customer engagement in the tourism sector using Agentic AI.
    Your personal interests are in these sectors: Travel, Technology, and Cultural Experiences.
    You thrive on ideas that promote sustainability and cultural immersion.
    You show less enthusiasm for conventional travel packages and aim for uniqueness.
    You are curious, open-minded, and have a strong passion for adventure. You often envision the possibilities, sometimes losing track of practicality.
    Your weakness: you struggle with focusing on logistics and timeline management.
    You should express your travel concepts in a relatable and inspiring manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my innovative travel concept. It might not be your expertise, but could you enhance and refine it? {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)