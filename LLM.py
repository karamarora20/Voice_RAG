from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain.tools import StructuredTool
from tool_functions import speak,takecommand,google_search as search
from langchain.memory import ConversationBufferWindowMemory




    

    
class openai_llm:
    def __init__(self):
        
        system = '''Respond to the human as helpfully and accurately as possible. You have access to the following tools:

                {tools}
                
                You can use the following tools:
                1. Search: Use a search tool to find information from the web.
                
                Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

                Valid "action" values: "Final Answer" or {tool_names}
                You will follow these instructions to help the human:

                1. Always keep the input of search tool as a string.
                

                Provide only ONE action per $JSON_BLOB, as shown:

                ```
                {{
                "action": $TOOL_NAME,
                "action_input": $INPUT
                }}
                ```

                Follow this format:

                Question: input question to answer
                Thought: consider previous and subsequent steps
                Action:
                ```
                $JSON_BLOB
                ```
                Observation: note any changes or results
                Thought: I know what to respond
                Action:
                ```
                {{
                "action": "Final Answer",
                "action_input": "Final response to human"
                }}


                
                Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation'''

        human = '''
                    {chat_history}
        {input}

                {agent_scratchpad}

                (reminder to respond in a JSON blob no matter what)'''

        self.prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", system),
                        MessagesPlaceholder("chat_history", optional=True),
                        ("human", human),
                    ]
                )
        self.agent= self.create_agent()





    def initialize_llm(self):
        return ChatOpenAI(temperature=0.5)
    
    def make_tool(self,tool):
        return StructuredTool.from_function(tool)

    def create_agent(self):
        memory=ConversationBufferWindowMemory(output_key='output',window_size=5)
        tools=[self.make_tool(search)]
        agent = create_structured_chat_agent(self.initialize_llm(), tools, self.prompt)
        agent_executor = AgentExecutor(
        agent=agent, tools=tools, memory=memory,verbose=True,handle_parsing_errors=True
    )
        return agent_executor
    def get_llm_response(self,query):
        result=self.agent.invoke({'input':query})
        return result['output']

        

speak("Hi, my name is JV how would I help you?")
agent=openai_llm()
while(True):
    
    query=takecommand().lower()
    if 'exit' in query or 'bye' in query:
        speak("Goodbye, have a nice day")
        break
    speak("Sure give me some time to think about it")
    response=agent.get_llm_response(query)
    speak(response)
    speak('Is there anything else I can help you with?')



