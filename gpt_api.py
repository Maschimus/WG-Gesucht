import openai
import api_keys
class GPTAPI:
    openai.api_key = api_keys.api_key_gpt
    
    def __init__(self):
        self.my_text ='''
           Add a long discription here
        '''


    def chat_with_chatgpt(self,prompt, model="text-davinci-003"):
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=False,
            temperature=0.1,
        )

        message = response.choices[0].text.strip()
        return message
    
    
    def get_evaluation_of_fit(self,wg_text):
        print("I make my suggestions now")
        prompt=" Bitte geben Sie nur bitte nur genau eine Zahl von 1 bis 10 an, um die Passgenauigkeit zu bewerten. Wobei 10 perfekt und 1 misserabel ist. Es handelt sich um WGs: \n \n \n" +self.my_text +"\n \n \n" +wg_text
        reply=self.chat_with_chatgpt(prompt)
        try:
            print("This is a "+ str(int(reply))+" Fit.")
            return(int(reply))
        except Exception as e:
            reply=self.get_evaluation_of_fit(wg_text="Bitte nenne nur die Zahl")
            try:
                print("This is a "+ str(int(reply))+" Fit.")
                return int(reply)
            except Exception as e:
                print("Somehow did not work")
                return 0
        
    def write_text(self,text_wg):
        prompt="Schreibe mir ein einschreiben für die WG mit diesem Text: " + text_wg+ "mit meinem nachfolgenden Text als Vorlage: \n" +self.my_text
        text=self.chat_with_chatgpt(prompt)
        return text
                 
    
