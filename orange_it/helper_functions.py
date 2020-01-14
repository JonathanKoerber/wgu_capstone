def salt_password(password):
    # for every 2 characters, insert #!
    iterations = 0
    password_array = []
    for char in password:
        iterations += 1
        password_array.append(char)
        if iterations % 2 == 0:
            password_array.append('#!')
    return ''.join(password_array)

