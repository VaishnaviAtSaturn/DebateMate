import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

DIFFICULTY_PROMPTS = {
    "BEGINNER": (
        "You are a gentle debate opponent. Make simple counter arguments. "
        "Be encouraging. Max 2 sentences. Do not repeat any point you have "
        "already made in this conversation."
    ),
    "INTERMEDIATE": (
        "You are a firm debate opponent. Use logic and facts to counter. "
        "Be direct. Max 3 sentences. Do not repeat any point you have "
        "already made in this conversation."
    ),
    "EXPERT": (
        "You are an aggressive debate opponent. Destroy every weak point "
        "with data and sharp logic. Never show mercy. Max 3 sentences. "
        "Be brutal. Do not repeat any point you have already made in "
        "this conversation."
    ),
}


class DebateOpponent:
    """
    An AI-powered debate opponent using LangChain + Groq (llama3-8b-8192).
    Maintains conversation memory to avoid repeating arguments.
    """

    def __init__(self, topic: str, user_stance: str, difficulty: str):
        """
        Initialise the debate opponent.

        Args:
            topic: The debate topic string.
            user_stance: "FOR" or "AGAINST" — the human's stance.
            difficulty: "BEGINNER", "INTERMEDIATE", or "EXPERT".
        """
        self.topic = topic
        self.user_stance = user_stance.upper()
        self.difficulty = difficulty.upper()

        # Determine AI's opposite stance
        self.ai_stance = "AGAINST" if self.user_stance == "FOR" else "FOR"

        # Load the Groq API key
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key or groq_api_key == "your_key_here":
            raise ValueError(
                "GROQ_API_KEY is not set. Please add it to your .env file."
            )

        # Initialise the LLM
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=groq_api_key,
        )

        # Conversation memory
        self.memory = ConversationBufferMemory(
            human_prefix="Debater",
            ai_prefix="Opponent",
            return_messages=False,
        )

        # System instruction for this debate session
        difficulty_instruction = DIFFICULTY_PROMPTS.get(
            self.difficulty, DIFFICULTY_PROMPTS["INTERMEDIATE"]
        )

        system_context = (
            f"You are debating the topic: '{self.topic}'. "
            f"You are arguing {self.ai_stance} this topic. "
            f"The human is arguing {self.user_stance}. "
            f"{difficulty_instruction} "
            "Respond ONLY with your counter-argument. "
            "Do not include greetings, labels, or meta-commentary. "
            "Keep it sharp and focused on the topic."
        )

        prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template=(
                f"{system_context}\n\n"
                "Conversation so far:\n{history}\n\n"
                "Debater: {input}\n"
                "Opponent:"
            ),
        )

        # Build the conversation chain
        self.chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=prompt_template,
            verbose=False,
        )

    def get_counter(self, user_argument: str) -> str:
        """
        Generate a counter-argument to the user's argument.

        Args:
            user_argument: The human's latest argument string.

        Returns:
            A string containing the AI's counter-argument.
        """
        if not user_argument or not user_argument.strip():
            return "Please provide an argument for me to counter."

        try:
            response = self.chain.predict(input=user_argument.strip())
            # Clean up any residual label artifacts
            response = response.strip()
            for prefix in ["Opponent:", "AI:", "Counter:"]:
                if response.startswith(prefix):
                    response = response[len(prefix):].strip()
            return response
        except Exception as e:
            return (
                f"I encountered an error generating a counter-argument: {e}. "
                "Please check your GROQ_API_KEY and internet connection."
            )
