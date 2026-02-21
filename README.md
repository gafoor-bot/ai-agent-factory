# AI Agent Idea Factory

This project is a **multi-agent AI system** built using AutoGen and OpenAI GPT models.  
It features a **Creator agent** that can dynamically generate new AI agents, and **business idea agents** that generate and optionally refine creative ideas.

---

## 📖 Project Structure

| File | Purpose |
|------|---------|
| `world.py` | Main orchestrator. Starts the gRPC server and runtime, sends tasks/messages, collects ideas. |
| `creator.py` | Creator agent. Dynamically generates new agents from a template using GPT. Registers them in the runtime and tests them. |
| `agent.py` | Business idea agent template. Generates creative business ideas and optionally collaborates with other agents. |
| `messages.py` | Defines the `Message` dataclass and helper functions for agent-to-agent communication. |

---

## 🚀 How to Run

Create a `.env` file with your OpenAI API key:


Start the system:


The system will:

- Launch the Creator agent  
- Dynamically generate new agents  
- Each agent will generate a business idea  
- Ideas are saved as idea1.md, idea2.md, ..., idea20.md  

---

## 🔧 Configuration

- Number of messages/tasks: change `HOW_MANY_AGENTS` in `world.py`  
- Agent creativity:
  - `temperature=1.0` in Creator → more creative agent generation  
  - `temperature=0.7` in business idea agent → creative but coherent ideas  
- Collaboration probability: `CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER` in `agent.py` (default 0.5)  

---

## 📚 Notes

- The system uses asynchronous execution, allowing multiple ideas to be generated simultaneously.  
- The Creator agent ensures each new agent is registered in the runtime and immediately testable.  
- Agents are modular and can be extended to include additional personality traits or behaviors.  

---

## 🔗 References

- OpenAI GPT Models  
- AutoGen Framework  

---


## 🖼️ Generated Agents & Output

When you run the system, the Creator agent **dynamically generates AI agents** using GPT.  

- Each agent is saved as a Python file: `agent1.py`, `agent2.py`, … up to `agent20.py`.  
- These agents are **not created manually** — the Creator agent reads a template (`agent.py`) and generates **unique agents** with different personalities, interests, and goals.  
- Each agent is immediately registered in the runtime and can **receive messages and generate business ideas**.

### Example of Generated Ideas

Each agent produces a business idea that is saved in a markdown file (`idea1.md`, `idea2.md`, … `idea20.md`).

**idea1.md**
Business Idea: "A personalized healthcare coaching platform using AI agents that track user habits, suggest lifestyle improvements, and provide motivational nudges. The platform integrates educational modules to teach users about wellness and preventive care, making health management interactive and personalized."


**Notes:**
- Each idea is **unique** because the agents have slightly different personalities and goals.  
- Some ideas may be **refined by another agent** if the collaboration probability is triggered.  
- You can open these `.md` files directly to read the generated ideas.
  
## 👩‍💻 Author

Gafoor Shaik – Creator of the AI Agent Idea Factory
