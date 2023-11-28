import api_backend

#api_backend.start_chat_gpt()
with open(r'Dataset/Corpus/term-timesPair.txt','r',encoding='utf-8') as f:
    termpairs = f.readlines()[6200:]
terms=[]
response=[]
for t in termpairs:
    terms.append(t.split('\t')[0])
chunk_size=20
result_list = [terms[i:i + chunk_size] for i in range(0, len(terms), chunk_size)]
times=0
with open(r'Dataset/Corpus/responses_fromgpt.txt','a',encoding='utf-8') as f:
    for terms_list in result_list:
        if times==0:
            api_backend.start_chat_gpt()
        times=times+1
        prompt = r'我将提供给你一个包含20个中文词汇的列表，请你对列表中的中文词汇进行分类，中文词汇列表为{},具体类别为[通用领域词汇，电商领域词汇，医疗领域词汇，金融领域词汇，文娱领域词汇]，反馈格式为json格式，如 "可以":"通用领域词汇" ，“电影”:"文娱领域词汇"'.format(terms_list)
        a = api_backend.make_gpt_request(prompt)
        receive,q=api_backend.Receive_limit()
        if receive:
            a=q
        a=a.replace('\n','')
        response.append(a)
        print(a)
        f.write(a+'\n')
api_backend.stop_chat_gpt()