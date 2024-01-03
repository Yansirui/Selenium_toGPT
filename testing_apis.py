#import api_backend
import json

def read_json(json_path):
    with open(json_path,'r',encoding='utf-8') as f:
        str=f.read()
        data=json.loads(str)
        return data
def get_information(content):
    #print(sentences[373])
    #sentences=list(set(sentences))
    #print(len(sentences))
    times=0
    with open(r'D:/Postgratuate/项目/继续预训练框架/构建sts数据集/医疗领域/responses_fromgpt.txt','a',encoding='utf-8') as f:
        for term_sentence in content:
            if times!= 0 and times % 150 == 0:
                api_backend.add_session()
            if times==0:
                api_backend.start_chat_gpt()
            times=times+1
            prompt = r'假设你是一个医生，请你根据"{}"这句话对{}解释的角度，结合自己的知识，对这句话进行精简改写'.format(term_sentence['description'],term_sentence['term'])
            a = api_backend.make_gpt_request(prompt)
            #receive,q=api_backend.Receive_limit()
            #if receive:
            #    a=q
            a=a.replace('\n','')
            print(a)
            f.write(a+'\n')
    api_backend.stop_chat_gpt()

while True:
    with open(r'D:/Postgratuate/项目/继续预训练框架/构建sts数据集/医疗领域/responses_fromgpt.txt','r',encoding='utf-8') as f:
        sentences = f.readlines()
    content = read_json(r'D:/Postgratuate/项目/继续预训练框架/构建sts数据集/医疗领域/term_descriptions.json')[len(sentences):]
    if len(content) == 0 :
        break
    else:
        import api_backend
        print(content[0]['description'])
        get_information(content)
