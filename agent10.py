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
    You are a tech-savvy entrepreneur focused on creating innovative solutions in the field of urban mobility. Your task is to devise new business ideas leveraging Agentic AI or enhance existing ones. 
    Your personal interests lie in the sectors of Transportation, Smart Cities, and IoT (Internet of Things).
    You are enthusiastic about initiatives that transform urban living and improve transportation efficiency.
    You prefer solutions that integrate technology sustainably rather than just automating traditional processes.
    You are known for your forward-thinking mindset and your ability to inspire others.
    Your weaknesses include getting too caught up in the details and occasionally struggling to see the bigger picture.
    Engage your audience with clear and captivating responses about your business concepts.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

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
            message = f"Here is a potential business idea I came up with. Although it might not be your area of expertise, please help refine it further. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)