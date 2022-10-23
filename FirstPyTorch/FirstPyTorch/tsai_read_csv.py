import pandas as pd
import numpy as np
import pprint


def foo_bar(x):
    if x == 'x':
        return 0

    if x.startswith('b'):
        if x == 'bx':
            return 0
        
        ret = int(x[1:], 2)
        return ret

    try:
        iv = int(x)
        return iv
    except:
        return x

    return None


TRAIN = 0
TEST = 1


def read_from_csv(train_filenames: list, test_filenames: list):
    len_train_dumps = len(train_filenames)
    len_test_dumps = len(test_filenames)

    MAX_TIMESTAMP_COUNT = 300

    #
    X = []
    y = []
    splits = [[], []]

    #
    train_index = 0
    test_index = 0
    for train_index in range(len_train_dumps):
        print(f'training item {train_index}...')
        dump_index = train_index
        in_filename = train_filenames[train_index]

        #
        df = pd.read_csv(in_filename)
        df = df.applymap(foo_bar)

        #
        signal_times = np.array([
            int(_item) for _item in list(df.columns)[2:]], dtype=np.float32)
        len_signal_times = len(signal_times)
        #print(f'(#{len_signal_times}) {signal_times}')

        time_list = list(range(len_signal_times))
        #print(f'(#{len_signal_times}) {time_list}')


        #
        signals = list(df.index)
        len_signals = len(signals)
        #print(f'(#{len_signals}) {signals}')


        #
        if False:
            X_now = []
            for row_index in range(len_signals):
                row = np.array(df.iloc[row_index].values[2:], dtype=np.float32)
                X_now.append(row)
            X_now.append(signal_times)

        elif False:
            res = df.to_records(index=True)
            res_pd = pd.DataFrame(res.ravel())
            X.append(res_pd)

        elif True:
            df_t0 = df.transpose()[2:]
            df_t0['time'] = df_t0.index
            #df_t1 = df_t0[[0, 1, 2, 3, 4, 5]].transpose()
            df_t1 = df_t0.transpose()
            #df_t1['time'] = df_t1.columns

            #
            v_time = int(df_t0['time'][len_signal_times-1])
            for i in range(MAX_TIMESTAMP_COUNT - len_signal_times):
                df_t1[[str(v_time + i + 1)]] = np.nan

            if len_signal_times >= MAX_TIMESTAMP_COUNT:
                print('ERROR!')

            #
            df_t1 = df_t1.fillna(method='ffill', axis=1)

            #
            #print(df_t0)
            #print(df_t1)

            #
            X.append(df_t1.to_numpy(dtype=np.float32))

        else:
            pass

        #
        #pprint.pprint(X)

        #
        y.append(1)

        # training dumps
        splits[TRAIN].append(train_index)

        #
        #pprint.pprint(df)

    
    for test_index in range(len_test_dumps):
        print(f'testing item {test_index}...')
        dump_index = train_index + test_index + 1
        in_filename = test_filenames[test_index]

        #
        df = pd.read_csv(in_filename)
        df = df.applymap(foo_bar)

        #
        signal_times = np.array([
            int(_item) for _item in list(df.columns)[2:]], dtype=np.float32)
        len_signal_times = len(signal_times)
        #print(f'(#{len_signal_times}) {signal_times}')

        time_list = list(range(len_signal_times))
        #print(f'(#{len_signal_times}) {time_list}')


        #
        signals = list(df.index)
        len_signals = len(signals)
        #print(f'(#{len_signals}) {signals}')


        #
        #X_now = []
        #X.append(X_now)
        #for row_index in range(len_signals):
        #    row = np.array(df.iloc[row_index].values[2:], dtype=np.float32)
        #    X_now.append(row)
        #X_now.append(signal_times)

        #
        if False:
            X_now = []
            for row_index in range(len_signals):
                row = np.array(df.iloc[row_index].values[2:], dtype=np.float32)
                X_now.append(row)
            X_now.append(signal_times)

        elif False:
            res = df.to_records(index=True)
            res_pd = pd.DataFrame(res.ravel())
            X.append(res_pd)

        elif True:
            df_t0 = df.transpose()[2:]
            df_t0['time'] = df_t0.index
            #df_t1 = df_t0[[0, 1, 2, 3, 4, 5]].transpose()
            df_t1 = df_t0.transpose()
            #df_t1['time'] = df_t1.columns

            #
            v_time = int(df_t0['time'][len_signal_times-1])
            for i in range(MAX_TIMESTAMP_COUNT - len_signal_times):
                df_t1[[str(v_time + i + 1)]] = np.nan

            if len_signal_times >= MAX_TIMESTAMP_COUNT:
                print('ERROR!')

            #
            df_t1 = df_t1.fillna(method='ffill', axis=1)

            #
            #print(df_t0)
            #print(df_t1)

            #
            X.append(df_t1.to_numpy(dtype=np.float32))

        else:
            pass

        #
        #pprint.pprint(X)

        #
        y.append(1)

        # training dumps
        splits[TEST].append(dump_index)

        #
        #pprint.pprint(df)

    #
    return X, y, splits