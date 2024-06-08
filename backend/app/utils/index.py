import logging
import os
from langchain_openai import OpenAI
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from llama_index.core.query_engine import NLSQLTableQueryEngine
from langchain.utilities import GoogleSearchAPIWrapper
from llama_index.core import SQLDatabase
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
)
from sqlalchemy import insert
from dotenv import load_dotenv
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase


load_dotenv("../../.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class HealthUtil:
    def __init__(self
                 )-> None:
        engine = create_engine("sqlite:///:memory:")
        metadata_obj = MetaData()

        # create Medical Resources Table SQL table
        table_name = "chitwon_hospital_ambulence_blood_bank_contact_number"
        medical_resource_table = Table(
            table_name,
            metadata_obj,
            Column("hospital_name", String(16), primary_key=True),
            Column("hospital_contact_number", String(16)),
            Column("Ambulence_service_name", String(25)),
            Column("Ambulence_service_contact_number", String(25)),
            Column("Blood_bank_name", String(25)),
            Column("Blood_bank_contact_number", String(25))
        )
        metadata_obj.create_all(engine)
        rows = [
            {"hospital_name": "BP Koirala Memorial Cancer Hospital", "hospital_contact_number":"056-524501","Ambulence_service_name":"B.P. Koirala Institute of Health Science","Ambulence_service_contact_number":"9845050113", "Blood_bank_name":"BP Koirala Memorial Cancer Hospital","Blood_bank_contact_number":"056-524501"},
            {"hospital_name": "Manakamana Hospital Pvt. Ltd.", "hospital_contact_number":"056-520180","Ambulence_service_name":"Chitwan Ambulance service ","Ambulence_service_contact_number":"9845731448,9813004484", "Blood_bank_name":"Nepal Redcross society Blood Bank","Blood_bank_contact_number":"056-595880"},
            {"hospital_name": "Bharatpur Hospital.", "hospital_contact_number":"056-597003","Ambulence_service_name":"Aksheri Smriti Pratishthan","Ambulence_service_contact_number":"9845151558", "Blood_bank_name":"Blood Donor's Society Nepal","Blood_bank_contact_number":" 985-5015362"},
            {"hospital_name": "Chitwan Medical College Teaching Hospital", "hospital_contact_number":"056-432933","Ambulence_service_name":"Asha Hospital","Ambulence_service_contact_number":"9845501011", "Blood_bank_name":"Youth For Blood Chitwan","Blood_bank_contact_number":"984-7269550"},

        ]
        for row in rows:
            stmt = insert(medical_resource_table).values(**row)
            with engine.begin() as connection:
                cursor = connection.execute(stmt)

        self.sys_prompt =  """Act as a very good and famous doctor and AI medical expert chatbot who works for patients.\
            You have lots of successful experience and have already served many users. You are here to guide users about their\
            demand in the medical field, so try to keep users from discussing anything other than medical. Your user is not familiar\ 
            with medical concepts, so use easy to understand words. In your response, you should ask user to consult with you instead\ 
            of a medical expert when they need medical consultation. You have been trained to be a very good medical expert. \
            Never ask user to consult with a medical expert! Only answer related to medical domain, symptoms and guidance for diagnosing and helping. Reply "I am a virtual doctor who can assist you in diagnosing your symptoms and provide information about the nearest healthcare services. If you have any queries related to that, feel free to ask, and I am happy to help you." \n
            As a medical expert you should follow following instructions delimited with backticks:
            '''
            1. You should generate your response in more concise and condense way rather than very long\
            2. You should properly greet when user greet.
            3. You should only generate exactly as given to introduce yourself when user greet you: "Namaste! I'm your friendly AI healthcare friend, here to help you feel better and navigate healthcare in Chitwon.\
            Feeling unwell? Confused about your symptoms? Need to find a hospital nearby? I'm here to listen, offer advice, and connect you with the right resources. \
            Don't hesitate to reach out I'm here to support you on your wellness journey!" \
        """

        # set memory and llm
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.llm = ChatOpenAI(model="gpt-4-1106-preview",temperature=0)
        db = SQLDatabase(engine=engine,include_tables=["chitwon_hospital_ambulence_blood_bank_contact_number"],sample_rows_in_table_info=4)
        agent_executor = create_sql_agent(self.llm, db=db, agent_type="openai-tools", verbose=True)

        # Search engine tool
        search = GoogleSearchAPIWrapper()
        self.tools = [Tool(
            name ="Search" ,
            func=search.run,
            description=self.sys_prompt
            ),
            Tool(
                name ="database search" ,
                func=agent_executor.invoke,
                description="useful for when you want to answer questions about the hospitals, blood bank, ambulence services and its contact number around chitwon city. The input to this tool should be a complete english sentence. It should help to fetch all infoo about hospital, blood bank and ambulence service contact numbers."
                ),
        ]

    # Main function to run agent
    def get_agent(self):
        logger = logging.getLogger("uvicorn")
        agent_executor = initialize_agent(
        self.tools, self.llm, agent="conversational-react-description", memory=self.memory, prefix=self.sys_prompt,handle_parsing_errors=True
    )
        return agent_executor