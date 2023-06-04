from RsCode.rs_code.ReedSolomon import ReedSolomonCode

encoder = ReedSolomonCode()
message = encoder.encode_number_msg('10010001101000110011110001001')

print("Message:                  ", message)
message[3] = 11
print("Corrupted msg:            ", message)
decoded = encoder.complete_decoding_algorithm(message)
print('Fully decoded message     ', decoded)
