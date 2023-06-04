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

message = encoder.encode_number_msg('111110010001101000110011110001001')

error1_array = []
for i in range(0, 9):
    check_message = message.copy()
    messageTmp = message.copy()
    messageTmp[i] = random.randint(1, 15)
    print("Message:                  ", message)
    print("Corrupted msg:            ", messageTmp)
    decoded = encoder.decode_mochnacki(messageTmp)
    print('Fully decoded message     ', decoded)
    if (check_message == decoded):
        error1_array.append([i, '1'])
    else:
        error1_array.append([i, '0'])
df = pd.DataFrame(error1_array, columns=['Index1', 'Match'])
df.to_csv(r'../Mochnacki/data_er1_moch_msg.csv', index=False)

print("2 ERRORY")
print("2 ERRORY")
print("2 ERRORY")

error2_array = []
for i in range(0, 9):
    check_message = message.copy()
    messageTmp = message.copy()
    error1 = random.randint(1, 15)
    for j in range(i + 1, 9):
        messageTmp = message.copy()
        messageTmp[i] = error1
        messageTmp[j] = random.randint(1, 15)
        print("Message:                  ", message)
        print("Corrupted msg:            ", messageTmp)
        decoded = encoder.decode_mochnacki(messageTmp)
        print('Fully decoded message     ', decoded)
        if (check_message == decoded):
            error2_array.append([i, j, '1'])
        else:
            error2_array.append([i, j, '0'])
df = pd.DataFrame(error2_array, columns=['Index1', 'Index2', 'Match'])
df.to_csv(r'../Mochnacki/data_er2_moch_msg.csv', index=False)

print("3 ERRORY")
print("3 ERRORY")
print("3 ERRORY")

error3_array = []
for i in range(0, 9):
    check_message = message.copy()
    messageTmp = message.copy()
    error1 = random.randint(1, 15)
    for j in range(i + 1, 9):
        messageTmp = message.copy()
        error2 = random.randint(1, 15)
        for k in range(j + 1, 9):
            messageTmp = message.copy()
            messageTmp[i] = error1
            messageTmp[j] = error2
            messageTmp[k] = random.randint(1, 15)
            print("Message:                  ", message)
            print("Corrupted msg:            ", messageTmp)
            decoded = encoder.decode_mochnacki(messageTmp)
            print('Fully decoded message     ', decoded)
            if (check_message == decoded):
                error3_array.append([i, j, k, '1'])
            else:
                error3_array.append([i, j, k, '0'])
df = pd.DataFrame(error3_array, columns=['Index1', 'Index2', 'Index3', 'Match'])
df.to_csv(r'../Mochnacki/data_er3_moch_msg.csv', index=False)


def calc_avg(file_name):
    df = pd.read_csv(file_name)
    avg = df['Match'].mean()
    return avg


error1_avg = calc_avg(r'../Mochnacki/data_er1_moch_msg.csv')
print("1 Error average: ", error1_avg)
error2_avg = calc_avg(r'../Mochnacki/data_er2_moch_msg.csv')
print("2 Error average: ", error2_avg)
error3_avg = calc_avg(r'../Mochnacki/data_er3_moch_msg.csv')
print("3 Error average: ", error3_avg)
