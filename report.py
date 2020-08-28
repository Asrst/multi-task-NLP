"""
File for generating report (f1-score, classification report), given a pred_file task containing
with coloumns 'uid', 'prediciton', 'label'
"""
from utils.task_utils import TasksParam
from utils.data_utils import TaskType, ModelType, NLP_MODELS
from utils.eval_metrics import *
from data_preparation import * 
import argparse
import logging
import os
from ast import literal_eval

# logger = logging.getLogger("multi_task")

def load_pred_file(dataPath, taskType, hasColNames):
    '''
    This fn loads data from tsv file in according to the format in taskType
    dataPath - path/name of file to read
    taskType - Type of task for which format will be set. Can be 
                Single Sentence Classification
                Sentence Pait Classification, NER
    hasColNames - Whether or not the file has columns. When hasColNames is not True, 
                it will not skip the first row
    '''
    true_labels = []
    predictions = []
    f = open(dataPath)
    for i, line in enumerate(f):
        if hasColNamesa and i < 1:
            continue
        cols = line.strip("\n").split("\t")
        assert len(cols) == 3, "Data not in required format, should have 3 coloumns 'uid', 'prediciton', 'label'"

        if taskType == TaskType.SingleSenClassification:
            pass

        elif taskType == TaskType.SentencePairClassification:
            pass
            
        elif taskType == TaskType.NER:
            true_labels.append(liter_eval(cols[-1]))
            predictions.append(liter_eval(cols[-2]))
        
        else:
            raise ValueError(taskType)

    return (true_labels, predictions)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task_file', type=str, required = True,
                        help = "path to task file.")
    parser.add_argument('--task_name', type=str, required = True,
                        help = "task name for which report is required.")
    parser.add_argument('--pred_file_path', type = str, required=True,
                        help="path to the saved prediction file")
    parser.add_argument('--hasColNames', default = False, action = 'store_true',
                        help="if pred_file provided is having column names to skip in first row")
                        

    args = parser.parse_args()

    allParams = vars(args)
    assert os.path.exists(args.pred_file_path), "prediction tsv file not present at {}".format(args.pred_file_path)

    tasks = TasksParam(args.task_file)
    taskType = tasks.taskTypeMap[args.task_name]
    true, preds = load_pred_file(args.pred_file_path, taskType, args.hasColNames)

    if taskType == TaskType.SingleSenClassification:
            pass
    elif taskType == TaskType.SentencePairClassification:
        pass
        
    elif taskType == TaskType.NER:
        from seqeval.metrics import classification_report
        seq_f1 = seqeval_f1_score(true, preds)
        print('Seq_f1_score on {}:{}'.format(taskName, seq_f1))

        seq_precision = seqeval_precision(true, preds)
        print('Seq_f1_score on {}:{}'.format(taskName, seq_precision))

        seq_recall = seqeval_recall(true, preds)
        print('Seq_f1_score on {}:{}'.format(taskName, seq_recall))

        print('\nClassifiction Report on {}:'.format(taskName))
        print(classification_report(true,preds))        
    else:
        raise ValueError(taskType)

if __name__ == "__main__":
    main()