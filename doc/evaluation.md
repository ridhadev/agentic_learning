# Evaluation

To test a agentic system, we need to evaluate at different levels:

- End-to-end evaluation : Evaluate the overall accuracy, speed, ... of the workflow
- Component level evaluation : Evaluate the output of each step seperatly and identify the weak points of the chain, so we can start work on it and priorittize it.

Evaluation can be organised along two axis (Summarized in the table below):
- Obejcetive (code based) Versus Subjective (Judgement based)
- Ground truth Versus No Ground truth 

<img src='images/Evaluations-Objective-Subjective-Matrix.png' width='80%'>

The code in ./evaluation/web_search_eval.py implement a task based with ground truth evaluation.