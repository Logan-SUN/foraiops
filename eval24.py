# -*- coding: utf-8 -*-
import os,re
import json
import argparse
from rouge import Rouge
from modelscope import AutoModelForCausalLM, AutoTokenizer
from modelscope import GenerationConfig


from swift.llm import (
get_model_tokenizer, get_template, inference, ModelType, get_default_template_type
)
from swift.tuners import Swift
model_type = ModelType.yi_34b_chat
template_type = get_default_template_type(model_type)

def my_tokenizer(instr):
     outstr = re.sub(r'([\u4e00-\u9fff])([\u4e00-\u9fff])', r'\1 \2 ', instr)
     outstr = re.sub(r'([\u4e00-\u9fff])([a-zA-Z])', r'\1 \2 ', outstr)
     outstr = re.sub(r'([a-zA-Z])([\u4e00-\u9fff])', r'\1 \2 ', outstr)
     outstr = re.sub(r'([^\u4e00-\u9fffa-zA-Z0-9\s-])', r' \1 ', outstr)
     outstr = re.sub(r'\s+', ' ', outstr)
     return outstr


def score_precision(hyp,ref):
    a=json.loads(hyp)['scores']
    b=json.loads(ref)['scores']
    return a==b

def file_rouge(data_path):
    rouger=Rouge()
    couter=0
    dataset,refs,hyps=[],[],[]
    with open(data_path,'r',encoding='utf-8')as f:
        for line in f:
            dataset.append(json.loads(line.strip()))
    for cnt,item in enumerate(dataset):
        query,ref=item['query'],item['response']

        print("==================================")
        print (ref)
        ref_n=my_tokenizer(ref)
        refs.append(ref_n)

        hyp, history = inference(model, template, query)
        print("===============model==============")
        print (hyp)
        hyp_n=my_tokenizer(hyp)
        hyps.append(hyp_n)
        print("{}/{}【完成度】".format(cnt+1, len(dataset)))
        couter+=int(score_precision(hyp,ref))
        print()
    print ("!!!score_precision: {}".format(couter/len(dataset)))
    res=rouger.get_scores(hyps,refs,avg=True)
    return res

score=file_rouge(data_path)
print (score)



def parse_args():
    parser = argparse.ArgumentParser(description="parameters")
    parser.add_argument('-m', '--model', nargs='*',help="model path")
    parser.add_argument('-f', '--file', nargs='*',help="test file path")
    args = parser.parse_args()
    return args

if __name__ == "__main__":

    args = parse_args()
    ckpt_dir=args.model
    model, tokenizer = get_model_tokenizer(model_type, model_kwargs={'device_map': 'auto'})
    model = Swift.from_pretrained(model, ckpt_dir, inference_mode=True)
    template = get_template(template_type, tokenizer)

    data_path=args.file
    score=file_rouge(data_path)
    print (score)
    print ("done!")