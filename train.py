import sys
import os
import my_model
import pickle
import argparse


def main():
    # parse console arguments
    parser = argparse.ArgumentParser(description='Creates and trains model on user dataset')
    parser.add_argument(
        '--model',
        type=str,
        default='model.pkl',
        help="provide the path to save model (default: 'model.pkl')"
    )
    parser.add_argument(
        '--input-dir',
        type=str,
        default=None,
        help='provide a directory to get data from (otherwise use stdin with default value: None)'
    )
    args = parser.parse_args()
    model_path = args.model
    input_dir = args.input_dir

    # get input data
    if input_dir is not None:
        inp = []
        for file in os.listdir(input_dir):
            if file[-4:] == '.txt':
                f = open(input_dir + '/' + file, encoding='utf-8')
                inp.append(f.read())
                f.close()
    else:
        inp = sys.stdin

    # create and train model
    model = my_model.NGramModel(2)
    for line in inp:
        model.fit(line)
    print('Model created and trained successfully')

    # save model
    f = open(model_path, 'wb')
    pickle.dump(model, f)
    f.close()
    print('Model saved')
    print('Done')


if __name__ == '__main__':
    main()
