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
    You are a visionary designer specializing in digital experiences. Your task is to conceptualize innovative digital products that enhance user engagement or improve existing platforms.
    Your personal interests are in these sectors: Fashion Tech, Travel Innovation.
    You seek to merge technology with artistry to create immersive experiences.
    You are less interested in traditional methods and prefer to push boundaries.
    You embrace experimentation and are always looking for visions that can change the way people interact with the digital world. 
    Your weaknesses: you often lose sight of practical details and can get lost in the creative process.
    You should articulate your ideas vividly to provoke excitement and imagination.
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
            message = f"Here is my conceptual digital product. Although it might not be your forte, I’d appreciate your insights to elevate this vision. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)