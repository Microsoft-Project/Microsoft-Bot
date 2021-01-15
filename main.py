from DataPipeline import prepare_dataset
from Evaluation import model_metrics
from MLPipeline import build_model


def build_model_end(model_type):
    build_model.build_save(model_type)


def datafeatures_end():
    try:
        tfidf, features, labels, category_to_id, df = build_model.get_datafeatures()
        return tfidf, features, labels, category_to_id, df
    except:
        print('File not found')


def accuaracycomp_end(features, labels):
    model_metrics.accuaracy_comp(features, labels)


def uploaddata_end(filepath):
    prepare_dataset.process_save(filepath)


if __name__ == '__main__':

    print('Welcome to team BroCode\'s label prediction bot')
    print('_______________________________________________\n')

    while True:

        print('Please choose one form the options given below -')
        print('1. Build model')
        print('2. Show accuracy comparison for all models')
        print('3. Upload new dataset')
        print('4. Quit')

        user_input = input("Option Choice: ")

        if user_input is "4":
            break

        elif user_input is "1":

            print('_______________________________________________\n')
            print('Build model')
            print('Which model would you like to build, please choose one form the options given below -')
            print('1. Logistic regression')
            print('2. LinearSVC')
            print('3. MultinomialNB')
            print('4. Random Forest Classifier')
            print('5. Quit')

            build_input = input("Build Choice: ")

            if build_input is "5":
                break
            elif build_input is "1":
                build_model_end('lgr')
            elif build_input is "2":
                build_model_end('lvc')
            elif build_input is "3":
                build_model_end('mnb')
            elif build_input is "4":
                build_model_end('rfc')

        elif user_input is '2':

            print('_______________________________________________\n')
            print('Accuracy comparisons for all models')

            _, features, labels, _, _ = datafeatures_end()

            accuaracycomp_end(features, labels)

        elif user_input is '3':

            print('_______________________________________________\n')
            print('Upload new dataset')

            print('Enter the path of the file you want to upload - \n')

            file_path = input("Path: ")
            uploaddata_end(file_path)
