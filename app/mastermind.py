import unicodedata

#from app.commands.quotes import process as quotes

def get_response(msg):
    
    msg = unicodedata.normalize('NFKD', msg).encode('ASCII', 'ignore').strip().decode("utf-8").lower()

    # Here we should implement some sort of AI/NLP/LSTM to give the user a proper reply
    # You could aso use a service like Watson, Luis or Wit.
    # Or just implement some predefined comands
    
    # In this example We are going to just send the message back to the user.
    return "Echo Bot: {}".format(msg)
