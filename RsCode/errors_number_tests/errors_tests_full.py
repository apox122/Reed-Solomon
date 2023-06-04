import random

import pandas as pd

from RsCode.rs_code.ReedSolomon import ReedSolomonCode

encoder = ReedSolomonCode()


def create_msg(length):
    s = ''
    for i in range(length):
        s = s + (str)(random.randint(0, 1))
    return s


length_bit = 36
msg = create_msg(length_bit)
print(msg, '\n')
message = encoder.encode_number_msg('10010001101000110011110001001')

error1_array = []
for i in range(0, len(message)):
    messageTmp = message
    messageTmp[i] = random.randint(1, 15)
    print("Message:                  ", message)
    print("Corrupted msg:            ", messageTmp)
    decoded = encoder.complete_decoding_algorithm(messageTmp)
    print('Fully decoded message     ', decoded)
    if (message == decoded):
        error1_array.append([i, '1'])
    else:
        error1_array.append([i, '0'])
df = pd.DataFrame(error1_array, columns=['Index', 'Match'])
df.to_csv(r'../CompleteDecoding/data_er1.csv', index=False)

error2_array = []
for i in range(0, len(message)):
    messageTmp = message
    corruptTmp = random.randint(0, 15)
    for j in range(i + 1, len(message)):
        messageTmp[i] = corruptTmp
        messageTmp[j] = random.randint(0, 15)
        print("Message:                  ", message)
        print("Corrupted msg:            ", messageTmp)
        decoded = encoder.complete_decoding_algorithm(messageTmp)
        print('Fully decoded message     ', decoded)
        if (message == decoded):
            error2_array.append([i, j, '1'])
        else:
            error2_array.append([i, j, '0'])
df = pd.DataFrame(error2_array, columns=['Index1', 'Index2', 'Match'])
df.to_csv(r'../CompleteDecoding/data_er2.csv', index=False)

error3_array = []
for i in range(0, len(message)):
    messageTmp = message
    corruptTmp = random.randint(1, 15)
    for j in range(i + 1, len(message)):
        corruptTmp2 = random.randint(1, 15)
        for k in range(j + 1, len(message)):
            messageTmp[i] = corruptTmp
            messageTmp[j] = corruptTmp2
            message[k] = random.randint(1, 15)
            print("Message:                  ", message)
            print("Corrupted msg:            ", messageTmp)
            decoded = encoder.complete_decoding_algorithm(messageTmp)
            print('Fully decoded message     ', decoded)
            if (message == decoded):
                error3_array.append([i, j, k, '1'])
            else:
                error3_array.append([i, j, k, '0'])
df = pd.DataFrame(error3_array, columns=['Index1', 'Index2', 'Index3', 'Match'])
df.to_csv(r'../CompleteDecoding/data_er3.csv', index=False)


def calc_avg(file_name):
    df = pd.read_csv(file_name)
    avg = df['Match'].mean()
    return avg


error1_avg = calc_avg(r'../CompleteDecoding/data_er1.csv')
print("1 Error average: ", error1_avg)
error2_avg = calc_avg(r'../CompleteDecoding/data_er2.csv')
print("2 Error average: ", error2_avg)
error3_avg = calc_avg(r'../CompleteDecoding/data_er3.csv')
print("3 Error average: ", error3_avg)
