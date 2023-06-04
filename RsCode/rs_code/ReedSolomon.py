from itertools import dropwhile, filterfalse


class ReedSolomonCode:
    def gf_16(self):
        return [
            # Table 1.4.2-1 from "NASA Technical Memorandum 102162, Tutorial on Reed-Solomon Error Correction Coding"
            # GF(2^m) = GF(2^4) = GF(16) for polynomial x^4+x+1 using alfa(x)=x, FCR=1
            1,  # [0001]  alpha 0
            2,  # [0010]  alpha 1
            4,  # [0100]  alpha 2
            8,  # [1000]  alpha 3
            3,  # [0011]  alpha 4
            6,  # [0110]  alpha 5
            12,  # [1100]  alpha 6
            11,  # [1011]  alpha 7
            5,  # [0101]  alpha 8
            10,  # [1010]  alpha 9
            7,  # [0111]  alpha 10
            14,  # [1110]  alpha 11
            15,  # [1111]  alpha 12
            13,  # [1101]  alpha 13
            9,  # [1001]  alpha 14
        ]

    def __init__(self):
        self.m = 4  # m - block length
        self.t = 3  # t - correciton capability
        self.n = pow(2, self.m) - 1  # n - block length
        self.k = self.n - 2 * self.t  # k - message length
        self.create_table()  # table - table of galois field GF(16)
        self.calculate_generator()  # generator g(x)

    def remove_zeros(message: str) -> str:
        if not message:
            return '0'
        i = 0
        while i < len(message) and message[i] == '0' and message[i + 1] != '1' and message[i + 2] != '1' and message[
            i + 3] != '1':
            i += 1
        return message[i:]

    def remove_zeros_int(self, message):
        return list(dropwhile(lambda x: x == 0, message))

    def add_zeros_at_start(self, message):
        missing_zeros = self.k * self.m - len(message)
        return message.zfill(missing_zeros + len(message))

    def create_binary_array(array):
        result = ''.join(format(element, '04b') for element in array)
        return result

    def create_binary_intArray(array):
        binary = []
        for element in array:
            b = format(element, '04b')
            for item in b:
                binary.append(int(item))
        return binary

    def convert_binInt_to_decInt(self, array):
        decimal = ''
        for element in array:
            decimal += str(element)
        decimal = self.msg_polynomial_syndromes(decimal)
        return decimal

    def create_table(self):
        self.table = self.gf_16()

    def calculate_generator(self):
        sub_polynomial_numbers = 2 * self.t
        generator = [1]
        for i in range(1, sub_polynomial_numbers + 1):
            generator = self.mul_polynomial(generator, [1, self.table[i]])
        self.generator = generator

    def encode_number_msg(self, message):
        max_word_lenghts_b = self.m * self.k

        if len(message) == max_word_lenghts_b:
            return self.printing_and_encoding_msg(message)

        elif len(message) < max_word_lenghts_b:
            return self.printing_and_encoding_msg(self.add_zeros_at_start(message))

    def mul_galois(self, x, y):
        x = int(x)
        y = int(y)
        if x == 0 or y == 0:
            return 0
        gf_x = self.table.index(x)
        gf_y = self.table.index(y)
        return self.table[(gf_x + gf_y) % (2 ** self.m - 1)]

    def mul_polynomial(self, a, b):
        a_len = len(a)
        b_len = len(b)
        solution = [0] * (a_len + b_len - 1)
        for i in range(a_len):
            for j in range(b_len):
                solution[i + j] = solution[i + j] = solution[i + j] ^ self.mul_galois(a[i], b[j])
        return solution

    def msg_polynomial(self, message):
        gf_tmp = [int(message[k:k + self.m], 2) for k in range(0, self.k * self.m, self.m)]
        i = 0
        while i < len(gf_tmp) and gf_tmp[i] == 0:
            i += 1
        return gf_tmp[i:]

    def msg_polynomial_syndromes(self, message):
        gf_tmp = [int(message[k:k + self.m], 2) for k in range(0, len(message), self.m)]
        i = 0
        while i < len(gf_tmp) and gf_tmp[i] == 0:
            i += 1
        return gf_tmp[i:]

    def calculate_parity_check(self, message):
        t1 = [1] + [0] * (self.t * 2)
        msg = self.mul_polynomial(message, t1)
        _, r = self.galois_div(msg, self.generator)
        return r

    def calculate_syndromes(self, message):
        result, reminder = self.galois_div(message, self.generator)
        return reminder

    def calculate_syndrome_weight(self, message):
        diff = 0
        for item in message:
            if item != 0:
                diff += 1
        return diff

    def correct_message(self, message, syndrome):
        message.reverse()
        syndrome.reverse()
        result = []
        i = 0
        while i < len(message) and i < len(syndrome):
            result.append(self.galois_add(message[i], syndrome[i]))
            i += 1
        result.extend(message[i:])
        result.reverse()
        return result

    def bin_to_decimal(self, message):
        decimal_array = []

        for i in range(0, len(message), 4):
            bits = message[i:i + 4]
            decimal_number = 0

            for bit in bits:
                decimal_number = (decimal_number << 1) | bit

            decimal_array += [decimal_number]

        return decimal_array

    def shift_right(self, message):
        message = ReedSolomonCode.create_binary_intArray(message)
        message = message[-4:] + message[0:-4]
        return self.bin_to_decimal(message)

    def shift_left(self, message):
        return message[4:] + message[:4]

    def decode_mochnacki(self, message):
        i = 0
        if len(message) < 15:
            for i in range(15 - len(message)):
                message = [0] + message
        result = message.copy()

        while i <= self.k:
            s = self.calculate_syndromes(result)
            w = self.calculate_syndrome_weight(s)
            if w <= self.t:
                result = self.correct_message(result, s)
                result = ReedSolomonCode.create_binary_intArray(result)
                for j in range(i):
                    result = self.shift_left(result)
                result = self.convert_binInt_to_decInt(result)
                print("Decoded M(x):             ", result)
                return result
            if i == self.k:
                try:
                    raise Exception('Uncorrectable Error Exception')
                except Exception as exp:
                    print("Exception: ", exp)
            result = self.shift_right(result)
            i += 1
        return result

    def galois_div(self, d1, d2):
        solution = list(d1)
        for i in range(len(d1) - (len(d2) - 1)):
            parameter = solution[i]
            if parameter != 0:
                for j in range(1, len(d2)):
                    if d2[j] != 0:
                        solution[i + j] ^= self.mul_galois(d2[j], parameter)
        separator = -(len(d2) - 1)
        return solution[:separator], solution[separator:]

    def printing_and_encoding_msg(self, message):
        self.print_rs_parameters()
        print('M(X)                      ', message)
        message_polynomial = self.msg_polynomial(message)
        print('M(X) to 10\'               ', message_polynomial)
        C_x = self.calculate_parity_check(message_polynomial)
        print('CK(X):                    ', C_x)
        poly_encoded = message_polynomial + C_x
        print('C(X)=M(X)+CK(X)           ', poly_encoded)
        print(25 * '-', "Encoding completed", 25 * '-')
        encoded_message = message + ReedSolomonCode.create_binary_array(C_x)
        encoded_message = ReedSolomonCode.remove_zeros(encoded_message)
        encoded_message = self.msg_polynomial(encoded_message)
        return poly_encoded

    def print_rs_parameters(self):
        print('Reed-Solomon(', self.n, ',', self.k, ')', 'g(x)', self.generator, '\n')

    def galois_add(self, a, b):
        return a ^ b

    def galois_power(self, number, i):
        return 1 if i == 0 else self.table[(self.table.index(number) * i) % (2 ** self.m - 1)]

    def calc_poly(self, polynomial, value):
        l = len(polynomial)
        total = polynomial[l - 1]
        for i in range(1, l):
            total = self.galois_add(total, self.mul_galois(polynomial[l - i - 1], self.galois_power(value, i)))
        return total

    def calc_syndroms_berle(self, polynomial):
        return [self.calc_poly(polynomial, self.table[i]) for i in range(1, 2 * self.t + 1)]

    def berlekamps_massey(self, syndromes):
        k, l = 1, 0
        c_x, delta_x = [1, 0], [1]
        while k <= 2 * self.t:
            e = syndromes[k - 1]
            for j in range(1, l + 1):
                e = self.galois_add(e, self.mul_galois(delta_x[len(delta_x) - j - 1], syndromes[k - 1 - j]))
            if e != 0:
                delta_star = self.add_polynomials(delta_x, self.mul_poly_by_scalar(c_x, e))
                if 2 * l < k:
                    l = k - l
                    c_x = self.mul_poly_by_scalar(delta_x, self.galois_inv(e))
                delta_x = delta_star
            k += 1
            c_x.append(0)
        delta_x = list(dropwhile(lambda x: x == 0, delta_x))
        if len(delta_x) - 1 > self.t:
            raise Exception
        return delta_x

    def galois_inv(self, x):
        if x == 0:
            return 0
        if x == 1:
            return 1
        return self.table[((2 ** self.m - 1) - self.table.index(x))]

    def mul_poly_by_scalar(self, polynomial, scalar):
        # multiplied = [0] * len(polynomial)
        # for i in range(0, len(polynomial)):
        #     multiplied[i] = self.__multiply_galois(polynomial[i], scalar)
        return [self.mul_galois(polynomial[i], scalar) for i in range(0, len(polynomial))]

    def add_polynomials(self, p1, p2):
        if len(p1) > len(p2):
            greater = p1
            lesser = [0] * (len(p1) - len(p2)) + p2
        else:
            greater = p2
            lesser = [0] * (len(p2) - len(p1)) + p1
        len_g, len_l = len(greater), len(lesser)

        return [self.galois_add(greater[i], lesser[i]) if i < len_l else greater[i] for i in range(0, len_g)]

    def calc_magnitude(self, syndromes, locator):
        syndromes_r = syndromes.copy()
        syndromes_r.reverse()
        delt = self.mul_polynomial(syndromes_r, locator)
        return self.galois_div(delt, [1] + [0] * (self.t * 2 - 1))[1]

    def chein_search(self, error_locator_polynomial):
        return list(filterfalse(lambda x: self.calc_poly(error_locator_polynomial, x) != 0, self.table))

    def calc_forney(self, magnitude, error_locator, roots):
        result = []
        for root in roots:
            magnitude_tmp = self.calc_poly(magnitude, root)
            locator = self.calc_deteritive(error_locator, root)
            tmp = self.mul_galois(magnitude_tmp, self.galois_inv(locator))
            result.append(tmp)
        return result

    def calc_deteritive(self, error_locator, x):
        error_locator_r = error_locator.copy()
        error_locator_r.reverse()
        total = error_locator_r[1]
        power = 2
        for i in range(3, len(error_locator_r)):
            if i % 2 != 0:
                total = self.galois_add(total, self.mul_galois(error_locator_r[i], self.galois_power(x, power)))
                power += 2
        if total == 0:
            raise Exception()
        return total

    def correct_msg(self, polynomial, err_vals, err_indx):
        if max(err_indx) < len(polynomial):
            for i in range(len(err_vals)):
                index = len(polynomial) - err_indx[i] - 1
                polynomial[index] = self.galois_add(polynomial[index], err_vals[i])
        else:
            raise Exception('Uncoretable')
        return polynomial

    def complete_decoding_algorithm(self, message):
        syndromes = self.calc_syndroms_berle(message)
        # print('Syndromes                 ', syndromes)
        if sum(syndromes) == 0:
            return message
        er_loc_poly = self.berlekamps_massey(syndromes)
        # print('Error location polyniomial', er_loc_poly)
        magnitude = self.calc_magnitude(syndromes, er_loc_poly)
        magnitude = self.remove_zeros_int(magnitude)
        # print('Magnitude                 ', magnitude)
        er_loc = self.chein_search(er_loc_poly)
        # print('Chein                     ', er_loc)
        if len(er_loc) != len(er_loc_poly) - 1:
            raise Exception('Uncoretable')
        if len(er_loc) > self.t:
            raise Exception('Uncoretable')
        er_val = self.calc_forney(magnitude, er_loc_poly, er_loc)
        # print('Forney (errors values)    ', er_val)
        er_indx = list(map(lambda x: self.table.index(self.galois_inv(x)), er_loc))
        # print('Errors index              ', er_indx)
        corrected_msg = self.correct_msg(message, er_val, er_indx)
        syndromes_corrected = self.calc_syndroms_berle(corrected_msg)
        if sum(syndromes_corrected) != 0:
            return Exception('Uncoretable')
        # print(25*'-',"Decoding completed",25*'-')
        return corrected_msg

# Uproszczony dekoder
# błedy w cx i mx osobno i sprawdzic jak wychodzi
