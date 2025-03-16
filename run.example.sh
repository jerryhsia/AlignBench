#!/bin/bash

export PYTHONPATH=$(cd $(dirname "$0");pwd)
cd $PYTHONPATH
. venv/bin/activate

# 评价模型信息
export API_KEY=sk-xxxx
export API_URL=https://api.deepseek.com/chat/completions
export API_MODEL=deepseek-reasoner

# 待评测模型信息
export QIANFAN_API_DEBUG=true
export QIANFAN_API_TIMEOUT=240
export QIANFAN_API_KEY=sk-xxx
export QIANFAN_API_URL=http://47.108.78.149:8916/predict

python3 get_answers.py --model qianfan_private --workers 3 --question-file question/data_release.jsonl --save-dir data/model_answer
python3 judge.py --config-path config/multi-dimension.json --model-name qianfan_private --parallel 3
python3 show_result.py --input-dir data/judgment --ques-file question/data_release.jsonl --save-file data/results/results.xlsx