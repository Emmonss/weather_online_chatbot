from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
import sys

def Load_model():
    agent = Agent.load("models/dialogue",
                       interpreter=RasaNLUInterpreter("models/ivr/demo"))
    return agent

def get_res(agent,text):
    try:
        res = agent.handle_message(text)
        return res
    except Exception as e:
        print(e)


if __name__ == '__main__':
    agent = Load_model()
    print("请输入：")
    while True:
        try:
            text = input()
            if not text == None:
                res = test(agent,text)
                for i in range(len(res)):
                    print(res[i]['text'])
        except Exception as e:
            print(e)

