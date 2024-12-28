from py_vollib.black import black
#import py_vollib_vectorized

black # check if the monkey-patch is applied.
#Vectorized <vectorized_black()>

flag = 'c'  # 'c' for call, 'p' for put
S = 95  # price of the underlying
K = 100  # strike
t = .2  # annualized time to expiration
r = .2  # interest-free rate
sigma = .2  # implied volatility

#black(flag, S, K, t, r, sigma, return_as='numpy')
out = black(flag, S, K, t, r, sigma)
print(out)