import argparse
import pickle


def main():
    # parse console arguments
    parser = argparse.ArgumentParser(description='Loads model and generates a text')
    parser.add_argument(
        '--model',
        type=str,
        default='model.pkl',
        help='provide the path to load model (default: model.pkl)'
    )
    parser.add_argument(
        '--prefix',
        type=str,
        default='',
        help="provide the prefix to start text with (default: '')"
    )
    parser.add_argument(
        '--length',
        type=int,
        default=50,
        help='provide the length of text (default: 50)'
    )
    args = parser.parse_args()
    model_path = args.model.strip('/')
    text_prefix = args.prefix
    length = args.length

    # load model
    f = open(model_path, 'rb')
    model = pickle.load(f)
    f.close()

    # generate text (possible to use custom seed,
    # current time is used as seed by default)
    text = model.generate(length, text_prefix)

    # print result
    print(text)


if __name__ == '__main__':
    main()
