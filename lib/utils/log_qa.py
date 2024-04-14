import os
import aspose.words as aw
from datetime import datetime
from lib.utils.information_schema import Person

def similarity_log_qa(input: str, output: list):
    text = ""
    time = datetime.now()
    cnt = 0
    for doc,score in output:
        text += f"SOURCE_{cnt}: " + doc.metadata["source"] + "\n" + "CONTENT: " + "\n"+" "+ doc.page_content + "\n" + "Similarity L2 Score: " + str(score) + "\n"
        
        cnt += 1
    
    file = open(r"lib\\log_QA\\similarity_log_qa.txt", "a",encoding="utf-8")
   
    file.write("----------INPUT----------:"+ "\n" + 
               input + "\n" + "----------OUTPUT----------:" +"\n"+ 
               text + "\n"+
               "DATE: " + str(time) + "\n" + "*" * 50 + "\n")
   
    file.close()   
    
def text_to_pdf_similarity_qa():  
    
    with open(r"lib\\log_QA\\similarity_log_qa.txt", "r",encoding="utf-8") as file:
        text = file.read()
        
    # Create a blank document.
    doc = aw.Document()
    
    # Use a document builder to add content to the document.
    builder = aw.DocumentBuilder(doc)
    
    builder.write(text)
    
    doc.save(r"lib\\log_QA\\similarity_log_qa.pdf")
    
    file.close()
    
    
    
    
def math_solver_log_qa(input: str, output: str):
        
        """
        Logs the input and output of a function.
    
        Args:
            input (str): The input of the function.
            output (str): The output of the function.
    
        Returns:
            None
        """
        time = datetime.now()
        file = open(r"lib\\log_QA\\math_solver_log_qa.txt", "a",encoding="utf-8")
    
        file.write("----------INPUT----------:"+ "\n" + 
                   input + "\n" + 
                   "----------OUTPUT----------:"+"\n" + 
                   output + "\n" + 
                   "Date: " + str(time) + "\n" + "*" * 50 + "\n")
        
        file.close()
        
    
    
def text_to_pdf_math_solver_qa():
        
    with open(r"lib\\log_QA\\math_solver_log_qa.txt", "r",encoding="utf-8") as file:
        text = file.read() 
    
    # Create a blank document.
    doc = aw.Document()
    
    # Use a document builder to add content to the document.
    builder = aw.DocumentBuilder(doc)
    
    builder.write(text)
    
    doc.save(r"lib\\log_QA\\math_solver_qa.pdf")
    
    file.close()
        

def data_extractor_log_qa(filename: str, filetype: str, output: Person):
    
    time =  datetime.now()
    
    file = open(r"lib\\log_QA\\data_extractor_log_qa.txt", "a",encoding="utf-8")
    
    file.write("----------INPUT----------: "+"\n\n"+"File Name: " + filename + "\n" + "File Type: " + filetype + "\n" + 
               "----------OUTPUT----------: "+"\n\n"+
               "Name: " + output.name+"\n\n"+
               "About: "+ output.about+"\n\n"+
               "Skills: "+ str(output.skills)+"\n\n"+
               "Experience: "+ str(output.experience)+"\n\n"+
               "Education: "+ str(output.education)+"\n\n"+
               "Languages: "+ str(output.languages)+"\n\n"+
               "Certificates: "+ str(output.certificates)+"\n\n"+               
               "Date: " + str(time) + "\n" + "*" * 50 + "\n")
    
    
        

def text_to_data_extractor_qa():
    
    with open(r"lib\\log_QA\\data_extractor_log_qa.txt", "r",encoding="utf-8") as file:
        text = file.read() 
        
    
    # Create a blank document.
    doc = aw.Document()
    
    # Use a document builder to add content to the document.
    builder = aw.DocumentBuilder(doc)
    
    builder.write(text)
    
    
    doc.save(r"lib\\log_QA\\data_extractor_log_qa.pdf")
    
    file.close()
