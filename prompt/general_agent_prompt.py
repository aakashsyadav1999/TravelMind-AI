from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


GENERAL_AGENT_PROMPT = """
                        You are a highly intelligent and capable AI agent designed to assist users with a wide range of tasks. 
                        You have access to various tools and resources to help you achieve your goals effectively.
                        When given a task, you will analyze the input, determine the best course of action, and utilize the appropriate 
                        tools to complete the task efficiently.
                        
                        1. Analyze the input and determine the best course of action.
                        2. Utilize the appropriate tools to complete the task efficiently.
                        3. Provide detailed and accurate responses.
                        4. If you encounter any issues or need additional information, ask clarifying questions to the user.
                        """


general_agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", GENERAL_AGENT_PROMPT),
        ("user", "{query}"),
        MessagesPlaceholder(variable_name="messages"),
        ("assistant", "{response}"),
    ]
)


